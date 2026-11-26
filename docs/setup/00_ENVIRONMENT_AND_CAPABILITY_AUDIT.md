# Environment and Capability Audit

**Audit date:** 2026-11-26 (Asia/Saigon)<br>
**Repository:** [macxuanhoa/Ecomdy](https://github.com/macxuanhoa/Ecomdy)<br>
**Audit scope:** local starter pack, public GitHub repository, available local tools, and supplied source materials.

## Findings

| Area | Observed state | Evidence / limit |
|---|---|---|
| Repository existence | Exists and is public | GitHub repository API returned `visibility: public`, `private: false`, `archived: false`. |
| Default branch and history | `main`; one existing commit, `560cf0d` (`Initial commit`) | `git ls-remote` and local fetch. Remote tree contains only `README.md` (`# Ecomdy`). |
| Local Git | Git 2.50.1; configured commit identity `macxuanhoa` / `macxuanhoa211002@gmail.com` | `git --version`, local Git config. |
| Working branch | `setup/phase-0-audit`, tracking `origin/main` | Created after fetching remote history; remote `main` was not changed. |
| Authentication / write access | Not verified | GitHub CLI (`gh`) is not installed. Anonymous read/fetch works. A successful authenticated push or API write has not been observed. |
| Python | Python 3.11.9 on PATH; bundled Python runtime also available | `python --version`; bundled runtime loaded through Codex workspace dependencies. |
| Other tools | Bundled Node.js is available. Graphviz (`dot`), Poppler (`pdftoppm`), and `gh` were not found on PATH. | Command discovery. Existing rendered diagrams are present. |
| GitHub Actions dependencies | Workflow uses current major releases of official checkout and setup-python actions, with persisted checkout credentials disabled. | Release status checked against [actions/checkout](https://github.com/actions/checkout/releases) and [actions/setup-python](https://github.com/actions/setup-python/releases) on the audit date. |
| Document libraries | Bundled `pypdf`, `pdfplumber`, `openpyxl`, and Pillow are available | Module discovery and use for source extraction / image inspection. |
| Local product implementation | No application source, package manifest, or runtime configuration is present in `ecomdy-intelligence` | Full local file inventory. The repository contains proposed specifications, diagrams, bootstrap material, and a documentation validator. |
| Local harness | A separate sibling directory `devharness-os` contains a Python CLI, config, skills, docs, diagrams, tests, and CI. It is not currently part of this Ecomdy Git repository. | Local file inventory. No claim is made here about its test result. |
| Inputs | Two PDFs (41 pages total), one two-sheet XLSX, one JPG note image, and source README | Both PDFs and both workbook sheets were text-extracted; the JPG was visually inspected. The source README says originals are ignored by Git. |
| Input publication | Original files are excluded by `docs/00-original/*`; only the README is re-included | Verified with `git check-ignore`. The remote is public, so original source files remain local. |
| Attachments in chat | No separate ZIP or additional file attachment was present in the available local input directory | The extracted starter pack and its `docs/00-original` materials were inspected. |

## Verified input interpretation

- The Challenge 2 workbook is the source for mandatory product requirements and discipline tasks. These are registered in `docs/01-requirements.md` and remain open until implementation or validation evidence exists.
- The master blueprint is a **proposed target architecture**, not a description of deployed software. Its illustrative priorities, stack, schedules, and scores remain proposals.
- The business workstream PDF explicitly labels additional work packages and example financial assumptions as proposed; its example financial values are not Ecomdy data.
- The JPG contains additional product directions (social trends, regional relevance, database-first collection, task-based model selection, and a plain-text assistant). They are guidance, not official Challenge 2 requirements.
- Seller interviews, Content Team feedback, Ecomdy source allowlist, brand guidance, previously published articles, and measured productivity results are not present as evidence in the input set.

## Capability and permission boundary

Local file reads/writes, Git operations, Python scripts, and public HTTP reads are available. Creating a branch locally is verified. Remote GitHub write access, repository settings changes, GitHub labels/milestones/projects, and pull-request creation remain unverified because `gh` is unavailable and no authenticated API action has succeeded. No credentials were requested or exposed.

## Risks and controls

1. **Public repository:** publish only reviewed project documentation and code. Keep originals, secrets, private customer data, and unapproved internal material out of Git.
2. **Existing remote history:** preserve `origin/main`; work on `setup/phase-0-audit` and use a pull request if authenticated write access is available.
3. **Proposal / implementation drift:** mark target designs, unverified assumptions, and implemented behavior separately; do not describe the documentation scaffold as a product.
4. **External source compliance:** no real source ingestion or scheduled collection is implemented. Source access requires a future allowlist and terms review.

## Current audit state

**Verified:** remote public/readable, branch/history fetched, local working branch created, source materials inventoried and extracted, originals ignored, available local capabilities inspected.<br>
**Pending verification:** authenticated push, PR creation, remote settings, full CI run on GitHub, complete harness test baseline, and any Ecomdy application behavior.
