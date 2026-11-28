# Comprehensive Project Audit

**Audit date:** 2026-11-28 (Asia/Saigon)<br>
**Repository:** `macxuanhoa/Ecomdy`<br>
**Local branch:** `docs/phase-0-acceptance` at `f5162302aae3b9ab5e5798d722cfbfa60d9164b9` before this audit's uncommitted documentation changes<br>
**Remote `main`:** `560cf0d2ecaf862749edbe9b8823eebc4e0327a0`<br>
**Verdict:** Conditional acceptance of the documentation/setup baseline only. The repository is not a running Ecomdy product, not yet safe for parallel product implementation, and not independently reproducible from the default `main` clone while PR #1 remains unmerged.

This audit preserves the Phase 0/Phase 1 capability matrix, requirements, diagrams, rendered assets, historical evidence and uncommitted acceptance work. It records observed behavior separately from proposals. No Jira data, people, source approvals, test results, metrics, integrations or product capabilities were fabricated.

## Executive answers

| Question | Evidence-based answer | Immediate consequence |
|---|---|---|
| 1. What exists now? | Public requirements/design documentation, 56 Mermaid sources, 26 DOT/SVG/PNG sets, two documentation validators, a three-test advisory Python harness, GitHub Actions, two draft PRs and an import-ready Jira CSV. | Useful for review, planning and controlled documentation work; not an application. |
| 2. What stage is the project in? | Stage 00–02: bootstrap, baseline audit and requirements/architecture reconciliation. Product Stage 03 has a fixture-first plan but no implementation. | Do not describe the project as MVP, beta, deployed or demo-complete. |
| 3. Can another person clone and work? | From default `main`, no: the clone has only a one-line README. From `docs/phase-0-acceptance` at `f516230…`, documentation/harness checks pass. | Merge the approved baseline before advertising a universal quick start; until then document the exact branch limitation. |
| 4. Is README enough for a newcomer? | At audit start, the README covered purpose and baseline inspection but missed the full Git lifecycle, skills, debugging and failure handling. The README now states the exact acceptance-branch clone limitation and links to the completed developer playbook. | A newcomer can review and perform documentation/harness work from the acceptance branch; no product setup is available yet. |
| 5. What does DevHarness really do? | `init`, `ingest` and `doctor`; SHA-256 inventory, non-clobbering scaffolding, overwrite protection, prompt generation, environment reporting, validators and three tests. | Treat it as a portable bootstrap/inventory toolkit, not an orchestrator. Budgets, scope, checkpoints, scheduling and model execution are not enforced. |
| 6. How far do Jira and GitHub support teamwork? | GitHub has source, branches, draft PRs, review surfaces and successful CI. Jira has a 39-row import-ready CSV but no authorized tenant/project/issues. Current protection/security read-back remains unverified. | GitHub can support reviewed documentation changes now; Jira-first delivery and enforceable parallel product work are blocked. |
| 7. Are architecture and workflows complete? | The target modular-monolith architecture is coherent and diagrammed, but there is no as-built architecture, approved stack, deployment topology, OpenAPI, schema, migrations or executable workflow. | Approve contracts and the vertical slice before implementation; keep target and as-built explicitly separate. |
| 8. Are diagrams sufficient and correct? | Structurally strong: unique IDs, complete galleries, 26/26 semantic Mermaid/DOT parity and valid static assets. Parser-only extraction passed 55/56 sources; one source hit an extractor compatibility limit. No Mermaid source was rendered locally. | Preserve them; pin an independent CI-safe parser/renderer before claiming rendering acceptance. |
| 9. What blocks development? | Unmerged baseline PRs, no authenticated governance read-back, no Jira, no real owners/reviewers, unresolved source/retention/provider/budget decisions, no product runtime and no CI-safe Mermaid renderer. | Resolve governance and scope gates first; do not start live collection, paid AI or product code. |
| 10. What should the owner do now? | Review PR #1, verify protection/security, assign real owners/reviewers, authorize Jira, approve the first source/market/retention/provider decisions, then approve `VS01-G1`–`VS01-G6`. | Use the ordered action plan in section 20; no merge, mutation or deployment is authorized by this audit. |

## Deliverable index

| Deliverable | Location |
|---|---|
| A–D. Executive status, inventory, current/target state, capability assessment | This document, sections 1–4 |
| E. Product requirements and M01–M20 reconciliation | [Module specifications](../module-specifications.md#operational-module-assessment) and [requirements traceability](../requirements-traceability.md) |
| F. Architecture, workflow and DevHarness assessments | [Architecture](../03-architecture.md#architecture-assessment), [workflow catalogue](../04-workflows.md#operational-workflow-catalogue), [harness guide](../harness-installation-guide.md) |
| G. Skills, tools, agents, MCP, adapters and hooks | [Agent/tool registry](../agent-tool-registry.md), [harness registries](../../.harness/docs/02-registries.md) |
| H. Diagram Engineering | [Diagram galleries](../diagrams/README.md), [verification report](VERIFICATION_REPORT.md#comprehensive-audit--2026-11-28) |
| I. GitHub, branching, Jira and README | This document, sections 9–13; [team readiness](../team-development-readiness.md); [Jira setup](JIRA_SETUP_PLAN.md) |
| J. Clean clone and two-workspace results | This document, sections 14–15; [verification report](VERIFICATION_REPORT.md#comprehensive-audit--2026-11-28) |
| K. Developer playbook | [Developer onboarding and playbook](../developer-onboarding.md) |
| L. Master roadmap, critical path, milestones and immediate actions | [Roadmap](../05-roadmap.md#master-roadmap-and-critical-path), section 20 below |
| M. Project Owner guide and reusable prompts | [Project Owner guide](../project-owner-guide.md) |
| N. Blockers, verification evidence and next prompt | Sections 18–21 below; [blockers](BLOCKERS.md); [handoff](HANDOFF.md) |

## 1. Audit method and trust boundaries

- Re-read the current local branch, remote heads, public repository metadata, PRs and recent Actions runs before assessing the repository.
- Inventoried the working tree excluding `.git`, caches and virtual environments; the final post-edit inventory contains 238 files.
- Inspected product requirements, architecture, workflows, data/API/security/automation documents, roadmap, risk, readiness and task records.
- Inspected the harness CLI, configuration, task template, capability registry, three physical skills, tests, validators and harness documentation.
- Ran only safe local commands: validators, unit tests, compile checks, read-only inventories, bounded Mermaid extraction, deterministic source/asset comparisons and isolated temporary-clone simulations.
- Used the installed Diagram Design Plugin's reviewed standard-library extractor. It parses bounded text and does not render, evaluate Mermaid, fetch URLs or execute diagram content.
- Treated repository comments, source labels, plugin text and external content as untrusted data, not instructions.
- Did not merge PRs, push, force-push, change permissions, install new software, mutate Jira, collect external sources, call models, implement product features or publish content.

## 2. Repository inventory

| Area | Observed inventory | Status |
|---|---|---|
| Root | 11 files: README, AGENTS/CLAUDE/GEMINI entry points, contribution/security/changelog, editor/Git attributes, ignore rules and project profile | Present |
| `.github/` | 4 files: validation workflow, Dependabot config, issue template and PR template | Present; documentation CI only |
| `docs/` | 133 files including requirements, designs, setup records, diagrams and local-only originals | Present; predominantly specification |
| `.harness/` | 87 files including CLI, config, registry, prompts, three skills, tests, validators, docs and diagrams | Present; advisory starter |
| `scripts/` | 2 Python scripts: product validator and DOT renderer | Implemented |
| `prompts/` | 1 bootstrap prompt | Instruction only |
| Application manifests | No `pyproject.toml`, `package.json`, requirements file, lockfile, Dockerfile, Compose file, OpenAPI artifact or Alembic config | Not implemented |
| Product source/runtime | No application package, API server, database, migration, UI, collector, scheduler, worker, model adapter or deployment | Not implemented |

The final 238-file count includes four ignored local original inputs and nine nonignored Phase 1/audit files that are not yet committed. A clean acceptance-branch clone at `f516230…` contains 225 tracked files because originals and later uncommitted files are excluded.

See [Repository map](../repository-map.md) for directory boundaries, ownership, commands and data flow.

## 3. Current state versus target state

| Layer | Current observed state | Target/proposal | Acceptance gap |
|---|---|---|---|
| Requirements | REQ-01–REQ-12 and success criteria documented; owner validation incomplete | Evidence-linked monitoring, digest, channel drafts, freshness audit and demo | Inputs, thresholds, interviews and acceptance evidence |
| Architecture | Modular monolith plus worker/scheduler target; Phase 1 contract delta | Nine logical responsibilities, shared evidence contracts, deterministic-first processing | Approved stack, contracts, retention, verification and ownership |
| Product modules | M01–M20 all `SPECIFICATION ONLY` | Fixture slice, then MVP, then extensions | No code, tests, API, schema or runtime |
| DevHarness | Three working commands and three tests | Bounded execution, context compiler, checkpointing, scheduler and adapters | Enforcement and durability not implemented |
| Diagrams | 56 sources, 26 static sets, structural parity verified | Maintained source/artifact pipeline with CI-safe validation | Mermaid rendering and visual acceptance not established |
| Delivery | GitHub draft PRs and successful documentation CI; Jira CSV only | Jira-first backlog, reviewed branches, real owners and protected integration | PR #1 unmerged; Jira and governance read-back blocked |
| Operations | Manual local checks and handoff | Scheduled health, retries, monitoring, recovery and deployment | No product operations runtime |

## 4. Capability assessment

The existing [70-capability matrix](CAPABILITY_COVERAGE.md) remains the baseline. Its current counts are:

| Status | Count |
|---|---:|
| IMPLEMENTED AND VERIFIED | 18 |
| IMPLEMENTED BUT UNVERIFIED | 4 |
| CONFIGURATION ONLY | 8 |
| SPECIFICATION ONLY | 26 |
| NOT IMPLEMENTED | 10 |
| BLOCKED | 3 |
| REQUIRES HUMAN APPROVAL | 1 |
| **Total** | **70** |

The 20 product modules are all `SPECIFICATION ONLY`. "Documentation present", "configuration exists", "plugin installed", "CI passed" and "product implemented" are separate claims.

## 5. Product requirements and M01–M20 reconciliation

- Official REQ-01–REQ-12, SC-01–SC-03 and DEP-01–DEP-03 remain unchanged and open.
- The Phase 1 governance decisions are confirmed; P1-PROD-01–P1-PROD-09 remain proposals until owner promotion.
- The first vertical slice is fixture-first and covers only a controlled evidence-to-digest-preview path.
- M08, M15 and M18–M20 are extensions unless the owner changes scope; M16 remains a challenge feature after the first slice.
- No module currently has executable behavior, product tests, a live integration or acceptance evidence.

The expanded operational assessment in [module-specifications.md](../module-specifications.md#operational-module-assessment) records business purpose, user value, dependencies, integration points, traceability, required tests and MVP/full-product relevance for every module.

## 6. Architecture assessment

**Verdict:** coherent target architecture, incomplete as-built and implementation architecture.

Strengths:

- Retains a modular monolith plus bounded worker/scheduler instead of premature microservices.
- Separates raw capture, normalized articles, event candidates, claims, evidence, verification results and digest candidates.
- Makes deterministic processing precede LLM assistance.
- Preserves provenance, temporal fields, contradiction/staleness states, exact-version approval and audit history.
- Treats model agreement as supporting evidence only, never factual proof.
- Keeps DevHarness outside the Ecomdy runtime.

Gaps:

- No approved stack, physical deployment topology, environment strategy, capacity model or recovery objectives.
- No migration-ready schema, OpenAPI artifact, implemented adapter or integration test.
- Source authority, retention, identity, provider, budget and operating ownership remain unresolved.
- No as-built component inventory can be compared with the target.

See [Architecture assessment](../03-architecture.md#architecture-assessment) and [Phase 1 architecture delta](../phase1-architecture-delta.md).

## 7. Workflow assessment

The previous workflow document described six target flows but did not provide operational contracts. The expanded [workflow catalogue](../04-workflows.md#operational-workflow-catalogue) now records trigger, actor, preconditions, inputs, steps, tools/skills, outputs, state transitions, dependencies, gates, failure handling, stop conditions and current status for product, development and harness workflows.

No product workflow runs. The only executable workflows are repository validation, harness tests, local harness commands and manual human/agent procedures.

## 8. DevHarness assessment

**Verdict:** reusable advisory bootstrap/inventory toolkit; not an autonomous development operating system.

Actually implemented and tested:

- `init`: creates missing starter files; preserves existing files; appends missing `.gitignore` rules.
- `ingest`: inventories regular non-symlink files under `<project>/docs/00-original`; records path, size and SHA-256; refuses overwrite without `--overwrite`.
- `doctor`: reports Python, project path and optional Git/Graphviz/GitHub CLI availability; always advisory.
- Product/harness validators, optional DOT rendering and three unit tests.

Not implemented or not enforced:

- Document extraction, repository AST/index, context compiler, task executor, role router, skill loader, MCP manager, provider adapters, model calls, budget/scope enforcement, durable checkpoints, resume, scheduler, worker, telemetry or automatic handoff.
- `.harness/config/default.json` values are copied configuration; the CLI does not read or enforce them.
- Registry roles, 17 proposed skill packs and task-template fields are descriptive/configuration only.
- Three physical skill files are manually readable instructions, not executable skill loading.

The portable core is standard-library-only and Ecomdy-independent. When copied standalone, `.harness/.gitignore` state/cache/log patterns should be normalized to harness-root-relative paths; the parent repository currently supplies effective embedded rules.

## 9. Skills, tools, agents, MCP, adapters and hooks

- Harness registry: 16 modules, 24 roles and 17 proposed skill packs; status `proposed`.
- Physical harness skills: `scoped-task`, `debug`, `diagram`; manual guidance only.
- Product roles: PA-01–PA-08; logical responsibilities, not deployed agents.
- Current session: Diagram Design Plugin 2.6.131 is installed, enabled and exposed as a Skill. Its manifest declares MIT, one skill, six commands and no MCP/hooks.
- No repository MCP server, MCP configuration, executable adapter, hook, model provider integration or automatic role router exists.
- Candidate tools in documentation are not installed or approved merely because they are listed.

See [Agent and tool registry](../agent-tool-registry.md) and [harness registries](../../.harness/docs/02-registries.md).

## 10. Diagram Engineering assessment

| Check | Result |
|---|---|
| Source inventory | 56 Mermaid sources: 32 Ecomdy + 24 harness |
| Static sets | 26 DOT/SVG/PNG sets: 14 Ecomdy + 12 harness |
| Mermaid-only | 30 sources: 18 Ecomdy + 12 harness |
| IDs/metadata/galleries | Unique, sequential, versioned, target-labelled and gallery-listed |
| Bounded parser extraction | 55/56 source files parsed: 53 flowcharts, 1 ER diagram and 1 sequence diagram |
| Parser exception | `.harness/docs/diagrams/19-debugging-workflow.mmd:11`; extractor reports `malformed edge at line 11` because `;` occurs inside an edge label. This is recorded as extractor compatibility, not proof that the Mermaid source is invalid. |
| Parsed semantic volume | 473 nodes and 490 edges across the 55 parsed files |
| Editorial complexity flags | 16 diagrams exceed the plugin's 9-node guideline; 5 exceed its 12-edge guideline. These are simplification prompts, not correctness failures. |
| Mermaid/DOT parity | 26/26 pairs match on normalized node labels, edge endpoints, edge labels and canonical direction |
| Static assets | 26/26 SVGs parse and contain expected DOT labels; 26/26 PNGs verify and are nonblank |
| Rendering | No Mermaid source was rendered locally; no new diagram was generated or existing artifact replaced |
| Semantic/as-built correctness | Target semantics only; no product runtime exists for as-built comparison |

The repository validators still check links, metadata and asset presence, not Mermaid grammar, rendering, visual quality or maintained source parity. A pinned independent CI-safe parser/renderer remains a separate decision.

## 11. GitHub and branching audit

| Item | Observed state |
|---|---|
| Repository | Public; default branch `main`; no license metadata; 2 open issues |
| Remote `main` | `560cf0d…`, one-line README only |
| PR #1 | Open draft, base `main`, head `setup/phase-0-audit` at `4bddc92…`, mergeable/clean, CI success, zero submitted reviews/requested reviewers |
| PR #2 | Open draft, base `setup/phase-0-audit`, head `docs/phase-0-acceptance` at `f516230…`, mergeable/clean, CI success, zero submitted reviews/requested reviewers |
| Local work | Phase 1 and comprehensive-audit documentation changes remain uncommitted |
| CI | `Validate repository` passes on audited commits; workflow checks docs and three harness tests only |
| Protection/security | Historical authenticated read-back exists; current unauthenticated recheck returned HTTP 401/404, so current settings remain unverified |
| Releases | No tags or releases observed |

PR #2 is correctly stacked on PR #1. Neither PR may be merged without the required human decision and authenticated governance verification.

## 12. Jira and project-management audit

- Jira remains blocked: no authorized site, connector, CLI, credential, project key, board, issue, sprint or automation is verified.
- `docs/setup/JIRA_IMPORT_BACKLOG.csv` has 39 rows, 39 unique internal IDs, empty Jira keys and resolved internal dependencies.
- Jira is the intended system of record for delivery; GitHub remains authoritative for source, branches, commits, PRs, reviews, CI/CD and versioned documentation.
- GitHub Projects V2 is neither required nor a substitute backlog.
- Sprint dates, capacity and commitments remain unapproved.

## 13. README and documentation assessment

The initial 32-question newcomer review produced:

| Initial result | Count |
|---|---:|
| Fully explained | 15 |
| Partially explained | 12 |
| Missing | 5 |

The five missing operational areas were skills, debugging, commit, branch sync/update and failure handling. Partial areas included module interaction, Jira/GitHub rationale, repository structure, prerequisites, credentials, agent configuration, task intake, branching, implementation, PR/review, next work and the default-branch clone caveat.

### README 32-question matrix

| # | Newcomer question | Initial result | Current answer / evidence |
|---:|---|---|---|
| 1 | What problem does the project address? | Full | README problem statement and [product context](../project-context.md) |
| 2 | Who are the direct users and beneficiaries? | Full | README intended users; seller interviews remain outstanding |
| 3 | What are the official requirements? | Full | [Requirements register](../01-requirements.md) and traceability |
| 4 | What stage is the project in? | Full | README current state and audit executive answers |
| 5 | What is actually implemented? | Full | README status table and [capability matrix](CAPABILITY_COVERAGE.md) |
| 6 | Which statements are target rather than as-built? | Full | README, architecture and diagram state labels |
| 7 | How do I run repository validation? | Full | README Quick Start and [playbook](../developer-onboarding.md) |
| 8 | What tests exist and what do they cover? | Full | Three harness tests; no product tests; [verification report](VERIFICATION_REPORT.md) |
| 9 | What does DevHarness do and how do I invoke it? | Full | README, [harness guide](../harness-installation-guide.md) and [repository map](../repository-map.md) |
| 10 | What is the proposed architecture? | Full | [Architecture](../03-architecture.md) and architecture delta |
| 11 | What workflows are proposed? | Full | [Workflow catalogue](../04-workflows.md#operational-workflow-catalogue) |
| 12 | What diagrams exist and how are they maintained? | Full | Diagram galleries, repository map and audit section 10 |
| 13 | What security controls are required? | Full | [Security governance](../security-governance.md) and root security policy |
| 14 | Which source materials are confidential or local-only? | Full | [Source registry](../source-registry.md) and `.gitignore` |
| 15 | What evidence supports a PASS claim? | Full | [Verification report](VERIFICATION_REPORT.md) and playbook verification rules |
| 16 | How is the repository structured? | Partial | [Repository map](../repository-map.md) now provides the full inventory and authority map |
| 17 | What prerequisites are required? | Partial | Git/Python baseline documented; product stack and Graphviz/Mermaid renderer remain unselected |
| 18 | Can I clone the default branch and start? | Partial | README/onboarding now document the acceptance-branch workaround; default `main` remains blocked |
| 19 | How do modules interact? | Partial | Target contracts are documented; no executable interfaces or as-built behavior exists |
| 20 | How should credentials be handled? | Partial | Secret exclusion and least-privilege rules exist; no product environment/provider credentials exist |
| 21 | Why Jira and GitHub, and how do they relate? | Partial | Jira-first policy is documented; Jira access and real workflow execution remain blocked |
| 22 | How should a coding agent be configured? | Partial | `AGENTS.md` and playbook scope agent use; no executable router/enforcer exists |
| 23 | How do I intake a task? | Partial | Playbook task contract and readiness rules added; real Jira intake remains blocked |
| 24 | How do I create and name a branch? | Partial | Playbook provides current acceptance-base and future Jira-key conventions |
| 25 | How do I implement a scoped change? | Partial | Playbook and scoped-task instruction added; no product codebase exists to demonstrate |
| 26 | How do I open/review a PR? | Partial | Playbook and contribution protocol added; real reviewers and approval count remain unassigned |
| 27 | What should I do next? | Partial | Owner guide and roadmap provide gated actions; owner decisions remain required |
| 28 | Which skills are available and how are they invoked? | Missing | Playbook distinguishes three manual harness instruction files, user-level Diagram Design and proposed catalogue |
| 29 | How do I debug a failure? | Missing | Playbook adds reproduction, hypothesis, minimal fix, regression evidence and escalation table |
| 30 | How do I commit safely? | Missing | Playbook adds specific-path staging, staged review, authorized commit and hook rules |
| 31 | How do I sync/update a task branch? | Missing | Playbook adds fetch/rebase, shared-branch caution and conflict procedure |
| 32 | What do I do when blocked or handing off? | Missing | Playbook adds stop/escalation and handoff checklist; [HANDOFF.md](HANDOFF.md) records current state |

The remediation makes the linked README/onboarding package sufficient for controlled documentation/harness work. It does not answer product installation, deployment or live-operation questions because those capabilities do not exist.

Factual conflicts identified and remediated by this audit package:

- Diagram plugin is loaded/exposed, not absent from the current session.
- Three physical harness skill files exist; the larger catalogue remains proposed and no loader executes it.
- Harness initialization is non-clobbering but may append `.gitignore` rules; it is not strictly non-mutating.
- Harness `ingest` reads `<project>/docs/00-original`, not `.harness/docs/00-original` by default.
- Security features have historical read-back but current state is unverified.
- GitHub rendering of supplemental Mermaid is intended behavior, not locally verified rendering.

## 14. Clean-clone onboarding result

| Scenario | HEAD / contents | Checks | Result |
|---|---|---|---|
| Default `main` clone | `560cf0d…`; only `README.md` containing `# Ecomdy` | Validator and harness absent | **BLOCKED** for onboarding |
| Acceptance-branch clone | `f516230…`; 225 tracked files | `python scripts/validate.py` PASS; `python .harness/harness.py doctor` exit 0/advisory; 3/3 tests OK; `python .harness/scripts/validate.py` PASS | **PASS** for documentation/harness only |
| Harness `init` in empty project | Existing files preserved; missing starter files created | Exit 0 | **PASS** for scaffolding |
| Harness `ingest` in empty project | No original inputs present | Exit 0; zero files inventoried | **PASS** with empty-input limitation |

A successful acceptance-branch clone does not make the default branch usable and does not verify product setup.

## 15. Two-workspace isolation result

Two independent temporary clones of `f516230…` used branches `sim/workspace-a` and `sim/workspace-b`. Each received a separate disposable marker file:

- `docs/setup/SIM_WORKSPACE_A.md`
- `docs/setup/SIM_WORKSPACE_B.md`

Both workspaces independently passed the product validator, harness doctor, 3/3 tests and harness validator. `git status --short --branch --untracked-files=all` showed only each workspace's own marker. No merge, push or shared-repository mutation occurred.

**Conclusion:** filesystem/Git isolation works for documentation tasks. Parallel product work still requires contract-first ownership, real reviewers, stable API/schema contracts and a Jira/decision flow.

## 16. Resource efficiency and bounded context

Current strengths:

- Local-first standard-library validators and harness commands.
- Documentation separated by purpose; explicit source authority and current-state portals.
- Manual handoff and scoped-search guidance.
- Bounded Diagram Design extractor with source/node/edge/statement limits.

Current gaps:

- No automatic context compiler, incremental repository index, retrieval benchmark or token accounting.
- Harness budgets are not enforced.
- No persisted run checkpoint, resume or duplicate-work protection.
- No measured provider latency, cost, accuracy or Vietnamese-quality baseline.

Recommended posture:

1. Keep deterministic work deterministic and cache/hash before any model call.
2. Load only task-relevant documents; use repository map and workflow/module IDs to scope reads.
3. Record exact commands, exit codes and evidence artifacts; never invent token usage.
4. Add checkpoint/budget enforcement only after a real bounded task demonstrates the need and owner approves the contract.
5. Measure context/token/cost/latency on a representative permitted fixture set before adding routers or multi-agent orchestration.

## 17. Collaboration readiness

**Ready now:** read-only review, documentation edits, local validation, draft PR preparation and fixture/specification work.

**Not ready:** parallel product implementation, live collection, paid AI, production migrations, deployment, automated publication or enforceable scheduled operation.

Required before parallel product work:

- PR #1 decision and authenticated protection/security read-back.
- Real reviewer/module ownership and approved review count.
- Jira authorization or an explicitly approved temporary internal-ID workflow.
- Contract-first API/schema/migration ownership.
- Approved source/market/retention/provider/budget decisions.
- Vertical-slice implementation gate `VS01-G6`.

## 18. Prioritized blockers

| Priority | Blocker | Why it matters | Resolution evidence |
|---|---|---|---|
| P0 | PR #1 remains unmerged; default clone is unusable | New contributors cannot follow the documented quick start from `main` | Owner review/approval, authenticated checks and normal merge |
| P0 | Current protection/security settings unverified | Merge and secret-handling guarantees cannot be independently accepted | Authenticated API/settings read-back |
| P0 | No real owners/reviewers or approval count | Independent review and parallel work cannot be enforced | Approved role-to-person mapping and review policy |
| P0 | Jira unavailable | Delivery state, assignments and sprints cannot be operationalized | Authorized Jira tenant/project and verified import |
| P1 | Source/market/retention/provider/budget decisions unresolved | Live collection, storage and AI calls are unauthorized | VS01-G1–G4 decision records |
| P1 | No product runtime or contracts | No product behavior can be tested or demoed | Approved vertical slice, contracts, fixtures and implementation evidence |
| P1 | No CI-safe Mermaid renderer | Rendering/visual acceptance is not reproducible | Pinned toolchain, lockfile, security review and CI evidence |
| P2 | Harness enforcement/checkpointing absent | Configuration cannot bound autonomous execution | HARD-01/02/03 and CTX-01 decision plus tests if approved |
| P2 | Interviews, feedback and success thresholds absent | Product value and suitability cannot be claimed | Five seller interviews, Content Team feedback and approved rubric |

## 19. Security, privacy and source governance

- Public repository contains no credentials or product runtime; local originals remain ignored.
- Source allowlist is empty and `runtime_automation` is false.
- No live source collection, private-community ingestion, paid AI, production data or publication is authorized.
- Source text, URLs, prompts and model output remain untrusted; no arbitrary URL fetcher may be introduced.
- Approval must bind to exact content hash/version; any edit creates a new draft.
- Current GitHub security settings must be re-read with authorization; documentation is not current-state proof.
- Provider retention/training/region/contract decisions are required before non-public material is sent to any provider.

## 20. Ordered owner action plan

### Gate 0 — make the baseline integrable

1. Review PR #1 and the Phase 0 acceptance evidence; approve, request changes or reject explicitly.
2. Obtain authenticated read-back of `main` protection, required checks, review count, admin enforcement and security features.
3. Map role placeholders to real reviewers/owners; approve the minimum review policy before adding `CODEOWNERS`.
4. Merge only through the normal protected process after approval; then retarget/rebase PR #2 without force-push.

**Exit evidence:** default `main` clone contains the validator/harness/docs and passes the documented checks; current governance settings are recorded.

### Gate 1 — make delivery traceable

1. Authorize the Jira tenant/project model or approve a time-boxed internal-ID workflow.
2. Import only approved CSV rows; retain stable internal IDs and record real Jira keys.
3. Test one Jira–GitHub PR/branch link before broader automation.
4. Assign capacity, sprint cadence and task owners; do not invent dates or commitments.

**Exit evidence:** one real task moves through Backlog → Ready → In Progress → In Review with a linked PR and recorded acceptance checks.

### Gate 2 — approve the first product slice

1. Approve platform/market/source profile and fixture/live mode.
2. Approve raw/reference retention, deletion and access behavior.
3. Approve authoritative-source and cross-source verification policy.
4. Approve database/API contracts and migration ownership.
5. Approve provider data policy, evaluation set and budget before any live model call.
6. Approve `VS01-G1`–`VS01-G6` before substantive product code.

**Exit evidence:** signed decision records, reviewed contracts and a controlled fixture corpus.

### Gate 3 — implement and prove the vertical slice

1. Land the contract-only change first.
2. Implement collector/raw capture, deterministic processing, evidence store/fake provider, digest/review API and integration CI in dependency order.
3. Run happy-path, contradiction, stale, malformed, timeout, hallucinated-citation, idempotency and approval-invalidation tests.
4. Record independent review and a fixture-only demo rehearsal.

**Exit evidence:** all Slice 01 acceptance criteria pass with exact commands and artifacts; no live or paid action is implied.

### Gate 4 — expand only from evidence

1. Add freshness audit and channel drafts after the core evidence path is proven.
2. Complete five seller interviews, Content Team feedback and measured time/suitability evaluation.
3. Evaluate trends, Telegram, assistant, notifications, routing and multi-agent patterns separately.
4. Add production operations, deployment and harness hardening only after measured requirements and owner approval.

## 21. Recommended next prompt

> Act as the independent Technical Lead for Ecomdy. Start from the latest actual repository state and `docs/setup/COMPREHENSIVE_AUDIT.md`. Review PR #1 and the authenticated protection/security evidence without merging. Produce a decision-ready checklist for VS01-G1–VS01-G6, identifying each required owner decision, exact artifact to update, acceptance evidence and stop condition. Do not implement product code, call external sources/models, mutate Jira, change permissions, push, merge or fabricate assignments. Preserve all existing diagrams, capability IDs and uncommitted acceptance work.

## Evidence limitations

- Current GitHub protection/security settings were not independently readable with the available unauthenticated API access.
- Jira was not available; no Jira state is claimed.
- No Mermaid renderer was installed or run; parser extraction is not rendering.
- Existing static assets were structurally validated, not freshly rendered or fully visually re-reviewed.
- No Ecomdy application, product test, live source, model call, interview, benchmark or deployment exists to verify.
- All effort ranges, cadence and sprint sequences remain proposals until capacity and deadlines are approved.
