#!/usr/bin/env python3
"""
Profile plate generator for amibhai (Swastik).

Queries the GitHub GraphQL API and writes two monochrome SVGs to output/ —
one per colour scheme. README.md picks between them with <picture> +
prefers-color-scheme.

Run: python generate.py  (requires GH_TOKEN environment variable)
"""

import os
import json
import time
import datetime
import requests

# ─── Config ───────────────────────────────────────────────────────────────────

USERNAME     = "amibhai"
GITHUB_TOKEN = os.environ["GH_TOKEN"]
HEADERS      = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}
GRAPHQL_URL = "https://api.github.com/graphql"

# Monochrome only — GitHub's own neutrals, so the plate reads in either theme.
DARK = {
    "primary": "#e6edf3",
    "muted":   "#7d8590",
    "rule":    "#30363d",
}

LIGHT = {
    "primary": "#1f2328",
    "muted":   "#59636e",
    "rule":    "#d1d9e0",
}

SUBTITLE = "Offensive and defensive security tooling"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


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


# ─── GitHub data fetchers ─────────────────────────────────────────────────────

def get_user_stats() -> dict:
    query = """
    query($login: String!) {
        user(login: $login) {
            repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {
                totalCount
            }
            createdAt
        }
    }
    """
    user = _graphql(query, {"login": USERNAME})["data"]["user"]
    return {
        "repos":      user["repositories"]["totalCount"],
        "created_at": user["createdAt"],
    }


def get_total_contributions(created_at: str) -> int:
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
    now = datetime.datetime.now(datetime.timezone.utc)
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


# ─── Cache I/O ────────────────────────────────────────────────────────────────

CACHE_PATH = "cache/stats_cache.json"


def load_cache(path: str = CACHE_PATH) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(data: dict, path: str = CACHE_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ─── SVG generator ────────────────────────────────────────────────────────────

def generate_svg(stats: dict, theme: str) -> str:
    """
    A borderless typographic plate: tracked-out name, quiet subtitle, one
    hairline rule, and a single justified metric line. No background fill —
    the README's own background shows through in either theme.
    """
    c = DARK if theme == "dark" else LIGHT
    W, H = 600, 128

    SANS = (
        "-apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, "
        "Helvetica, Arial, sans-serif"
    )
    MONO = (
        "ui-monospace, SFMono-Regular, Menlo, "
        "&quot;Courier New&quot;, monospace"
    )

    metrics = (
        f"{stats['repos']} repositories"
        f"   ·   {stats['contributions']:,} contributions "
        f"since {stats['since']}"
    )
    stamp = f"updated {stats['updated_at']}"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" \
width="{W}" height="{H}" role="img" aria-labelledby="plate-title">
  <title id="plate-title">Swastik — {xml_escape(SUBTITLE)}. \
{xml_escape(metrics)}.</title>
  <text x="1" y="38" font-family="{SANS}" font-size="28" font-weight="400" \
letter-spacing="7" fill="{c['primary']}">SWASTIK</text>
  <text x="1" y="62" font-family="{SANS}" font-size="12.5" \
fill="{c['muted']}">{xml_escape(SUBTITLE)}</text>
  <line x1="1" y1="86" x2="{W - 1}" y2="86" stroke="{c['rule']}" \
stroke-width="1"/>
  <text x="1" y="110" font-family="{MONO}" font-size="11.5" \
fill="{c['muted']}">{xml_escape(metrics)}</text>
  <text x="{W - 1}" y="110" text-anchor="end" font-family="{MONO}" \
font-size="11.5" fill="{c['muted']}">{xml_escape(stamp)}</text>
</svg>
"""


def save_svg(content: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    cache = load_cache()

    print("[*] fetching github stats...")
    try:
        user_stats    = get_user_stats()
        contributions = get_total_contributions(user_stats["created_at"])

        cache = {"_user_stats": user_stats, "_contributions": contributions}

    except Exception as exc:
        print(f"[!] API call failed: {exc} — falling back to cache")

        cached_user = cache.get("_user_stats") or {}
        user_stats = {
            "repos":      cached_user.get("repos", 0),
            "created_at": cached_user.get("created_at", "2024-06-24T00:00:00Z"),
        }
        contributions = cache.get("_contributions", 0)

    save_cache(cache)

    created = datetime.datetime.fromisoformat(
        user_stats["created_at"].replace("Z", "+00:00")
    )
    now = datetime.datetime.now(datetime.timezone.utc)

    stats = {
        "repos":         user_stats["repos"],
        "contributions": contributions,
        "since":         created.strftime("%B %Y"),
        "updated_at":    now.strftime("%d %b %Y"),
    }

    print("[*] generating svgs...")
    save_svg(generate_svg(stats, "dark"),  "output/profile.svg")
    save_svg(generate_svg(stats, "light"), "output/profile_light.svg")
    print("[+] done.")


if __name__ == "__main__":
    main()
