# Verification Report

**Date:** 2026-11-26 (Asia/Saigon)<br>
**Snapshot commit:** `087c27e554e57039af0f9c74e0a8bb09d6c58372`<br>
**Status:** Local checks, independent review, push, and remote CI pass for the bundled-harness setup commit. Draft PR #1 remains open; no merge or product tests are claimed.

| Check | Command / method | Result |
|---|---|---|
| Git installed | `git --version` | PASS — `git version 2.50.1.windows.1` |
| Python installed | `python --version` | PASS — Python 3.11.9 |
| GitHub CLI | `gh --version`, `gh auth status` | NOT INSTALLED — Git Credential Manager still provided authenticated push/API access |
| Remote read | `git ls-remote --heads https://github.com/macxuanhoa/Ecomdy.git` | PASS — `main` at `560cf0d2ecaf862749edbe9b8823eebc4e0327a0` |
| Repository metadata | GitHub public repository API read | PASS — public, not archived, default branch `main` |
| History fetch | `git fetch origin main` | PASS — fetched one initial commit |
| Local branch | `git switch -c setup/phase-0-audit origin/main` | PASS |
| Branch push | `git push origin setup/phase-0-audit` | PASS — setup commit `087c27e554e57039af0f9c74e0a8bb09d6c58372` is on the remote branch |
| Draft pull request | GitHub API read-back | PASS — [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1), open, draft, unmerged; head `087c27e`, base `main` at `560cf0d` |
| Baseline GitHub Actions | Check run `Validate repository / validate` | PASS — conclusion `success`; [run 45841280241](https://github.com/macxuanhoa/Ecomdy/actions/runs/45841280241) |
| Current setup commit GitHub Actions | Push and pull-request events for `087c27e` | PASS — both `Validate repository` runs completed successfully: [push](https://github.com/macxuanhoa/Ecomdy/actions/runs/45846988006), [pull request](https://github.com/macxuanhoa/Ecomdy/actions/runs/45847001038) |
| Repository metadata | Authenticated GitHub API read-back | PASS — description, 5 topics, 7 project labels, 2 undated challenge milestones |
| `main` protection | Authenticated branch-protection API read-back | PASS — PR required, strict `validate` check from GitHub Actions required, conversation resolution required, admins enforced, force-push/deletion disabled, approvals required: 0 |
| Security settings | Authenticated GitHub API read-back | PASS — secret scanning, push protection, vulnerability alerts, Dependabot security updates, and private vulnerability reporting enabled |
| Dependabot version updates | `.github/dependabot.yml` | CONFIGURED IN PR — monthly GitHub Actions updates; activates after merge |
| GitHub Projects API | GraphQL `projectsV2` read query | BLOCKED — current token scopes are `gist`, `repo`, `workflow`; Projects query requires `read:project`; no board was created |
| Original source exclusion | `git check-ignore -v docs/00-original/master-blueprint.pdf` and `.harness/docs/00-original/source.pdf` | PASS — source files in both paths are ignored; staged originals count is zero |
| Original source hashes | SHA-256 compared with `docs/source-manifest.json` | PASS — all four source-file hashes match |
| PDF source read | `pdfplumber` extraction | PASS — 7-page and 34-page files extracted |
| Workbook source read | `openpyxl` | PASS — both sheets extracted |
| Image source read | Pillow metadata + visual inspection | PASS — 1017×856 image inspected |
| Diagram render review | Contact sheets of 14 Ecomdy and 12 DevHarness existing PNG diagrams | PASS — no obvious clipping at overview scale; semantic review remains limited to proposed target designs. Fresh rendering not performed because Graphviz is unavailable. |
| JSON syntax | Python `json.loads` on `project-profile.json` and `docs/source-manifest.json` | PASS — exit code 0 |
| YAML syntax | `yaml.safe_load` for `.github/workflows/validate.yml`, `.github/ISSUE_TEMPLATE/task.yml`, and `.github/dependabot.yml` | PASS — 3 files parsed; exit code 0 |
| Product and harness docs/diagram validation | `python scripts/validate.py`; `python .harness/scripts/validate.py` | PASS — both print `Validation: PASS`; exit code 0 |
| Staged diff whitespace | `git diff --cached --check` | PASS — exit code 0 |
| Credential-pattern scan | Python scan over `git ls-files --cached --others --exclude-standard`; ignored originals excluded by Git | PASS — zero matches for common token/private-key patterns; not a full secret scanner |
| DevHarness OS unit tests | `python -m unittest discover -s .harness/tests -p "test_*.py" -v` | PASS — 3 tests, exit code 0, including preservation of existing generated outputs unless `--overwrite` is set |
| Ecomdy application tests | No Ecomdy `tests/` directory or application code | NOT APPLICABLE — no product implementation supplied |
| Diagram rendering | `dot` availability check | NOT RUN — Graphviz is not installed / not on PATH; existing SVG/PNG files are present |
| Independent review | Read-only reviewer of setup docs and source-backed claims | PASS with one correction — workbook list items share a single cell; citations now use cell coordinate plus item number. |
| Current package review | Read-only independent review of the harness code/docs, source boundaries, overwrite safety, and commands | PASS — two documentation findings corrected; no remaining blocker |
| Current setup commit push / CI | Git push + GitHub Actions API read-back | PASS — PR head points to `087c27e`; both events succeeded |
| Merge / post-merge check | Not performed | PENDING — draft PR awaits owner review and merge |

No application tests or deployment checks are reported as passing. Markdown validation checks local targets and diagram asset presence, not external links or semantic correctness of diagrams.
