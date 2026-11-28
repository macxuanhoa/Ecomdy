# Developer Operations Matrix

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Scope:** Controlled documentation/harness work on the approved branch. Product implementation remains gated by `VS01-G6`.<br>
**Rule:** A documented procedure is not an automated capability. Proposed CLI commands are not supported until implemented and tested.

## Skill and tool map

| Resource | Current status | How to use | Limitation |
|---|---|---|---|
| `.harness/skills/scoped-task/SKILL.md` | Physical instruction file; manually readable | Read before a scoped change; apply its contract/verification guidance | No skill loader or executor |
| `.harness/skills/debug/SKILL.md` | Physical instruction file; manually readable | Read when reproducing or fixing a failure | No automatic diagnosis |
| `.harness/skills/diagram/SKILL.md` | Physical instruction file; manually readable | Read before changing diagram sources/metadata | No renderer or visual acceptance |
| Diagram Design Plugin 2.6.131 | User-level installation; exposed in the audit session | Invoke through the Qoder Skill catalog; use only reviewed extractor/generation procedures | Not inherited by clones; no repository CI dependency |
| `.harness/harness.py init` | Implemented and tested | Scaffold missing files without clobbering existing files | May append missing `.gitignore` rules |
| `.harness/harness.py ingest` | Implemented and tested | Inventory/hash `<project>/docs/00-original` | No content extraction or source approval |
| `.harness/harness.py doctor` | Implemented and tested | Report environment in advisory mode | No readiness gate or agent execution |
| `.harness/harness.py route` | Implemented and tested | Select the unique most-specific explicit route and write an explainable advisory JSON record | No task execution, recipe compilation, model routing or limit enforcement |
| `.harness/harness.py capabilities` | Implemented and tested | Report registered/installed/configured/session/smoke/integrated/verified states independently | Local artifact inspection only; not a complete host catalog or OS sandbox |
| `scripts/validate.py` | Implemented and tested | Validate local Markdown links, diagram metadata/listings and static assets | No Mermaid grammar/render/semantic validation |
| `.harness/scripts/validate.py` | Implemented and tested | Validate harness docs/diagram metadata/assets | No role/skill execution |
| `.harness/scripts/validate_techniques.py` | Implemented and tested | Validate technique cards and references | No installation or effectiveness claim |
| `.harness/scripts/validate_routing.py` | Implemented and tested | Validate profiles, routes and recipes | No runtime routing or execution |
| `.harness/scripts/validate_execution.py` | Implemented and tested | Validate trace/checkpoint state semantics | No automatic capture or resume |
| `.harness/scripts/validate_tool_manifest.py` | Implemented and tested | Validate 20 candidate records, lifecycle semantics, procedures and `NOT_RUN` research commands | No installation, activation or candidate effectiveness claim |
| `scripts/render_diagrams.py` | Implemented; runtime depends on Graphviz | Regenerate DOT assets when an approved Graphviz is installed | Graphviz is absent in the audited environment |
| Jira | Blocked | Use stable internal IDs and import-ready CSV until access is authorized | No real Jira keys/issues exist |

## 1. Receive and understand a task

- **What:** Confirm objective, stable ID, scope, dependencies, acceptance checks, budget and stop conditions.
- **Why:** Prevent scope drift, duplicate work and unauthorized implementation.
- **How:** Read handoff/status/blockers, relevant requirement/module/workflow and `.harness/templates/task.json`; write a task contract.
- **Tool:** Git, documentation portal, task template.
- **Skill:** `scoped-task` instruction.
- **Harness:** Task template only; no executor enforces it.
- **Status:** Manual procedure; Jira intake blocked.
- **Expected:** A reviewable Ready task or an explicit Blocked decision.
- **Verify:** Contract contains allowed/forbidden paths, exact commands, reviewer role and rollback.
- **Recovery:** Mark Blocked and request the missing owner/source/contract decision; do not invent it.
- **Next:** Create a task branch only after scope is approved.

## 2. Configure the coding agent

- **What:** Load repository rules and constrain the agent to the approved task.
- **Why:** External content and tool output are untrusted; unbounded agents can exceed authority.
- **How:** Read `AGENTS.md`, relevant specs and only task-scoped skills; disable unapproved automation/paid calls.
- **Tool:** Qoder session, `AGENTS.md`, repository map.
- **Skill:** `scoped-task`; optional user-level Diagram Design for diagrams.
- **Harness:** Config/template are descriptive; budgets and scope are not enforced.
- **Status:** Manual configuration.
- **Expected:** Agent can state scope, evidence rules and stop conditions.
- **Verify:** Ask for a short restatement of allowed paths, checks and forbidden actions before editing.
- **Recovery:** Reset context to the task contract; remove unrelated files from scope.
- **Next:** Inspect existing implementation before changing files.

## 3. Create a task branch

- **What:** Create one short-lived branch from the approved base.
- **Why:** Isolate review and avoid direct changes to `main`.
- **How:** Use `docs/phase-0-acceptance` until PR #1 merges; then use current `main`. Name `<type>/<jira-key>-<short-kebab>` only when a real Jira key exists.
- **Tool:** Git.
- **Skill:** `scoped-task`.
- **Harness:** None.
- **Status:** Manual; current PR #2 is stacked on PR #1.
- **Expected:** Clean task branch with no unrelated work.
- **Verify:** `git status --short --branch --untracked-files=all` and `git log --oneline --decorate -3`.
- **Recovery:** Do not force-push or discard work; coordinate a safe branch reset only with the owner.
- **Next:** Implement the smallest reviewed change.

## 4. Implement a scoped change

- **What:** Modify only approved files and preserve provenance/contracts.
- **Why:** Keep diffs reviewable and avoid breaking dependent work.
- **How:** Inspect existing behavior, reuse valid artifacts, update source before rendered output, record assumptions.
- **Tool:** Editor, Git diff, relevant validator.
- **Skill:** `scoped-task`; `diagram` for diagram changes.
- **Harness:** No file-scope enforcement yet.
- **Status:** Manual.
- **Expected:** Minimal coherent diff with traceability.
- **Verify:** `git diff`, changed-path list and requirement/capability references.
- **Recovery:** Revert only the agent's own incomplete edit; preserve user work and request review if intent is unclear.
- **Next:** Run deterministic verification.

## 5. Run verification

- **What:** Execute existing checks and record exact outcomes.
- **Why:** Separate observed evidence from assumptions.
- **How:** Run product validator, harness validator, technique/routing/execution/tool-manifest validators, unit tests, compile check and task-specific checks that actually exist.
- **Tool:** Python, Git, validators.
- **Skill:** `scoped-task`.
- **Harness:** Validators/tests are implemented; no generic verification runner.
- **Status:** Automated checks exist for docs/harness only.
- **Expected:** PASS, FAIL, NOT RUN or BLOCKED with evidence.
- **Verify:** Capture command, exit code and relevant output; never mark an unrun check PASS.
- **Recovery:** Fix root cause or record the blocker; do not weaken tests or bypass hooks.
- **Next:** Review and stage the diff.

## 6. Review and stage the diff

- **What:** Stage only intended files and inspect for secrets/originals/noise.
- **Why:** Prevent accidental disclosure and unrelated commits.
- **How:** Use specific `git add -- <paths>`, then inspect staged diff and status.
- **Tool:** Git.
- **Skill:** `scoped-task`.
- **Harness:** None.
- **Status:** Manual.
- **Expected:** Staged set matches the task contract.
- **Verify:** `git diff --cached --check`, `git diff --cached --name-only`, secret/original scan.
- **Recovery:** Unstage unintended paths; do not delete unfamiliar files.
- **Next:** Commit only when authorized.

## 7. Commit safely

- **What:** Create a new commit describing why the change is needed.
- **Why:** Preserve a reviewable, recoverable history.
- **How:** Use the repository style; never amend published work, skip hooks/signing or include secrets.
- **Tool:** Git.
- **Skill:** `scoped-task`.
- **Harness:** None.
- **Status:** Manual; documentation commits are authorized for this remediation.
- **Expected:** New commit with exact hash and clean staged state.
- **Verify:** `git show --stat --oneline HEAD` and `git status --short`.
- **Recovery:** If a hook fails, fix the cause and create a new commit; do not use `--no-verify`.
- **Next:** Push/open or update the PR only when authorized.

## 8. Push and open/update a pull request

- **What:** Publish the task branch and maintain its stacked PR.
- **Why:** Enable independent review and CI without merging automatically.
- **How:** Push the approved branch; update PR #2 while PR #1 is pending; include scope, checks, risks and rollback.
- **Tool:** Git/GitHub.
- **Skill:** `scoped-task`.
- **Harness:** None.
- **Status:** Manual; push authorized for documentation remediation, merge not authorized.
- **Expected:** Remote head matches local commit; PR is reviewable.
- **Verify:** `git ls-remote`, PR API/UI head SHA, CI conclusion and requested reviewers.
- **Recovery:** Investigate rejected push/CI; never force-push a shared branch.
- **Next:** Address review and sync from the approved base.

## 9. Sync a task branch

- **What:** Update from the approved base without rewriting shared history.
- **Why:** Reduce conflicts while preserving collaborators' work.
- **How:** Fetch, inspect status, rebase only an unpublished task branch; coordinate a merge for shared branches.
- **Tool:** Git.
- **Skill:** `scoped-task`.
- **Harness:** None.
- **Status:** Manual.
- **Expected:** Branch contains approved base plus task changes.
- **Verify:** `git log --graph`, conflict-free status and rerun checks.
- **Recovery:** Resolve conflicts narrowly; never discard the user's changes or force-push shared history.
- **Next:** Re-run review/CI and update handoff.

## 10. Respond to review and CI

- **What:** Resolve findings or record an explicit rebuttal/deferral.
- **Why:** Keep quality gates and decisions visible.
- **How:** Map each finding to a change/evidence; rerun affected checks.
- **Tool:** GitHub PR, local checks.
- **Skill:** `scoped-task`; `debug` for failures.
- **Harness:** CI validates docs/harness only.
- **Status:** Manual review; no reviewers currently assigned.
- **Expected:** All findings have a traceable disposition.
- **Verify:** PR review threads, new commit hashes and current CI.
- **Recovery:** Keep PR draft/blocked if required review or governance evidence is missing.
- **Next:** Merge only through protected process after approval.

## 11. Debug and handle failure

- **What:** Reproduce, isolate one hypothesis, make a minimal fix and prove regression coverage.
- **Why:** Avoid speculative changes and hidden failures.
- **How:** Capture exact command/input/expected/actual; reduce scope; change one cause; rerun focused and regression checks.
- **Tool:** Python/Git/logs.
- **Skill:** `debug`.
- **Harness:** Doctor/tests/validators; no automatic debugger.
- **Status:** Manual.
- **Expected:** Root cause and evidence, or an explicit Blocked state.
- **Verify:** Before/after outputs and relevant tests.
- **Recovery:** Stop at retry/scope limit; request owner/vendor input rather than looping.
- **Next:** Update blocker/handoff and continue independent work.

## 12. Change a diagram

- **What:** Update source, metadata and paired artifacts without redrawing unrelated diagrams.
- **Why:** Preserve semantic provenance and avoid unverified visual drift.
- **How:** Identify diagram ID/state; edit source; validate metadata/assets; render only with approved pinned tooling; inspect output.
- **Tool:** Mermaid/DOT source, Graphviz when available, Diagram Design for reviewed generation.
- **Skill:** `diagram`; Diagram Design Skill.
- **Harness:** Validators and DOT renderer; no Mermaid renderer.
- **Status:** Source/asset checks implemented; Mermaid rendering open.
- **Expected:** Reviewed source and matching artifact, or an explicit render blocker.
- **Verify:** Parser/parity/asset checks plus full-size visual inspection when rendered.
- **Recovery:** Restore the valid source/artifact; do not claim parser success as rendering.
- **Next:** Update gallery, docs and verification evidence.

## 13. Resume or hand off

- **What:** Record observed state and next authorized action.
- **Why:** Prevent stale context and duplicated work.
- **How:** Capture branch/HEAD, PR/base/head, changed files, checks, blockers, decisions and stop conditions.
- **Tool:** Git/GitHub, handoff/status docs.
- **Skill:** `scoped-task`.
- **Harness:** Manual handoff only; no generator.
- **Status:** Manual.
- **Expected:** Another session can resume without guessing.
- **Verify:** Compare recorded SHA/status with actual Git state.
- **Recovery:** Correct stale claims immediately; preserve historical evidence separately.
- **Next:** Start the next approved task or stop at the authorization boundary.

## Automation boundary

The procedures above are intentionally manual unless a row says a check/command is implemented. `.harness/config/default.json`, task-template budgets and proposed CLI names do not enforce behavior. See the [Minimum Viable DevHarness plan](minimum-viable-harness-plan.md) for proposed automation and its acceptance gates.
