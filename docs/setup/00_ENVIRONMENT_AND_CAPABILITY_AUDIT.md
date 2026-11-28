# Environment and Capability Audit

**Audit date:** 2026-11-26 (Asia/Saigon)<br>
**Repository:** [macxuanhoa/Ecomdy](https://github.com/macxuanhoa/Ecomdy)<br>
**Audit scope:** local starter pack, public GitHub repository, available local tools, and supplied source materials.

## Findings

| Area | Observed state | Evidence / limit |
|---|---|---|
| Repository existence | Exists and is public | GitHub repository API returned `visibility: public`, `private: false`, `archived: false`. |
| Default branch and history | `main`; one existing commit, `560cf0d` (`Initial commit`) | `git ls-remote` and local fetch. Remote tree contains only `README.md` (`# Ecomdy`). |
| Local Git | Git 2.50.1; configured commit identity name `macxuanhoa` | `git --version`, local Git config. The configured email is intentionally omitted from this public audit. |
| Working branch | `setup/phase-0-audit`, tracking `origin/setup/phase-0-audit`; Phase 0 acceptance uses local `docs/phase-0-acceptance` | Remote `main` was not changed; the acceptance branch is uncommitted and has no upstream. |
| Authentication / write access | Verified | `gh` is not installed, but Git Credential Manager authenticated a branch push and authorized repository API updates. Credential values were not exposed. |
| Python | Python 3.11.9 on PATH; bundled Python runtime also available | `python --version`; bundled runtime loaded through Codex workspace dependencies. |
| Other tools | Bundled Node.js is available. Graphviz (`dot`), Poppler (`pdftoppm`), and `gh` were not found on PATH. | Command discovery. Existing rendered diagrams are present. |
| GitHub Actions dependencies | Workflow uses current major releases of official checkout and setup-python actions, with persisted checkout credentials disabled. | Release status checked against [actions/checkout](https://github.com/actions/checkout/releases) and [actions/setup-python](https://github.com/actions/setup-python/releases) on the audit date. |
| GitHub workflow result | `Validate repository` passed on the setup branch | Check run for the pushed setup commit; latest run URL is in `VERIFICATION_REPORT.md`. |
| Workflow token permissions | Repository default is read-only | Authenticated API read-back of Actions workflow permissions. |
| Repository settings | Description, five topics, seven additional labels, and two undated official-scope milestones configured | Authenticated GitHub API read-back verified values. |
| Branch protection | `main` requires a PR, up-to-date successful `validate` check from GitHub Actions, and resolved conversations; force pushes/deletions are disabled and admins are included | Authenticated read-back. Minimum approving reviews is 0 because a reviewer group has not been confirmed. |
| Security settings | Secret scanning, push protection, vulnerability alerts, Dependabot security updates, and private vulnerability reporting enabled | Authenticated GitHub API read-back; public-repository availability checked against [GitHub security feature availability](https://docs.github.com/en/code-security/getting-started/github-security-features). |
| Dependency automation | Monthly GitHub Actions version updates configured in `.github/dependabot.yml` on the setup branch | Configuration becomes active on the default branch after PR merge; security updates are enabled at repository level. |
| GitHub Projects | Not created | GraphQL `projectsV2` query returned missing `read:project` scope; current credential scopes are `gist`, `repo`, and `workflow`. Project API work requires a GitHub authorization with project access. |
| Document libraries | Bundled `pypdf`, `pdfplumber`, `openpyxl`, and Pillow are available | Module discovery and use for source extraction / image inspection. |
| Local product implementation | No application source, package manifest, or runtime configuration is present in `ecomdy-intelligence` | Full local file inventory. The repository contains proposed specifications, diagrams, bootstrap material, and a documentation validator. |
| Local harness | The supplied sibling directory `devharness-os` was adapted into `.harness/` with overwrite protection and a stronger validator. It includes a Python CLI, config, skills, docs, diagrams, templates, scripts, and tests. | Local file inventory. It remains an advisory starter and is not a product runtime dependency. Three embedded unit tests pass; standalone parity is not implemented. |
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

Local file reads/writes, Git operations, Python scripts, GitHub branch push, pull-request creation, repository metadata/settings, labels, and milestones are available and verified. GitHub CLI is unavailable, so remote updates used the existing Git Credential Manager non-interactively. No credentials were requested in chat or exposed.

## Risks and controls

1. **Public repository:** publish only reviewed project documentation and code. Keep originals, secrets, private customer data, and unapproved internal material out of Git.
2. **Existing remote history:** preserve `origin/main`; changes are isolated on `setup/phase-0-audit` and draft PR #1.
3. **Proposal / implementation drift:** mark target designs, unverified assumptions, and implemented behavior separately; do not describe the documentation scaffold as a product.
4. **External source compliance:** no real source ingestion or scheduled collection is implemented. Source access requires a future allowlist and terms review.

## Current audit state

**Verified:** remote public/readable, source materials inventoried and extracted, originals ignored; setup package commit `a08bb16` and follow-up status commit `d4584ae` are on the PR branch; push and pull-request GitHub Actions passed for both; repository metadata, security settings, labels, milestones, and `main` protection read back successfully.<br>
**Pending verification:** merge and post-merge default-branch checks, Ecomdy application behavior, owner-approved product scope, source allowlist, brand inputs, seller interviews, and Content Team feedback.

## Phase 0 recheck — 2026-11-27

The acceptance audit verified baseline `4bddc925c941979da60b1250ec4d139381776e22`, PR #1, two successful CI event runs, local validators, 3/3 embedded harness tests, two fresh clones and the 56-diagram inventory. It did not install tools, create Jira data, commit, push or merge.

Current limits at this Phase 0 snapshot: Jira access is unavailable; branch-protection/security API revalidation returned HTTP 401; 30 Mermaid-only diagrams lack local parser/render evidence; DOT/MMD parity is not reliably verified; product runtime and autonomous harness behavior are absent. The later [comprehensive audit](COMPREHENSIVE_AUDIT.md) records parser extraction at 55/56, Mermaid/DOT parity at 26/26 and static assets at 26/26, while rendering and current governance read-back remain open. See [PHASE_0_ACCEPTANCE.md](PHASE_0_ACCEPTANCE.md) and [CAPABILITY_COVERAGE.md](CAPABILITY_COVERAGE.md).
