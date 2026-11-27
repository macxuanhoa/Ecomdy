# Phase 0 Capability Coverage Matrix

**Baseline:** `4bddc925c941979da60b1250ec4d139381776e22`
**Audit date:** 2026-11-27 (Asia/Saigon)
**Scope:** actual repository, CLI, tests, CI evidence, configuration, documentation and diagram artifacts. Target designs are not treated as runtime behavior.

## Status rules

| Status | Meaning |
|---|---|
| IMPLEMENTED AND VERIFIED | Executable behavior or repository artifact exists and a named check/evidence supports the claimed scope. |
| IMPLEMENTED BUT UNVERIFIED | Artifact/configuration exists, but current acceptance evidence is missing, denied or incomplete. |
| CONFIGURATION ONLY | Defaults, templates or candidate settings exist; no enforcing runtime is demonstrated. |
| SPECIFICATION ONLY | Requirements, design, task or policy text exists; no executable implementation is demonstrated. |
| NOT IMPLEMENTED | No implementation was found in the audited baseline. |
| BLOCKED | Required access, authorization, dependency or owner decision is unavailable. |
| REQUIRES HUMAN APPROVAL | Evidence may exist, but the next action requires an explicit authorized person. |

A passing documentation validator does not verify product behavior, Mermaid grammar, diagram semantics or deployment. Jira keys remain `TBD` until an authorized Jira project is available.

## A. Repository, governance and reproducibility

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| FND-01 | Requirements and target-design baseline | `docs/01-requirements.md`, `docs/requirements-traceability.md`, `docs/project-context.md` | Validator PASS; target/current states explicitly separated. | IMPLEMENTED AND VERIFIED | Maintain requirement-to-task traceability; owner ratifies constitution before implementation. |
| FND-02 | Local-only original-source protection | `.gitignore`, `docs/00-original/`, `docs/source-registry.md` | Fresh clones contain only the tracked README under original-document paths; local PDF/XLSX/JPG inputs were absent. | IMPLEMENTED AND VERIFIED | Add a deterministic publication check before any future publish operation. |
| FND-03 | Git baseline and draft PR | PR #1, branch `setup/phase-0-audit` | Local/remote setup HEAD equals `4bddc925…`; PR #1 is open, draft, mergeable and clean. Remote `main` remains `560cf0d…`. | IMPLEMENTED AND VERIFIED | Owner review required; do not merge PR #1 without approval. |
| FND-04 | Repository CI | `.github/workflows/validate.yml` | Push run `45854047956` and PR run `45854060651` passed; local equivalent checks passed. | IMPLEMENTED AND VERIFIED | Keep required check `validate`; add parser/render checks only after approved tooling is pinned. |
| FND-05 | Protected `main` | GitHub branch protection/ruleset | Historical setup read-back exists, but Phase 0 API revalidation returned HTTP 401; current settings cannot be independently accepted. | IMPLEMENTED BUT UNVERIFIED | Owner provides authenticated read-back after PR review; confirm required reviews and admin enforcement. |
| FND-06 | Repository security settings | `SECURITY.md`, `docs/security-governance.md` | Secret scanning/push protection/vulnerability reporting are documented from earlier setup; current Phase 0 read-back was unavailable. | IMPLEMENTED BUT UNVERIFIED | Re-read settings with owner authorization; do not infer enabled state from documentation alone. |
| FND-07 | Code ownership review | `.github/CODEOWNERS` | No `CODEOWNERS` file found; no reviewer group is established. | NOT IMPLEMENTED | Owner nominates reviewers and module owners; add scoped `CODEOWNERS` after approval. |
| FND-08 | Branch and PR convention | `CONTRIBUTING.md`, `.github/pull_request_template.md` | Minimal feature-branch guidance exists; no Jira-key or branch-pattern convention exists. | SPECIFICATION ONLY | Adopt the controlled branch/PR convention in `PHASE_0_ACCEPTANCE.md`; update template. |
| FND-09 | Fresh-clone reproducibility | `scripts/validate.py`, `.harness/tests/`, `.harness/scripts/validate.py` | Two independent temporary clones of baseline `4bddc925…` passed product validator, 3 harness tests and harness validator. | IMPLEMENTED AND VERIFIED | Repeat after accepted dependency/tooling changes; record commit and outputs. |
| FND-10 | Two-workspace isolation simulation | Separate temporary clones | Both workspaces completed checks independently; original inputs were not present in either clone. | IMPLEMENTED AND VERIFIED | For real parallel work, add contract-first module ownership and integration fixtures. |
| FND-11 | Execution checkpoint and handoff | `docs/setup/HANDOFF.md`, `docs/setup/EXECUTION_STATUS.md` | Current branch, SHA, PR state, checks, blockers and non-goals are recorded and reconciled by this package. | IMPLEMENTED AND VERIFIED | Update at every safe stop; never use stale handoff as current proof. |

## B. Project management and Jira

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| PM-01 | Jira Cloud project, backlog, Scrum board and epics | `docs/setup/JIRA_SETUP_PLAN.md` | No Jira site URL, connector, CLI, credential or authorization was available. No issue, project, board or sprint was fabricated. | BLOCKED | Owner authorizes access and approves project key/name/workflow; execute the setup plan. |
| PM-02 | Jira–GitHub integration and automation | `docs/setup/JIRA_SETUP_PLAN.md` | No Jira integration or automation result exists. | BLOCKED | Connect the approved repository, verify PR/branch linking and least-privilege rules. |
| PM-03 | Requirement/task traceability | `docs/requirements-traceability.md`, `docs/task-register.md`, `docs/setup/TASK_REGISTRY.md` | Unique requirement, setup and product task IDs exist; Jira keys are not yet assigned. | IMPLEMENTED AND VERIFIED | Add real Jira keys after access; do not replace requirement IDs. |
| PM-04 | Sprint/backlog planning | `docs/sprint-planning.md`, `docs/setup/JIRA_SETUP_PLAN.md` | Candidate waves and dependencies exist; dates, capacity and commitments are explicitly unapproved. | SPECIFICATION ONLY | Owner confirms capacity, sprint cadence and acceptance gates before scheduling. |

## C. Embedded DevHarness runtime

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| HAR-01 | Workspace initialization | `.harness/harness.py` → `initialize` | Unit test confirms existing files are preserved and missing ignore rules are appended. | IMPLEMENTED AND VERIFIED | Keep behavior; add tests for re-init and path edge cases when scope is approved. |
| HAR-02 | Source inventory and SHA-256 | `.harness/harness.py` → `ingest` | Unit test confirms inventory creation for authorized local files; symlinks/out-of-scope paths are skipped. | IMPLEMENTED AND VERIFIED | Keep extraction manual unless an approved task adds adapters. |
| HAR-03 | Generated-output overwrite protection | `.harness/harness.py`, `--overwrite` | Unit test confirms refusal without opt-in and explicit overwrite behavior. | IMPLEMENTED AND VERIFIED | Preserve; do not weaken the guard for automation convenience. |
| HAR-04 | Environment doctor | `.harness/harness.py` → `doctor` | CLI reports Python/Git/Graphviz/GitHub CLI availability and advisory mode. | IMPLEMENTED AND VERIFIED | Treat as advisory, not a readiness gate for absent product runtime. |
| HAR-05 | Link, registry and diagram-asset validation | `.harness/scripts/validate.py`, `scripts/validate.py` | Both validators PASS; metadata, listing and assets are checked. | IMPLEMENTED AND VERIFIED | Add approved Mermaid parser/render validation separately. |
| HAR-06 | Harness unit tests | `.harness/tests/test_harness.py` | 3/3 tests PASS in local worktree, CI and fresh clones. | IMPLEMENTED AND VERIFIED | Add tests alongside any approved harness change. |
| HAR-07 | Runtime configuration enforcement | `.harness/config/default.json` | `automation_enabled: false`, budgets and `approved_tasks_only: true` exist, but the CLI does not read/enforce the file. | CONFIGURATION ONLY | HARD-01: define enforcement contract and tests before enabling any automation. |
| HAR-08 | Task-contract scope enforcement | `.harness/templates/task.json` | Fields for dependencies, allowed/forbidden paths, criteria, commands, budgets and approval exist; no executor enforces them. | CONFIGURATION ONLY | HARD-02: implement a bounded validator/executor only after owner approval. |
| HAR-09 | Executable role agents | `.harness/registry/capabilities.json`, product role profiles | Roles are definitions only; no agent executor/provider adapter exists. | SPECIFICATION ONLY | Map roles to deterministic tasks before considering model-backed agents. |
| HAR-10 | Scheduler/worker | `docs/automation-specification.md` | No scheduler, queue, worker or product job runner exists; runtime automation is false. | NOT IMPLEMENTED | Keep disabled; design after source/runtime approvals. |
| HAR-11 | Checkpoint/resume | `docs/automation-specification.md`, handoff documents | Manual checkpoints exist; no persisted execution state or resume mechanism exists. | NOT IMPLEMENTED | HARD-03: specify state schema and recovery tests if automation is approved. |
| HAR-12 | Iteration/runtime/cost enforcement | `.harness/config/default.json`, task template | Limits are configured (`3` iterations, `30` minutes, `$1`) but not enforced. | CONFIGURATION ONLY | HARD-01: enforce pre-call and stop conditions; no paid calls without approval. |
| HAR-13 | Scoped retrieval and repository index | `docs/context-engineering.md` | No retrieval index, context compiler or incremental index exists. | NOT IMPLEMENTED | CTX-01: prototype only after measuring a real task and defining provenance. |
| HAR-14 | Automatic handoff generation | `.harness/prompts/bootstrap.md`, manual handoff doc | A prompt requests evidence-first planning; no automatic checkpoint/handoff generator exists. | NOT IMPLEMENTED | HARD-03: generate structured handoff only from verified run state. |
| HAR-15 | Standalone/embedded parity | Sibling `devharness-os/` versus `.harness/` | Standalone ingest lacks overwrite guard; standalone validator omits Mermaid metadata checks; standalone has 2 tests versus embedded 3. | NOT IMPLEMENTED | Either retire the standalone copy or port reviewed fixes with parity tests; do not silently maintain two behaviors. |

## D. Diagram engineering and tooling

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| DGM-01 | Editable diagram sources and registry metadata | `docs/diagrams/`, `.harness/docs/diagrams/` | 56 unique IDs: 56 Mermaid sources, 26 DOT sources; embedded validator PASS; no exact duplicate Mermaid/DOT content. | IMPLEMENTED AND VERIFIED | Preserve sources; update version/state comments on approved changes. |
| DGM-02 | Static DOT renderings | 26 SVG + 26 PNG artifacts | All SVGs parse and contain expected DOT labels; all PNGs are valid/nonblank; overview contact sheets showed no obvious clipping. | IMPLEMENTED AND VERIFIED | Re-render only changed DOT after approved Graphviz installation/version pinning. |
| DGM-03 | Mermaid syntax validation and local rendering | Mermaid sources, GitHub-rendered snippets | 30 Mermaid-only diagrams have no local static render; no Mermaid parser/CLI executed. | IMPLEMENTED BUT UNVERIFIED | Install approved pinned Mermaid CLI in a separate task; parse/render all Mermaid sources. |
| DGM-04 | Mermaid/DOT source-to-artifact consistency | 26 paired source sets | A first comparison script produced false mismatches by treating titles/edge labels as node labels; no reliable parity verdict exists. | IMPLEMENTED BUT UNVERIFIED | Fix parser semantics and run deterministic comparison before regeneration. |
| DGM-05 | Visual quality | Contact sheets and existing artifacts | Existing 26 static renderings inspected at overview scale; no obvious clipping. Full-size review of every changed diagram remains task-specific. | IMPLEMENTED AND VERIFIED | Inspect each newly rendered artifact before claiming visual acceptance. |
| DGM-06 | Semantic/as-built correctness | 56 target diagrams | All are explicitly target design; no product runtime exists to compare against. | BLOCKED | Owner approves target semantics; compare to as-built only after implementation evidence exists. |
| TLS-01 | Diagram Design plugin/skill | Qoder marketplace `diagram-design` 2.6.131 | Official market metadata found; one skill, six commands, no MCP. Not installed; license/security review incomplete. | CONFIGURATION ONLY | Owner selects it before installation; record source, license, version and compatibility. |
| TLS-02 | Official Draw.io MCP / Agent Skill | Marketplace and MCP catalog | No official Draw.io MCP was verified; community/third-party candidates were not treated as official. | NOT IMPLEMENTED | If needed, obtain an official source or approve a specific third-party after security review. |
| TLS-03 | Mermaid CLI | `@mermaid-js/mermaid-cli` | Metadata reviewed: 12.2.0, MIT, Node >=22.13.0; local Node 22.18.0 meets engine. Not installed. | CONFIGURATION ONLY | DIAG-01: approve exact version, lock dependencies and verify Chromium sandbox/security settings. |
| TLS-04 | Structurizr | Architecture-as-code candidate | Useful for model-driven C4/views, but no need or implementation is established; no installation performed. | CONFIGURATION ONLY | Use only if C4 model consistency becomes a requirement; evaluate DSL/CLI license and Java/runtime dependencies first. |

## E. Context, token and collaboration controls

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| CTX-01 | Progressive L0–L4 context loading | `docs/context-engineering.md` | Policy/specification exists; no automated loader enforces it. | SPECIFICATION ONLY | Pilot on one approved task with file/byte/token ceilings and measured results. |
| CTX-02 | Scoped task context pack | `.harness/templates/task.json`, PR template | Contract fields exist; no compiler assembles or validates a pack automatically. | CONFIGURATION ONLY | PRGOV-01: require baseline, scope, dependencies, evidence and stop conditions in each task. |
| CTX-03 | Token/cost/runtime telemetry | Provider/session telemetry | No versioned telemetry artifact or provider cost breakdown was found. The reported 1,189,524 tokens / ~1h38m is user-supplied and not independently decomposed. | NOT IMPLEMENTED | Capture provider-reported metrics without inventing missing fields; start with bounded task budgets. |
| CTX-04 | Incremental indexing/delta audit | Context engineering specification | No incremental index, delta auditor or cache exists. | NOT IMPLEMENTED | Measure a real repeated audit before selecting an indexing approach. |
| CTX-05 | Deterministic-first acceptance process | Validators, tests, Git/API checks, diagram scripts | Phase 0 used local checks before document synthesis; outputs and limits were recorded. | IMPLEMENTED AND VERIFIED | Keep this order for subsequent phases; avoid repeated review of unchanged files. |
| COL-01 | Module ownership | Constitution, roadmap | No named owners or ownership map exists; team members were not invented. | NOT IMPLEMENTED | Owner assigns module/reviewer ownership; add `CODEOWNERS`. |
| COL-02 | API/schema contract coordination | `docs/api-design.md`, `docs/database-design.md` | Target contracts only; no OpenAPI artifact, migration owner or contract-change workflow exists. | SPECIFICATION ONLY | Contract-first change task with compatibility tests and rollback before parallel implementation. |
| COL-03 | Integration-test policy | `docs/06-validation.md` | Target strategy exists; no product integration suite or fixtures exist. | SPECIFICATION ONLY | Define contract fixtures and CI integration gate before vertical-slice work. |
| COL-04 | Parallel conflict prevention | Task template, roadmap | Allowed/forbidden path fields exist but are not enforced; no ownership/locking convention exists. | CONFIGURATION ONLY | Use small non-overlapping tasks, contract-first changes and deterministic diff checks. |
| COL-05 | Reviewer assignment | PR template, branch protection evidence | PR review process exists, but no reviewer team or minimum approval is confirmed. | REQUIRES HUMAN APPROVAL | Owner nominates independent reviewers and approval count; verify protection read-back. |

## F. Product capabilities M01–M20

Shared evidence: all 20 entries are `Proposed` in `docs/02-product-vision.md`; `project-profile.json` sets `runtime_automation: false`; no application package, API, database, UI, AI executor or scheduler exists. The status below is therefore SPECIFICATION ONLY for every product capability.

| ID | Capability | Implementation / reference | Phase 0 evidence | Status | Next action |
|---|---|---|---|---|---|
| M01 | Source Management | Product vision, `docs/source-registry.md` | Requirement/design only; source allowlist is empty. | SPECIFICATION ONLY | ECO-01/ECO-02/ECO-05: approve source policy, ownership and schema. |
| M02 | Data Collection | Architecture/ingestion diagrams, module specs | No connector, fetch record or ingestion runtime. | SPECIFICATION ONLY | ECO-06: one approved connector with fixtures and provenance. |
| M03 | Scheduled Crawling | `docs/automation-specification.md` | No scheduler/worker; schedules disabled by policy. | SPECIFICATION ONLY | ECO-06/ECO-08: define disabled-by-default job contract and safe schedule. |
| M04 | Data Normalization | SRS, processing diagram, module specs | No normalization code or tests. | SPECIFICATION ONLY | ECO-07: deterministic fixtures and temporal rules. |
| M05 | Deduplication | SRS, processing diagram | No duplicate detection implementation. | SPECIFICATION ONLY | ECO-07: exact/semantic fixtures with measured precision/recall. |
| M06 | News Classification | SRS, processing diagram | No taxonomy/classifier implementation. | SPECIFICATION ONLY | ECO-07: approved taxonomy and labeled fixtures. |
| M07 | Market Intelligence | Product vision, target diagrams | No market data model or analysis runtime. | SPECIFICATION ONLY | Scope with owner; likely ECO-12 extension after core evidence. |
| M08 | Trend Intelligence | Product vision, automation spec | No trend snapshots or aggregation implementation. | SPECIFICATION ONLY | ECO-12: separate extension decision and benchmark. |
| M09 | Claim Extraction | SRS, role registry | No claim extraction or span-linking implementation. | SPECIFICATION ONLY | ECO-07: claim schema and provenance fixtures. |
| M10 | Source Verification | SRS, security/governance | No verifier or supported/conflicted/stale state implementation. | SPECIFICATION ONLY | ECO-07: authority, conflict and effective-date tests. |
| M11 | Seller Impact Analysis | Product vision, role registry | No seller-impact inference or evaluation implementation. | SPECIFICATION ONLY | Define acceptance during ECO-01/ECO-05; preserve inference labels. |
| M12 | Knowledge Database | `docs/database-design.md` | Conceptual model only; no schema, instance or migration. | SPECIFICATION ONLY | ECO-05: approved contracts, retention and migration strategy. |
| M13 | Weekly Digest | Product vision, workflows | No digest generator or scheduled sample. | SPECIFICATION ONLY | ECO-08: controlled one-week sample with citations. |
| M14 | Content Studio | Product vision, user guide | No editor, draft generator or version store. | SPECIFICATION ONLY | ECO-08/ECO-09: web/social/video drafts and exact-version review. |
| M15 | SEO Assistant | Product vision, role registry | No SEO checks or channel optimization implementation. | SPECIFICATION ONLY | ECO-08: approved rubric and cited-output checks. |
| M16 | Content Freshness Audit | Product vision, roadmap | No authorized corpus or audit implementation. | SPECIFICATION ONLY | ECO-10: old/new fixtures with evidence-linked findings. |
| M17 | Editorial Workflow | Product vision, security/governance | No role checks, review states or approval invalidation. | SPECIFICATION ONLY | ECO-09: authorization and version-invalidation tests. |
| M18 | Conversational Assistant | Product vision | No assistant, retrieval or Telegram adapter. | SPECIFICATION ONLY | ECO-12: extension decision after MVP evidence. |
| M19 | Notification System | Product vision, tool registry | No notification adapter, consent or delivery controls. | SPECIFICATION ONLY | ECO-12: extension decision and least-privilege delivery design. |
| M20 | Analytics and Evaluation | Product vision, validation strategy | No metrics pipeline, baseline or evaluation dataset. | SPECIFICATION ONLY | ECO-04/ECO-11/ECO-12: approve rubric, baseline and reporting. |

## Acceptance interpretation

The matrix accepts the **documentation/setup baseline and bounded advisory harness** only. It does not accept Ecomdy as an implemented product or DevHarness as an autonomous execution platform. Jira, diagram parser/render coverage, ownership and runtime enforcement remain explicit gaps with next actions rather than implied completion.
