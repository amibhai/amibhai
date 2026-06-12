# Setup

## 1. Create the GitHub profile repository

Go to **https://github.com/new** and create a repository named exactly **`amibhai`**
(the repo name must match your GitHub username exactly — that is what activates
the special profile README feature).

- Visibility: **Public**
- Do NOT initialize with a README, .gitignore, or license

## 2. Push this project to the repo

```bash
cd amibhai
git init
git add .
git commit -m "chore: initial setup"
git branch -M main
git remote add origin https://github.com/amibhai/amibhai.git
git push -u origin main
```

## 3. Create a Personal Access Token

Go to **GitHub Settings → Developer settings → Personal access tokens →
Fine-grained tokens → Generate new token**

| Field | Value |
|-------|-------|
| Token name | `profile-readme-updater` |
| Expiration | 1 year (or custom) |
| Resource owner | your account |
| Repository access | **Only select repositories** → select `amibhai` |

Repository permissions:

| Permission | Level |
|------------|-------|
| Contents | Read and Write *(commits the updated SVGs back)* |
| Metadata | Read *(required by default)* |

Account permissions:

| Permission | Level |
|------------|-------|
| Followers | Read *(to fetch follower count)* |
| Starring | Read *(to fetch star counts)* |

## 4. Add the token as a repository secret

In the `amibhai` repo:
**Settings → Secrets and variables → Actions → New repository secret**

| Field | Value |
|-------|-------|
| Name | `GH_TOKEN` |
| Value | *(paste the token you just created)* |

## 5. Trigger the first run

Go to **Actions → Update profile README → Run workflow → Run workflow**.

The workflow will:
1. Run `generate.py` to fetch your GitHub stats via the GraphQL API
2. Write `output/profile.svg` (dark) and `output/profile_light.svg` (light)
3. Cache per-repo LOC data to `cache/loc_cache.json`
4. Commit and push all three files back to the repo

After the run completes your profile card is live at **github.com/amibhai**.

## 6. Test locally

```bash
export GH_TOKEN=your_personal_access_token
pip install requests python-dateutil lxml
python generate.py
```

Generated SVGs appear in `output/`. The LOC cache is written to
`cache/loc_cache.json` and speeds up subsequent runs by skipping repos
whose HEAD commit SHA has not changed.

## Schedule

The workflow runs automatically at **00:00 UTC daily** via cron.
To change the cadence, edit the `cron:` value in
`.github/workflows/update.yml`.

## How it works

```
generate.py
  ├── get_user_stats()      GraphQL: followers, repo count, created date
  ├── get_total_stars()     GraphQL: paginated star sum across all owned repos
  ├── get_total_commits()   GraphQL: contributionsCollection looped year-by-year
  ├── get_lines_of_code()   GraphQL: commit history additions+deletions, cached
  └── generate_svg()        Pure SVG string, no external resources
        ├── output/profile.svg        dark theme
        └── output/profile_light.svg  light theme

README.md
  └── <picture> tag — GitHub switches dark/light SVG by visitor OS theme
```
