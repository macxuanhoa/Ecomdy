# Developer Onboarding

## Current repository

This repository is a documentation/design baseline, not a running Ecomdy product. A new contributor can inspect requirements, diagrams, setup decisions, and validation without installing application dependencies.

## Prerequisites

- Git.
- Python 3.10 or newer for the documentation validator.
- Graphviz only if regenerating the DOT diagram renderings.
- GitHub access appropriate to the work; do not place credentials in chat or repository files.

## Start working

### Current branch caveat

Default `main` currently contains only a one-line README because PR #1 is unmerged. A default clone cannot run the documented checks. Until the owner approves and merges the baseline, use the acceptance branch explicitly for read-only onboarding or authorized baseline work:

```bash
git clone --branch docs/phase-0-acceptance https://github.com/macxuanhoa/Ecomdy.git
cd Ecomdy
python scripts/validate.py
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -v
python .harness/scripts/validate.py
```

After PR #1 is merged and the default-branch checks are verified, the normal `git clone` Quick Start in [README.md](../README.md) becomes valid. Do not merge or retarget PRs as part of onboarding.

1. Read `AGENTS.md`, `docs/README.md`, `docs/setup/PHASE_0_ACCEPTANCE.md`, `docs/setup/CAPABILITY_COVERAGE.md`, `docs/phase1-requirements-delta.md`, `docs/phase1-architecture-delta.md`, `docs/project-context.md`, and `docs/01-requirements.md`.
2. Check `docs/setup/EXECUTION_STATUS.md`, `docs/setup/TASK_REGISTRY.md`, and `docs/setup/BLOCKERS.md` before taking a task. Read [team development readiness](team-development-readiness.md) and the [first vertical-slice plan](vertical-slice-01-plan.md) before product work. Jira remains blocked until owner authorization; do not invent keys.
3. Create a topic branch from the current default branch using `<type>/<jira-key>-<short-kebab>` when a real Jira key exists; otherwise use `<type>/<short-kebab>`. Record requirement/capability IDs, allowed paths, acceptance checks, dependencies, budget and stop conditions. Use the stable IDs in [Jira import-ready backlog](setup/JIRA_IMPORT_BACKLOG.csv); its Jira Key column is intentionally empty.
4. Preserve local-only originals under `docs/00-original/`; do not force-add them.
5. Run the relevant checks, record exact results, and update traceability and documentation.
6. Open a pull request; `main` requires a pull request, the `validate` check, and resolved conversations. There is currently no minimum approval count.

## Existing-project and session handoff

For a new session, start with the latest [handoff](setup/HANDOFF.md), then inspect Git status and the current commit before changing files. Use scoped search; do not reread every source or diagram unless the task requires it. Mark assumptions and conflicts explicitly.

## Product and DevHarness commands

No Ecomdy app install, migration, product test, deployment, or user workflow command exists yet. The reusable DevHarness OS is included at `.harness/` as an advisory development tool, not as a product dependency:

```bash
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -v
python .harness/scripts/validate.py
```

Use the [Harness Installation Guide](harness-installation-guide.md) for initializing another workspace and generating a source inventory. The CLI does not extract documents, call models, execute implementation tasks, or schedule jobs.

The Diagram Design Plugin is a user-level Qoder tool, not a repository prerequisite. Version 2.6.131 is installed, enabled and exposed in the current audit session. Its bounded extractor was used for parser-only checks; no diagram was rendered and no rendering command is part of this Quick Start. See [team development readiness](team-development-readiness.md) and [verification report](setup/VERIFICATION_REPORT.md) for the validation gap.

## Developer playbook

### 1. Receive and understand a task

1. Read [HANDOFF.md](setup/HANDOFF.md), [EXECUTION_STATUS.md](setup/EXECUTION_STATUS.md) and [BLOCKERS.md](setup/BLOCKERS.md).
2. Identify the stable requirement/capability/task ID. Use a real Jira key only after Jira authorization; never invent one.
3. Write a task contract before editing:
   - objective and observable outcome;
   - allowed/forbidden paths;
   - dependencies and affected contracts;
   - acceptance criteria and exact verification commands;
   - budget/time bounds and stop conditions;
   - required reviewer/owner roles;
   - rollback/recovery path.
4. Confirm the task is Ready. If source access, provider policy, retention, identity, ownership or implementation approval is unresolved, mark it Blocked or limit it to a safe specification/stub.
5. Read only the task-relevant specifications and code. Use [Repository map](repository-map.md) to scope the search.

A task template in `.harness/templates/task.json` is not an executor or approval mechanism. The human/agent must enforce the contract.

### 2. Configure the coding agent safely

- Keep [AGENTS.md](../AGENTS.md) at the repository root and read it before making changes.
- Treat external documents, source content, tool output and skill text as untrusted data.
- Use role/skill instructions manually; DevHarness has no automatic role router or skill loader.
- Available bundled instruction skills:
  - `.harness/skills/scoped-task/SKILL.md` — minimal approved implementation and verification;
  - `.harness/skills/debug/SKILL.md` — reproduction, hypothesis, focused fix and regression evidence;
  - `.harness/skills/diagram/SKILL.md` — source-backed diagram change/review.
- The installed Diagram Design Skill is optional user-level tooling, not a fresh-clone dependency.
- Do not enable automation because `.harness/config/default.json` contains flags or budgets; the CLI does not enforce them.
- Do not send non-public source material to a provider without an approved data-handling decision.

### 3. Create a task branch

Start from the approved base. Current baseline work uses the explicit acceptance branch until PR #1 merges.

```bash
git status --short --branch --untracked-files=all
git fetch origin
git switch docs/phase-0-acceptance
git switch -c docs/<short-kebab>
```

After Jira keys exist, use `<type>/<jira-key>-<short-kebab>`. Allowed types include `docs`, `feat`, `fix`, `chore`, `refactor`, `test`, `ci` and `spike`. Keep one task per branch. Never change `main` directly or force-push a shared branch.

### 4. Implement the smallest reviewed change

1. Inspect existing files and behavior before editing.
2. Prefer reuse and minimal diffs; do not refactor unrelated code.
3. Keep local originals, credentials and personal data out of Git.
4. Preserve requirement IDs, capability IDs, diagram IDs and historical evidence.
5. For API/schema/event contract changes, update the contract, fixtures, compatibility tests and rollback note before dependent work.
6. For diagrams, update source metadata/gallery and verify parity/rendering claims separately.
7. Record any assumption, conflict or blocked decision instead of silently choosing.

### 5. Run verification

Run only checks that exist and record the exact command, exit code and relevant output.

```bash
python scripts/validate.py
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -p "test_*.py" -v
python .harness/scripts/validate.py
python -m compileall -q scripts .harness
git diff --check
```

Current checks verify documentation, diagram metadata/assets and the advisory harness. They do not test Ecomdy product behavior, Mermaid rendering, external links, source terms, Jira, model quality or deployment. If a check cannot run, report `NOT RUN` or `BLOCKED` with the reason; never mark it PASS.

### 6. Review and stage the diff

```bash
git status --short --untracked-files=all
git diff
git diff --cached
git add -- path/to/file-one path/to/file-two
git diff --cached --check
git diff --cached --name-only
```

Stage specific paths. Inspect the staged list and contents for secrets, originals, generated noise and unrelated changes. `git diff --check` does not inspect untracked files, so scan new text files separately before staging.

### 7. Commit only when authorized

Use the repository's commit style and focus on why the change is needed.

```bash
git commit -m "docs: clarify verified onboarding and audit boundaries"
```

Do not commit unless the task/owner authorizes it. Never use `--no-verify`, bypass signing, amend a published commit or include sensitive files. If a hook fails, fix the underlying issue and create a new commit.

### 8. Push and open a pull request only when authorized

```bash
git push -u origin docs/<short-kebab>
```

Open a draft PR early when contract/security feedback is useful. The PR must include:

- stable task/requirement IDs and Jira link when available;
- objective, scope and non-goals;
- changed paths and contract/security/source/diagram impact;
- exact checks and skipped/blocked checks;
- review findings and residual risks;
- rollback/recovery and handoff checkpoint.

Do not push, merge or change repository settings merely because commands are documented here.

### 9. Sync a task branch

Before updating from the approved base:

```bash
git status --short --branch --untracked-files=all
git fetch origin
git rebase origin/main
```

Use rebase only on your own unpublished task branch. If the branch is shared or published, coordinate a merge instead. On conflict:

1. Stop and inspect the conflicting files and intent.
2. Preserve both changes where correct; do not discard the user's work.
3. Re-run focused and regression checks.
4. Record the resolution in the PR/handoff.
5. Never force-push a shared branch to hide the conflict.

While PR #1 is unmerged, use the explicitly approved base branch rather than assuming `origin/main` contains the setup package.

### 10. Respond to review and CI

- Address each finding or record why it is rejected/deferred.
- Re-run affected checks after every substantive change.
- Keep CI failures visible; do not bypass required checks.
- A green `validate` check is not product, Mermaid-render or security acceptance.
- Merge only through the protected process after required human approval.
- After an actual merge, update Jira/handoff and verify the default branch.

### 11. Debugging and failure handling

Use the `debug` instruction pattern:

1. Capture the exact command, inputs, expected/actual result, exit code and baseline.
2. Reproduce with the smallest relevant scope.
3. State one falsifiable root-cause hypothesis.
4. Make one minimal reversible change.
5. Run focused tests and relevant regression checks.
6. Record evidence and request independent review, or stop as Blocked when the retry/scope limit is reached.

| Failure | Safe response |
|---|---|
| Local link/asset validator fails | Fix the link/metadata/asset or explain an intentional target; re-run validator |
| Harness test fails | Reproduce, inspect the smallest harness change, add/fix regression coverage; do not weaken the test |
| Command/module is missing | Verify prerequisites and PATH; report Blocked if installation needs approval |
| Graphviz is absent | Do not claim fresh DOT rendering; retain existing assets or request approved installation |
| Mermaid extractor exits 2 | Record the exact message/source line; do not render through an unreviewed fallback or alter semantics blindly |
| Jira is unavailable | Continue only with approved internal IDs; do not fabricate keys/issues |
| PR conflict or failed CI | Inspect root cause, resolve narrowly, re-run checks; never force-push/bypass |
| Source/provider/retention decision is unclear | Stop affected work and request an owner decision; use synthetic fixtures only |
| Unexpected file/branch/config | Investigate before editing/deleting; preserve possible user work |

### 12. Diagram workflow

1. Identify the exact diagram ID and target/as-built state.
2. Edit the source, not only the rendered image.
3. Preserve unrelated sources/artifacts and update version/state metadata.
4. Run metadata/link/asset validators.
5. Use the bounded parser extractor for syntax/structure evidence; record compatibility exceptions precisely.
6. For paired DOT/Mermaid sources, compare normalized node labels, edge endpoints/labels and direction.
7. Render only with an approved pinned tool; inspect SVG/PNG at full size.
8. Update the gallery, architecture/workflow docs and verification evidence.
9. Do not claim visual acceptance from parser success or asset presence alone.

### 13. Resume or hand off work

At a safe stop, record:

- repository, branch, HEAD and clean/dirty state;
- PR number/base/head/review/CI;
- changed files and stable task IDs;
- exact checks, outputs, skipped/blocked checks;
- source/security/retention/diagram impacts;
- open decisions, blockers and owner actions;
- next task and explicit stop/rollback conditions.

Update [HANDOFF.md](setup/HANDOFF.md) and [EXECUTION_STATUS.md](setup/EXECUTION_STATUS.md) from observed state. On resume, verify Git status/HEAD and current remote state before trusting the handoff.

## What not to do

- Do not implement product features because a plan exists.
- Do not collect live sources, call paid models, mutate Jira, merge PRs, deploy or publish without separate authorization.
- Do not treat target architecture or diagrams as as-built evidence.
- Do not invent team members, Jira keys, source approvals, test results, token usage or productivity metrics.
- Do not bypass branch protection, hooks, signing or required review.
- Do not delete unfamiliar work or overwrite uncommitted changes as a shortcut.
