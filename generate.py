#!/usr/bin/env python3
"""
GitHub profile SVG generator for amibhai (Swastik).
Queries the GitHub GraphQL API → writes dark/light SVGs to output/.
Run: python generate.py  (requires GH_TOKEN environment variable)
"""

import os
import json
import time
import datetime
import requests
from dateutil.relativedelta import relativedelta

# ─── Config ───────────────────────────────────────────────────────────────────

USERNAME     = "amibhai"
DOB          = datetime.date(2004, 6, 3)
GITHUB_TOKEN = os.environ["GH_TOKEN"]
HEADERS      = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}
GRAPHQL_URL = "https://api.github.com/graphql"

TOOLS = [
    ("andronet",      "packet analyzer"),
    ("wifi_down",     "wifi auditing"),
    ("recon-toolkit", "network recon"),
    ("cred-toolkit",  "credential attacks"),
    ("wordsmith",     "wordlist gen"),
]

DARK = {
    "background":   "#0d1117",
    "border":       "#30363d",
    "text_primary": "#e6edf3",
    "text_muted":   "#8b949e",
    "text_accent":  "#58a6ff",
    "text_green":   "#3fb950",
    "text_red":     "#f85149",
}

LIGHT = {
    "background":   "#ffffff",
    "border":       "#d0d7de",
    "text_primary": "#24292f",
    "text_muted":   "#57606a",
    "text_accent":  "#0969da",
    "text_green":   "#1a7f37",
    "text_red":     "#cf222e",
}

# characters allocated to label + dot-padding before x=200 value column
LABEL_WIDTH = 22


# ─── Helpers ──────────────────────────────────────────────────────────────────

def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def fmt_label(label: str) -> str:
    """Return 'label ..........' right-padded with dots to LABEL_WIDTH chars."""
    with_space = label + " "
    dots = max(0, LABEL_WIDTH - len(with_space))
    return with_space + "." * dots


def _graphql(query: str, variables: dict | None = None) -> dict:
    """Post a GraphQL query with retry logic for transient / rate-limit errors."""
    payload: dict = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(3):
        resp = requests.post(
            GRAPHQL_URL, json=payload, headers=HEADERS, timeout=30
        )

        remaining = int(resp.headers.get("X-RateLimit-Remaining", 999))
        if remaining < 10:
            print(f"[!] rate limit low ({remaining} remaining) — sleeping 60s")
            time.sleep(60)

        if resp.status_code in (502, 503):
            print(
                f"[!] HTTP {resp.status_code} — retrying in 10s "
                f"(attempt {attempt + 1}/3)"
            )
            time.sleep(10)
            continue

        if resp.status_code in (403, 429):
            print(f"[!] rate limited (HTTP {resp.status_code}) — sleeping 60s")
            time.sleep(60)
            continue

        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            raise RuntimeError(f"GraphQL error: {data['errors']}")

        return data

    raise RuntimeError("GraphQL request failed after 3 retries")


# ─── Uptime ───────────────────────────────────────────────────────────────────

def get_uptime(dob: datetime.date) -> str:
    today = datetime.date.today()
    d = relativedelta(today, dob)
    base = f"{d.years} years, {d.months} months, {d.days} days"
    if today.month == dob.month and today.day == dob.day:
        return base + " [BIRTHDAY]"
    return base


# ─── GitHub data fetchers ─────────────────────────────────────────────────────

def get_user_stats() -> dict:
    query = """
    query($login: String!) {
        user(login: $login) {
            followers { totalCount }
            repositories(ownerAffiliations: OWNER) { totalCount }
            createdAt
        }
    }
    """
    user = _graphql(query, {"login": USERNAME})["data"]["user"]
    return {
        "followers":  user["followers"]["totalCount"],
        "repos":      user["repositories"]["totalCount"],
        "created_at": user["createdAt"],
    }


def get_total_stars() -> int:
    query = """
    query($login: String!, $cursor: String) {
        user(login: $login) {
            repositories(
                ownerAffiliations: OWNER,
                first: 100,
                after: $cursor
            ) {
                nodes { stargazerCount }
                pageInfo { hasNextPage endCursor }
            }
        }
    }
    """
    total = 0
    cursor = None
    while True:
        repos = (
            _graphql(query, {"login": USERNAME, "cursor": cursor})
            ["data"]["user"]["repositories"]
        )
        for r in repos["nodes"]:
            total += r["stargazerCount"]
        if not repos["pageInfo"]["hasNextPage"]:
            break
        cursor = repos["pageInfo"]["endCursor"]
        time.sleep(0.5)
    return total


def get_total_commits(created_at: str) -> int:
    """
    Sum contributions across all calendar years from account creation to now.
    GitHub restricts contributionsCollection windows to <=366 days, so we
    loop year-by-year.
    """
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
        user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
                contributionCalendar { totalContributions }
            }
        }
    }
    """
    created_year = datetime.datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    ).year
    now = datetime.datetime.utcnow()
    total = 0

    for year in range(created_year, now.year + 1):
        from_dt = f"{year}-01-01T00:00:00Z"
        to_dt = (
            now.strftime("%Y-%m-%dT%H:%M:%SZ")
            if year == now.year
            else f"{year}-12-31T23:59:59Z"
        )
        count = (
            _graphql(query, {"login": USERNAME, "from": from_dt, "to": to_dt})
            ["data"]["user"]["contributionsCollection"]
            ["contributionCalendar"]["totalContributions"]
        )
        total += count
        time.sleep(0.5)

    return total


def _viewer_id() -> str:
    return _graphql("query { viewer { id } }")["data"]["viewer"]["id"]


def get_lines_of_code(cache: dict) -> tuple[int, int, dict]:
    """
    Returns (total_additions, total_deletions, updated_cache).
    Cache key: "{owner}/{repo}:{head_commit_sha}"
    Only re-scans repos where HEAD SHA has changed since last run.
    """
    list_query = """
    query($login: String!, $cursor: String) {
        user(login: $login) {
            repositories(
                ownerAffiliations: OWNER,
                first: 100,
                after: $cursor
            ) {
                nodes {
                    nameWithOwner
                    defaultBranchRef {
                        target { ... on Commit { oid } }
                    }
                }
                pageInfo { hasNextPage endCursor }
            }
        }
    }
    """
    commit_query = """
    query($owner: String!, $name: String!, $cursor: String) {
        repository(owner: $owner, name: $name) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            nodes {
                                additions
                                deletions
                                author { user { id } }
                            }
                            pageInfo { hasNextPage endCursor }
                        }
                    }
                }
            }
        }
    }
    """

    viewer_id = _viewer_id()

    # Collect all owned repos with their current HEAD SHA
    repos: list[dict] = []
    cursor = None
    while True:
        result = _graphql(list_query, {"login": USERNAME, "cursor": cursor})
        repo_page = result["data"]["user"]["repositories"]
        for r in repo_page["nodes"]:
            branch = r["defaultBranchRef"]
            if not branch:
                continue
            target = branch.get("target") or {}
            if "oid" not in target:
                continue
            repos.append({"nwo": r["nameWithOwner"], "sha": target["oid"]})
        if not repo_page["pageInfo"]["hasNextPage"]:
            break
        cursor = repo_page["pageInfo"]["endCursor"]
        time.sleep(0.5)

    total_add = 0
    total_del = 0
    new_cache: dict = {}

    for repo in repos:
        nwo = repo["nwo"]
        sha = repo["sha"]
        key = f"{nwo}:{sha}"

        if key in cache:
            entry = cache[key]
            total_add += entry["additions"]
            total_del += entry["deletions"]
            new_cache[key] = entry
            continue

        print(f"  scanning {nwo}...")
        owner, name = nwo.split("/", 1)
        repo_add = 0
        repo_del = 0
        cc = None

        while True:
            try:
                data = _graphql(
                    commit_query, {"owner": owner, "name": name, "cursor": cc}
                )
                ref = data["data"]["repository"]["defaultBranchRef"]
                if not ref:
                    break
                history = ref["target"]["history"]

                for commit in history["nodes"]:
                    author = commit.get("author") or {}
                    cuser  = author.get("user") or {}
                    if cuser.get("id") == viewer_id:
                        repo_add += commit["additions"]
                        repo_del += commit["deletions"]

                if not history["pageInfo"]["hasNextPage"]:
                    break
                cc = history["pageInfo"]["endCursor"]
                time.sleep(0.5)

            except Exception as exc:
                print(f"  [!] error scanning {nwo}: {exc}")
                break

        new_cache[key] = {"additions": repo_add, "deletions": repo_del}
        total_add += repo_add
        total_del += repo_del

    return total_add, total_del, new_cache


# ─── Cache I/O ────────────────────────────────────────────────────────────────

def load_cache(path: str = "cache/loc_cache.json") -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(data: dict, path: str = "cache/loc_cache.json") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ─── SVG Generator ────────────────────────────────────────────────────────────

def generate_svg(stats: dict, theme: str) -> str:
    c      = DARK if theme == "dark" else LIGHT
    W      = 480
    LEFT   = 20
    VAL_X  = 200
    LINE_H = 18
    FONT   = "'Courier New', monospace"

    elems: list[str] = []
    y = 0

    def txt(
        text: str,
        x: int,
        cy: int,
        fill: str,
        size: int = 13,
        weight: str = "normal",
    ) -> None:
        elems.append(
            f'  <text x="{x}" y="{cy}" '
            f'font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}">{xml_escape(text)}</text>'
        )

    def hline(cy: int) -> None:
        elems.append(
            f'  <line x1="{LEFT}" y1="{cy}" x2="{W - LEFT}" y2="{cy}" '
            f'stroke="{c["border"]}" stroke-width="1"/>'
        )

    def stat_row(
        label: str, value: str, val_color: str | None = None
    ) -> None:
        nonlocal y
        color = val_color or c["text_accent"]
        txt(fmt_label(label), LEFT, y, c["text_muted"])
        txt(value, VAL_X, y, color, weight="bold")
        y += LINE_H

    # ── Prompt header ─────────────────────────────────────────────────────────
    y = 34
    txt("swastik@github ~ $", LEFT, y, c["text_accent"], size=14, weight="bold")
    y += LINE_H + 6   # extra gap below header

    # ── Stats block ───────────────────────────────────────────────────────────
    stat_row("uptime", stats["uptime"])

    # OS: two-line value
    txt(fmt_label("os"), LEFT, y, c["text_muted"])
    txt("windows · linux ·", VAL_X, y, c["text_accent"], weight="bold")
    y += LINE_H
    txt("android 16", VAL_X, y, c["text_accent"], weight="bold")
    y += LINE_H

    stat_row("repos",         f"{stats['repos']:,}")
    stat_row("commits",       f"{stats['commits']:,}")
    stat_row("stars",         f"{stats['stars']:,}")
    stat_row("followers",     f"{stats['followers']:,}")
    stat_row("lines written", f"{stats['additions']:,}")

    net = stats["net_loc"]
    net_color = c["text_red"] if net < 0 else c["text_accent"]
    stat_row("net loc", f"{net:,}", val_color=net_color)

    if stats.get("api_error"):
        y += 2
        stat_row("api error", "using cached data", val_color=c["text_red"])

    # ── Separator ─────────────────────────────────────────────────────────────
    y += 6
    hline(y)
    y += LINE_H + 2

    # ── Toolkit section ───────────────────────────────────────────────────────
    txt("toolkit", LEFT, y, c["text_muted"])
    y += LINE_H + 2

    TOOL_DESC_X = 160
    for tool_name, tool_desc in TOOLS:
        txt(tool_name, LEFT,        y, c["text_primary"])
        txt(tool_desc, TOOL_DESC_X, y, c["text_muted"])
        y += LINE_H

    # ── Separator ─────────────────────────────────────────────────────────────
    y += 6
    hline(y)
    y += LINE_H

    # ── Last updated ──────────────────────────────────────────────────────────
    txt(
        f"last updated: {stats['updated_at']}",
        LEFT, y, c["text_muted"], size=11,
    )
    y += LINE_H + 10   # bottom padding

    height = y

    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{height}">\n'
        f'  <rect width="{W}" height="{height}" rx="6" ry="6" '
        f'fill="{c["background"]}" stroke="{c["border"]}" stroke-width="1"/>'
    )

    return header + "\n" + "\n".join(elems) + "\n</svg>"


def save_svg(content: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    cache = load_cache()
    api_error = False
    new_cache = dict(cache)

    print("[*] fetching github stats...")
    try:
        user_stats                       = get_user_stats()
        stars                            = get_total_stars()
        commits                          = get_total_commits(user_stats["created_at"])
        additions, deletions, loc_cache  = get_lines_of_code(cache)

        new_cache = loc_cache
        new_cache["_user_stats"] = user_stats
        new_cache["_stars"]      = stars
        new_cache["_commits"]    = commits

    except Exception as exc:
        print(f"[!] API call failed: {exc}")
        api_error = True

        cached_user = cache.get("_user_stats") or {}
        user_stats = {
            "followers":  cached_user.get("followers", 0),
            "repos":      cached_user.get("repos", 0),
            "created_at": cached_user.get("created_at", "2020-01-01T00:00:00Z"),
        }
        stars   = cache.get("_stars", 0)
        commits = cache.get("_commits", 0)

        # Sum LOC from whatever is already cached per-repo
        additions = sum(
            v["additions"] for v in cache.values()
            if isinstance(v, dict) and "additions" in v and "deletions" in v
        )
        deletions = sum(
            v["deletions"] for v in cache.values()
            if isinstance(v, dict) and "additions" in v and "deletions" in v
        )

    # Always persist cache so the next run benefits from this run's data
    save_cache(new_cache)

    stats = {
        "uptime":      get_uptime(DOB),
        "os":          "windows · linux · android 16",
        "repos":       user_stats["repos"],
        "commits":     commits,
        "stars":       stars,
        "followers":   user_stats["followers"],
        "additions":   additions,
        "net_loc":     additions - deletions,
        "updated_at":  datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "api_error":   api_error,
    }

    print("[*] generating svgs...")
    save_svg(generate_svg(stats, "dark"),  "output/profile.svg")
    save_svg(generate_svg(stats, "light"), "output/profile_light.svg")
    print("[+] done.")


if __name__ == "__main__":
    main()
