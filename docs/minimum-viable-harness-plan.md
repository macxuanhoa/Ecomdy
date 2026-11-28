# Minimum Viable DevHarness Implementation Plan

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Status:** Proposal for owner approval. No new harness command is implemented by this document.<br>
**Goal:** Add the smallest deterministic controls that improve team delivery without making the full harness a prerequisite for Ecomdy product work.

## 1. Scope and non-goals

### In scope

- Reproducible bootstrap and environment checks.
- Task-scoped context loading/compilation with provenance and bounds.
- Skill discovery and usage mapping.
- File-scope validation against a task contract.
- Allowlisted verification execution with timeouts and captured evidence.
- Deterministic session handoff generation.
- Diagram validation/rendering adapters behind an approved tool manifest.

### Explicitly out of scope for the first release

- Autonomous loops, self-improvement, general model routing and multi-agent orchestration.
- Scheduler/worker, always-on services and automatic publication.
- Paid model calls, external crawling and Jira mutation before separate authorization.
- A generic shell executor, arbitrary code execution or secret-bearing context packs.
- Repository-wide semantic intelligence before a measured need exists.

## 2. Current reusable baseline

| Existing asset | Verified behavior | Reuse boundary |
|---|---|---|
| `.harness/harness.py init` | Preserves existing files, creates missing starter files, appends missing ignore rules | Extend with deterministic checks; do not weaken overwrite protection |
| `.harness/harness.py ingest` | Inventories/hashes regular non-symlink files under `<project>/docs/00-original` | Reuse path/hash helpers; it is not a content extractor |
| `.harness/harness.py doctor` | Reports Python/Git/Graphviz/GitHub CLI availability | Keep advisory unless a task explicitly requires a tool |
| `.harness/templates/task.json` | Stores scope, dependencies, checks, budgets and approval fields | Treat as input schema; no executor currently enforces it |
| `.harness/skills/` | Three manually readable instruction files | Build a catalogue without claiming automatic loading |
| `scripts/validate.py` and `.harness/scripts/validate.py` | Local link/metadata/asset checks | Reuse as verification commands; no Mermaid renderer exists |
| `.harness/tests/test_harness.py` | Three passing starter tests | Add deterministic tests beside each approved capability |
| `docs/setup/HANDOFF.md` | Manual checkpoint structure | Generate only from observed Git/task/check state |

## 3. Security and execution invariants

1. Python standard library remains the default runtime.
2. No shell strings: verification commands are structured arrays with an executable allowlist.
3. Resolve and check paths; reject traversal, symlinks and paths outside the approved project/task scope.
4. Enforce file-count, byte, output, runtime and retry limits before execution.
5. Redact common secret patterns from context packs, logs and handoff output.
6. Network access is off by default; Jira/model/source adapters require explicit configuration and authorization.
7. Generated files refuse overwrite unless the caller passes an explicit opt-in.
8. Every result records command/tool version, inputs, exit code, timestamps and limitations; missing metrics remain `unknown`.

## 4. P0 capabilities

All CLI examples in this section are **PROPOSED — NOT IMPLEMENTED**.

### H0-01 — Reproducible bootstrap

- **User problem:** New workspaces can drift or accidentally overwrite local work.
- **Reuse:** `initialize`, `doctor`, `.gitignore` handling and existing tests.
- **Proposed implementation:** Add a check-only bootstrap mode, deterministic file manifest and prerequisite report; keep current non-clobbering behavior.
- **Dependencies:** None.
- **Proposed CLI:** `python .harness/harness.py bootstrap --project PATH --check`
- **Acceptance tests:**
  - Empty project creates the expected starter set with stable relative paths.
  - Second run changes no existing file and adds no duplicate ignore rule.
  - Pre-existing sentinel file remains byte-identical.
  - Missing Python/Git is reported without stack trace or mutation.
  - Path traversal and symlink project paths are rejected.
- **Security:** No network, no package installation, no credential discovery.
- **Effort:** 1–2 engineer-days.
- **Priority:** P0 / first.
- **Team impact:** Makes onboarding reproducible and reviewable.

### H0-02 — Project context loading

- **User problem:** Agents read too much, miss authority boundaries or ingest local-only originals.
- **Reuse:** Repository map, source manifest, task template and `ingest` path/hash helpers.
- **Proposed implementation:** Load an explicit allowlist of task-relevant tracked files with path, SHA-256, size, authority and reason; exclude ignored originals by default.
- **Dependencies:** H0-01 path/manifest helpers.
- **Proposed CLI:** `python .harness/harness.py context load --task PATH --max-files 40 --max-bytes 262144 --output PATH`
- **Acceptance tests:**
  - Only task-listed files are loaded; order is stable across runs.
  - Ignored `docs/00-original/*` and `.harness/docs/00-original/*` are excluded unless explicitly approved.
  - File-count/byte ceiling fails closed with a deterministic error.
  - Changed file hash invalidates the saved context.
  - Secret-pattern fixture is redacted and reported.
- **Security:** Local-only output; no provider upload; provenance required for every loaded file.
- **Effort:** 2–3 engineer-days.
- **Priority:** P0.
- **Team impact:** Reduces irrelevant context and protects source boundaries.

### H0-03 — Task-specific context compilation

- **User problem:** A loaded file list is not a concise, reviewable agent brief.
- **Reuse:** Task contract fields, requirement/module/workflow IDs and H0-02 manifest.
- **Proposed implementation:** Compile objective, constraints, relevant excerpts, open decisions, checks and stop conditions into a bounded JSON/Markdown pack with provenance.
- **Dependencies:** H0-02.
- **Proposed CLI:** `python .harness/harness.py context compile --task PATH --output PATH`
- **Acceptance tests:**
  - Same task/input hashes produce byte-identical output.
  - Pack includes objective, allowed/forbidden paths, dependencies, checks, budget and stop conditions.
  - Excerpts never exceed configured byte/share limits.
  - Missing requirement ID or acceptance command produces a validation error.
  - No target design is labelled implemented.
- **Security:** Deterministic summarization only; no model call; redaction inherited from H0-02.
- **Effort:** 3–4 engineer-days.
- **Priority:** P0.
- **Team impact:** Gives agents and reviewers the same scoped brief.

### H0-04 — Skill discovery and usage mapping

- **User problem:** Proposed skills are confused with installed/executable skills.
- **Reuse:** `.harness/skills/`, `.harness/registry/capabilities.json` and technology evaluation.
- **Proposed implementation:** Catalogue physical instruction files separately from proposed packs; map task types to manual guidance and installed user-level tools without executing them.
- **Dependencies:** H0-03 task type.
- **Proposed CLI:** `python .harness/harness.py skills map --task PATH --format json`
- **Acceptance tests:**
  - Reports exactly three physical harness instruction files in the current baseline.
  - Proposed catalogue entries are marked `proposed`, never `installed`.
  - Unknown task type returns an empty mapping plus guidance, not a guessed skill.
  - Missing/unreadable skill file is reported explicitly.
  - Mapping performs no script execution or network access.
- **Security:** Treat skill text as untrusted data; do not auto-follow embedded instructions.
- **Effort:** 1–2 engineer-days.
- **Priority:** P0.
- **Team impact:** Prevents false capability claims and improves manual skill selection.

### H0-05 — File-scope checking

- **User problem:** Agents edit forbidden or unrelated paths.
- **Reuse:** Task template, Git diff/name-status and H0-01 path checks.
- **Proposed implementation:** Compare changed, staged and untracked paths against allowed/forbidden globs; classify deletions and renames; emit a deterministic report. Untracked paths are always included; there is no opt-out flag.
- **Dependencies:** H0-01 and approved task contract.
- **Proposed CLI:** `python .harness/harness.py scope check --task PATH --base REF`
- **Acceptance tests:**
  - Allowed modification passes; forbidden modification fails.
  - Untracked file is always included in the report and cannot be excluded by a flag.
  - Rename is checked against both old and new paths.
  - Deletion outside scope fails.
  - `../escape`, absolute outside path and symlink target are rejected.
  - Git/path enumeration failure or ambiguity fails closed.
  - No filesystem content is modified.
- **Security:** Read-only Git/path inspection; no shell; no automatic revert; incomplete path enumeration is a failure, not an empty scope.
- **Effort:** 2–3 engineer-days.
- **Priority:** P0.
- **Team impact:** Enables safer parallel documentation and later contract-first product work.

### H0-06 — Verification command execution

- **User problem:** Checks are run inconsistently and evidence is lost.
- **Reuse:** Existing validators, unit-test command and compile check.
- **Proposed implementation:** Structured allowlist runner with dry-run, working directory, timeout, output cap, exit capture and evidence artifact; no arbitrary shell.
- **Dependencies:** H0-03 contract and H0-05 scope report.
- **Proposed CLI:** `python .harness/harness.py verify run --task PATH --dry-run`; execution requires a separate `--execute` flag.
- **Acceptance tests:**
  - Dry-run prints resolved argv/cwd/timeout and changes nothing.
  - Known passing validator returns exit 0 and captured output.
  - Nonzero fixture returns the exact exit code and failure excerpt.
  - Timeout fixture terminates child process and records `TIMEOUT`.
  - Shell metacharacters/executable not on the allowlist are rejected.
  - Output beyond cap is truncated with an explicit marker.
- **Security:** No shell, allowlisted executables/arguments, bounded child process, redacted evidence.
- **Effort:** 3–5 engineer-days.
- **Priority:** P0 after scope checking.
- **Team impact:** Produces repeatable evidence without claiming unrun checks.

### H0-07 — Session handoff generation

- **User problem:** Manual handoffs become stale or omit blockers.
- **Reuse:** `HANDOFF.md`, `EXECUTION_STATUS.md`, Git state and H0-06 evidence.
- **Proposed implementation:** Generate a structured draft from observed branch/HEAD, changed paths, checks, blockers and next task; require human review before replacing the tracked handoff.
- **Dependencies:** H0-05 and H0-06.
- **Proposed CLI:** `python .harness/harness.py handoff write --task PATH --output PATH`
- **Acceptance tests:**
  - Output contains exact branch/HEAD and no invented Jira key/reviewer.
  - PASS/FAIL/NOT RUN/BLOCKED states match evidence files.
  - Existing output is refused without `--overwrite`.
  - Secret-pattern fixture is redacted.
  - Generated draft is deterministic for the same Git/evidence state.
- **Security:** No remote mutation; human approval required to publish handoff.
- **Effort:** 2–3 engineer-days.
- **Priority:** P0.
- **Team impact:** Improves resume reliability and reduces repeated audit work.

### H0-08 — Diagram validation and rendering adapters

- **User problem:** Parser extraction is mistaken for rendering; contributors lack a shared toolchain.
- **Reuse:** Galleries, validators, DOT renderer, Diagram Design extractor and parity method.
- **Proposed implementation:** Tool manifest with approved versions; validation adapter for metadata/assets/parity; separate renderer adapters for DOT and Mermaid after dependency approval.
- **Dependencies:** Approved tool manifest; Graphviz for DOT; reviewed pinned Mermaid runtime for Mermaid.
- **Proposed CLI:** `python .harness/harness.py diagram check --path PATH`; `diagram render --path PATH --tool dot|mermaid` remains disabled until its tool is approved.
- **Acceptance tests:**
  - Inventory finds 56 Mermaid and 26 DOT sources in the current baseline.
  - Metadata/gallery/static asset checks match existing validators.
  - Paired Mermaid/DOT parity passes 26/26.
  - Extractor exception is reported as `EXTRACTOR_COMPATIBILITY`, not `INVALID_MERMAID`.
  - DOT render uses the pinned executable and refuses unexpected output paths.
  - Mermaid render remains `BLOCKED` when no approved runtime is configured.
- **Security:** No arbitrary remote font/template fetch; sandbox browser runtime; inspect generated SVG/PNG.
- **Effort:** 3–5 engineer-days, excluding Mermaid dependency approval.
- **Priority:** P0 for validation; rendering gated by tool approval.
- **Team impact:** Makes diagram claims reproducible without replacing valid artifacts.

## 5. P1 capabilities

### H1-01 — Jira adapter

- **User problem:** Delivery state lives in an unimported CSV.
- **Reuse:** 39-row CSV, stable internal IDs, Jira setup plan.
- **Proposed implementation:** Offline CSV validation first; authenticated read/write adapter only after site/project authorization; dry-run mapping and idempotent sync.
- **Dependencies:** Authorized Jira tenant/project, field mapping and secret handling.
- **Proposed CLI:** `python .harness/harness.py jira validate --csv PATH`; `jira sync --dry-run` before any write.
- **Acceptance tests:** 39 unique IDs; empty/duplicate keys handled; dependency validation; dry-run changes nothing; unauthorized mode fails closed; one real issue-to-PR link verified after authorization.
- **Security:** Least privilege, token from environment/secret store, no token in logs, no fabricated keys.
- **Effort:** 4–6 engineer-days after access.
- **Priority:** P1 / Track A dependency.
- **Team impact:** Operationalizes Jira-first delivery.

### H1-02 — Repository intelligence

- **User problem:** Repeated searches waste context and miss dependencies.
- **Reuse:** Repository map, Grep/Glob workflows and future product source tree.
- **Proposed implementation:** Incremental file/symbol index with provenance and explicit refresh; no semantic claims without tests.
- **Dependencies:** H0-02/H0-03 context contracts; actual product source tree.
- **Proposed CLI:** `python .harness/harness.py repo index --path . --output PATH`
- **Acceptance tests:** Stable index for unchanged tree; hash-based delta; ignored originals excluded; symbol lookup returns file/line provenance; corrupted index rebuilds safely.
- **Security:** Local index; no source upload; path/size limits.
- **Effort:** 5–8 engineer-days.
- **Priority:** P1 after a measured repeated-search task.
- **Team impact:** Reduces context cost for larger codebases.

### H1-03 — Checkpoint and resume

- **User problem:** Long tasks cannot resume without re-reading everything.
- **Reuse:** Task contract and generated handoff schema.
- **Proposed implementation:** Versioned local run state with task ID, input hashes, step results, artifacts and stop reason; resume only compatible state.
- **Dependencies:** H0-03, H0-06 and H0-07.
- **Proposed CLI:** `python .harness/harness.py checkpoint save --task PATH`; `checkpoint resume --task PATH --checkpoint PATH`
- **Acceptance tests:** Save/restore exact step state; changed input hash blocks resume; partial failure records stop reason; no duplicate side effects; corrupt checkpoint fails closed.
- **Security:** Local encrypted/secret-free state; no automatic retry of external side effects.
- **Effort:** 5–8 engineer-days.
- **Priority:** P1 after one real long task demonstrates need.
- **Team impact:** Reduces repeated work and supports bounded execution.

### H1-04 — Resource telemetry

- **User problem:** Token/cost/runtime claims cannot be verified.
- **Reuse:** Verification evidence and provider/session telemetry where exposed.
- **Proposed implementation:** Record wall time, exit codes, bytes and provider-reported token/cost fields; unknown remains unknown.
- **Dependencies:** H0-06 and an approved provider/session metric source.
- **Proposed CLI:** `python .harness/harness.py telemetry summarize --run PATH`
- **Acceptance tests:** Wall time/bytes captured; missing token/cost shown as `unknown`; no estimated token counts presented as actual; redaction works; deterministic aggregation.
- **Security:** No prompt/source content in telemetry; provider data handling approval required.
- **Effort:** 3–5 engineer-days.
- **Priority:** P1.
- **Team impact:** Enables evidence-based routing/budget decisions later.

## 6. Dependency-aware implementation sequence

1. **Approve H0-01–H0-08 scope and security invariants.** No implementation starts from this plan alone.
2. **Wave H0-A:** H0-01 → H0-02 → H0-03.
3. **Wave H0-B:** H0-04 and H0-05 can run in parallel after H0-03.
4. **Wave H0-C:** H0-06 → H0-07.
5. **Wave H0-D:** H0-08 validation can proceed independently; renderer activation waits for approved tool manifests.
6. **P1:** Jira adapter follows authorization; repository intelligence follows real source-code scale; checkpoint follows a measured long task; telemetry follows approved metric sources.

Product work does **not** wait for H1. After `VS01-G6`, a product task may use the existing manual task contract, validators and Git/PR process while the harness is upgraded independently.

## 7. Approval checklist

- Owner approves P0 scope, effort range and security invariants.
- Technical owner approves structured command runner and path policy.
- Diagram owner approves tool manifest and renderer dependency process.
- Jira owner authorizes tenant/project before H1-01 network access.
- Each capability lands with tests, documentation, rollback and a handoff update.
- No capability is marked implemented until its exact acceptance tests pass in a clean clone.
