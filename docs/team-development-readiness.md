# Team Development Readiness

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Status:** Proposed operating model. Role labels are placeholders, not assignments. Branch protection, reviewer count and `CODEOWNERS` require owner approval and authenticated verification.

## 1. Current integration state

- Permanent integration branch: `main` only.
- Existing temporary baseline branch: `setup/phase-0-audit`, represented by draft PR #1.
- Existing temporary acceptance branch: `docs/phase-0-acceptance`, represented by stacked draft PR #2.
- No release branch, environment branch or long-lived feature branch is approved.
- PR #1 and PR #2 remain unmerged. PR #2 targets PR #1's branch to avoid duplicate changes against `main`.
- Jira is authoritative for delivery planning once authorized; no Jira project, issue or key is currently verified.

## 2. Branch model

| Branch | Purpose | Lifetime | Merge path |
|---|---|---|---|
| `main` | Accepted source, documentation and CI configuration | Permanent | Protected PR only |
| `setup/phase-0-audit` | Baseline setup work for PR #1 | Temporary until PR #1 resolves | PR to `main` after human approval |
| `docs/phase-0-acceptance` | Acceptance and Phase 1 documentation | Temporary until PR #2 resolves | Retarget/rebase to `main` after PR #1 merges |
| `<type>/<jira-key>-<short-kebab>` | One approved task | Short-lived | PR to current `main` or explicitly approved stack |
| `<type>/<short-kebab>` | One approved task before Jira keys exist | Short-lived | Same review path; stable local task ID recorded |
| `spike/<short-kebab>` | Time-boxed investigation | Short-lived; no direct product merge | Findings PR or documented discard decision |

Allowed types: `docs`, `feat`, `fix`, `chore`, `refactor`, `test`, `ci`, `spike`. Do not use person names as permanent branches. Do not force-push, delete shared branches or change `main` directly.

## 3. Task flow

1. Start from the latest `main` unless an explicit stack is approved.
2. Record stable requirement/capability/task IDs, objective, allowed/forbidden paths, dependencies, acceptance criteria, verification commands, budget and stop conditions.
3. Use the real Jira key only after Jira authorization and import; until then use SET/ECO/VS01/DIAG/PRGOV/COL IDs without fabricating a Jira key.
4. Create one task-scoped branch and keep the diff minimal.
5. Run deterministic local checks before requesting review.
6. Open a draft PR early for contract/security feedback when useful; mark ready only when evidence is complete.
7. Obtain independent review and any specialist approval required by the change.
8. Merge only through the approved GitHub process; update Jira/handoff after actual merge.

## 4. Module and ownership boundaries

| Role placeholder | Primary scope | Review responsibility |
|---|---|---|
| Project Owner | Product scope, source policy, budget, merge/deploy/publish decisions | Final acceptance and authorization boundaries |
| Technical Lead / Architect | Cross-module contracts, architecture decisions, migration strategy | Contract compatibility and architectural impact |
| Source & Collection Owner | M01–M03, source allowlist, connectors, jobs | Terms, rate limits, timeout/retry and provenance |
| Processing & Evidence Owner | M04–M11, normalization, dedup, claims and verification | Deterministic behavior, evidence and temporal integrity |
| Knowledge & API Owner | M12, persistence contracts, API resources and migrations | Schema/API compatibility, retention and query safety |
| Content & Editorial Owner | M13–M17, digest/drafts/review/approval | Citation preservation and exact-version approval |
| Platform & Quality Owner | CI, test strategy, security checks, deployment readiness, diagram validation | Reproducibility, failure visibility and regression coverage |
| DevHarness Owner | `.harness/` changes and parity with any future standalone release | Isolation from product runtime and bounded execution |
| Independent Reviewer | Assigned task diff | Correctness, tests, scope, security and documentation |

The Project Owner must map these roles to real people or teams before they become enforceable. No names, assignments or approval counts are invented here.

## 5. Review policy

### Every change

- Author records exact checks and skipped checks.
- At least one reviewer other than the author reviews correctness, scope, security and evidence.
- Requirement/capability traceability and relevant docs are updated.
- Secrets, local-only originals and unnecessary personal data are excluded.

### Specialist review required before merge

| Change | Required review role |
|---|---|
| Source allowlist, connector permissions, retention or publication behavior | Project Owner + Source/Collection + Security |
| Public API or shared event/claim/evidence contract | Technical Lead + Knowledge/API + affected consumer owner |
| Database migration | Knowledge/API + Technical Lead; destructive migrations require Project Owner approval |
| AI provider, prompt/template contract, verification policy or budget | Processing/Evidence + Security/AI owner + Project Owner |
| Branch protection, CI permissions, deployment or secrets | Platform/Quality + Project Owner |
| Diagram source/artifact changes | Diagram/Platform reviewer; visual inspection for changed outputs |

These are proposed requirements. Current branch protection cannot be revalidated and no minimum approval count is claimed. Do not add `CODEOWNERS` with fictional handles; add it only after real owners approve the mapping.

## 6. API and schema coordination

1. Use contract-first changes for shared APIs, events and database entities.
2. Update [api-design.md](api-design.md), [database-design.md](database-design.md) and affected module contracts in the same task or a preceding contract PR.
3. Define compatibility: additive, breaking or behavior-changing. Breaking changes require a version/migration plan.
4. Add request/response fixtures and contract tests before dependent implementation branches.
5. Assign one migration owner per change. Do not allow parallel unreviewed edits to the same migration chain.
6. Prefer forward-compatible, reversible migrations; destructive operations require explicit approval and recovery evidence.
7. Run integration tests against the agreed database/runtime before merge once the stack is approved.
8. A future OpenAPI artifact must be generated from implemented contracts and checked in CI; it does not exist yet.

## 7. Integration cadence

- Proposed active-development integration: at least twice weekly, subject to reviewer capacity.
- Contract-only PRs integrate before dependent feature branches.
- Keep task branches small and rebase/merge from the approved base without rewriting shared history.
- Run CI on every PR; do not treat a passing documentation validator as product verification.
- Record integration conflicts and contract decisions in the handoff and decision log.
- Release, deployment and production promotion cadence remain undecided.

## 8. Local setup and verified quick start

Prerequisites verified by direct executable checks: Git 2.50.1, Python 3.11.9 and Node 22.18.0. An earlier environment notice reported Node 24.22.1; the discrepancy is recorded and the direct executable result is used for current commands. Graphviz and Mermaid CLI are not installed. Default `main` currently contains only a one-line README because PR #1 is unmerged. The following commands are verified for the acceptance-branch documentation/harness baseline:

```bash
git clone --branch docs/phase-0-acceptance https://github.com/macxuanhoa/Ecomdy.git
cd Ecomdy
python scripts/validate.py
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -v
python .harness/scripts/validate.py
```

After PR #1 merges, verify a default-branch clone before replacing this branch-specific instruction. There is no Ecomdy application install, migration, product test, server or deployment command yet. Do not add speculative commands to Quick Start. When the first slice is approved, add only commands that have been run successfully in a clean environment.

## 9. Jira and backlog handoff

- Jira remains blocked by missing authorized site/connector/credential and owner-approved project model.
- Use [setup/JIRA_SETUP_PLAN.md](setup/JIRA_SETUP_PLAN.md) for setup and [setup/JIRA_IMPORT_BACKLOG.csv](setup/JIRA_IMPORT_BACKLOG.csv) for import preparation.
- CSV rows use stable internal IDs; the `Jira Key` column remains empty.
- Do not create a parallel GitHub Projects backlog.
- After authorization, import/create only owner-approved rows, record real keys, verify permissions and test one PR link before broader automation.

## 10. Diagram engineering readiness

- Qoder market Plugin `diagram-design` 2.6.131 is installed, enabled and exposed as a Skill in the current audit session.
- After a one-line quoted-label compatibility fix, its reviewed bounded extractor parsed 56/56 Mermaid sources: 482 nodes, 499 edges and zero dangling edges. One isolated secret-store node is intentional. Mermaid/DOT parity passed 26/26 on unchanged paired inputs and static assets passed 26/26. No Mermaid source was rendered locally.
- Mermaid CLI was evaluated but not selected or installed. Rendering and visual acceptance remain open.
- Preserve all 56 existing sources and valid artifacts. Add/replace only task-relevant diagrams after a pinned, CI-safe validation tool is approved.
- User-level plugin installation and parser extraction do not make fresh-clone Mermaid rendering reproducible.

## 11. Handoff checklist

At each safe stop, record:

- repository, branch, HEAD SHA and clean/dirty state;
- PR number, base/head, review state and actual CI results;
- changed files and stable task IDs;
- checks run with exact outputs and any skipped/blocked checks;
- source/security/retention/diagram impacts;
- open decisions, blockers and owner actions;
- next task and explicit stop/rollback conditions.

Update [setup/HANDOFF.md](setup/HANDOFF.md) and [setup/EXECUTION_STATUS.md](setup/EXECUTION_STATUS.md) from observed state. Historical Phase 0 evidence must remain historical.

## 12. Readiness verdict

The repository has a usable documentation/harness onboarding path and a proposed collaboration model. It is **not yet team-ready for parallel product implementation** until real owners/reviewers, Jira access, API/schema ownership, migration policy, source/provider decisions and the vertical-slice approval are confirmed.

## 13. Dependency and parallel-work matrix

“Can parallelize” means work can proceed against approved contracts without editing the same files. It does not authorize product implementation or invent staff assignments.

| Workstream / modules | Must exist before implementation | Can proceed in parallel with | Hands off to | Owner role placeholder | Current state |
|---|---|---|---|---|---|
| Track A — team infrastructure | Owner authorization; reviewed PR stack | Track B planning; Track C documentation | Reviewers, Jira keys, protected integration path | Project Owner + Technical Lead + Platform/Quality | Partly prepared; external authorization and authenticated read-back blocked |
| Track B — Minimum Viable DevHarness P0 | Approved H0 scope and security boundaries | Track A setup; Track C contract/fixture documentation | Scoped context, verification and handoff for all tracks | DevHarness Owner + Platform/Quality | Plan only; no new command implemented |
| Diagram source/tooling | Reviewed tool identity; task-scoped source change | Track A/B documentation | Validated source and, later, approved renderer | Diagram/Platform reviewer | 56/56 parser pass; Mermaid render not installed |
| M01–M03 source and collection | VS01-G1; contract freeze from VS01-G3 | M04–M06 after contracts are stable | Normalized source/capture contracts | Source & Collection Owner | Specification only |
| M04–M06 normalization, dedup and classification | Source/capture contracts; VS01-G3 | M09–M11 against the same fixtures | Immutable article versions and claim candidates | Processing & Evidence Owner | Specification only |
| M12 knowledge store | VS01-G2 retention; VS01-G3 schema/DB decision | Verification and digest contract work | Persistence/query contracts to all consumers | Knowledge & API Owner | Specification only |
| M09–M11 claims and verification | M04–M06/M12 contracts; VS01-G4 adapter policy | Digest aggregation against fixed fixtures | Eligible evidence and verification states | Processing & Evidence Owner | Specification only |
| M13–M17 digest and editorial | Eligible claim contracts; VS01-G5 review roles | UI/API work after contract freeze | Versioned digest preview and review evidence | Content & Editorial Owner | Specification only |
| M18–M20 validation/extensions | Accepted MVP evidence and new scope approval | Later discovery only | Post-MVP decision | Project Owner + affected module owner | Specification only |

Critical path: approved source/retention/architecture decisions → contract-only freeze → collector/processing/evidence work in parallel → digest integration → independent demo acceptance. Track B P1 is not a prerequisite for fixture-only product work; only the approved deterministic checks needed by the task are prerequisites.

## 14. Track A/B/C execution boundaries

| Track | Can start now without product code | Blocked until | Must not do |
|---|---|---|---|
| A — Team Infrastructure | Review PR stack; prepare reviewer-role mapping; prepare Jira import and onboarding test plan | Owner assigns real people; Jira site/project authorization; authenticated GitHub settings read-back | Invent owners, create Jira issues, change protection/permissions or claim default-branch onboarding |
| B — Minimum Viable DevHarness | Review H0-01–H0-08 plan; identify reusable validators and fixtures | Owner approves implementation scope, execution policy and tests | Add proposed commands to docs as if implemented; enable shell execution, network or paid AI |
| C — Ecomdy Product | Review VS01 plan and approval pack; prepare synthetic fixture/contract proposals | VS01-G1–G6 recorded; then only fixture-only implementation | Crawl live sources, call paid AI, migrate production data, deploy or publish |

Track A and Track B can progress in parallel after their own approvals. Track C documentation can progress alongside them, but Track C implementation waits for the six gates. A blocker in one track must not silently expand another track's authority.

## 15. Shared-file ownership and coordination

| Shared path / concern | Coordination owner role | Rule |
|---|---|---|
| `README.md`, `docs/README.md`, `CONTRIBUTING.md`, `AGENTS.md` | Platform/Quality + Technical Lead | One integration owner per cross-track edit; review navigation and status claims together |
| `docs/setup/HANDOFF.md`, `EXECUTION_STATUS.md`, `TASK_REGISTRY.md`, `VERIFICATION_REPORT.md`, `DECISION_LOG.md` | Platform/Quality | Update from observed evidence; do not rewrite historical results |
| `.harness/**` | DevHarness Owner | Keep isolated from product runtime; preserve standalone/embedded boundary |
| `docs/diagrams/**`, `.harness/docs/diagrams/**`, `scripts/render_diagrams.py`, `scripts/validate.py` | Diagram/Platform reviewer | One owner per source/artifact set; no parallel regeneration of the same output |
| Requirements, architecture, module, API and database specifications | Technical Lead + affected module owner | Contract-first PR; record compatibility and affected consumers |
| Future application modules | Assigned module owner | One task branch; no cross-module edits without the affected owner's review |
| Future migration chain | One Knowledge/API migration owner | Single ordered chain; forward-only reviewed changes; no parallel migration authors |
| `.github/**`, protection, secrets and deployment configuration | Platform/Quality + Project Owner | Explicit authorization and authenticated read-back required |

Coordination rules:

1. Announce the shared file and intended change in the task record before editing.
2. Keep shared-file diffs small and separate from unrelated feature work.
3. Use contract-first branches for APIs, schemas and shared events; consumers branch from the approved contract.
4. Give each migration chain one owner and each generated artifact one producer.
5. Sync from the approved base without force-pushing; resolve conflicts explicitly.
6. If two tasks need the same shared file, sequence them or assign one integration owner rather than merging unreviewed competing edits.
7. Record cross-track decisions in the decision log and handoff, not only in chat.

## 16. Worked developer task — OPS-03 compatibility remediation

This example uses the controlled diagram change executed in the current acceptance branch. It is a documentation/tooling task, not product implementation.

| Field | Worked example |
|---|---|
| Stable task ID | `OPS-03`; no Jira key exists. `DIAG-01` remains plugin verification and `DIAG-02` remains CI-safe parser/renderer pinning. |
| What | Quote one Mermaid edge label and add the shared diagram tooling guide |
| Why | The installed extractor rejected a semicolon inside an unquoted pipe label; contributors also lacked a precise installed-capability guide |
| Allowed paths | `.harness/docs/diagrams/19-debugging-workflow.mmd`, `docs/setup/DIAGRAM_TOOLING.md`, `docs/README.md` and linked status evidence |
| Forbidden paths | Other diagram sources/assets, Qoder plugin cache, dependency manifests, product code, credentials and local originals |
| Dependencies | Reviewed Diagram Design 2.6.131 package; existing valid sources; approved documentation branch |
| Tool / skill | Python standard-library extractor; `diagram-design:diagram-design` for the separate smoke test; repository validators |
| Harness capability | Existing validation only; no new harness command |
| How | Change only the label quoting; run full extraction; run both validators; document parser/render limits and smoke evidence |
| Expected result | 56/56 sources parse with unchanged extractor-normalized label text and endpoints; no dangling edge; no claim of Mermaid rendering |
| Actual verification | 56/56 parsed; 482 nodes; 499 edges; 101 labeled edges; 0 dangling edges; both repository validators passed |
| Recovery | Revert only the one-line compatibility change through a reviewed commit if a supported renderer later proves a problem; do not regenerate unrelated diagrams |
| Next step | Owner selects and approves a pinned Mermaid parser/renderer before rendering acceptance is claimed |

The remediation commit `27b628ba1fd6e91ac7365859606c8501c1f4c884`, PR #2 link and CI evidence are recorded in [setup/HANDOFF.md](setup/HANDOFF.md) and [setup/VERIFICATION_REPORT.md](setup/VERIFICATION_REPORT.md). Later review-fix commits are tracked on PR #2 rather than pinned in this example.

## 17. Delegation and assignment rules

- **Agent-delegable now:** read-only source/evidence lookup; deterministic validation; draft documentation from verified facts; diagram smoke generation in an isolated temporary directory; diff review against explicit scope.
- **Agent-delegable only after task approval:** implement one bounded H0 capability with tests; update one approved diagram source; prepare a contract-only PR. The agent must not choose new dependencies, permissions, paid services or product scope.
- **Human-only:** assign real owners/reviewers; approve Jira/GitHub permissions; approve VS01 gates; authorize dependencies, live collection, AI budget, migration, merge, deployment and publication.
- **Team-assignable after owner mapping:** independent documentation tasks, harness capabilities with disjoint paths, fixture/contract tasks after G3, and module implementation after G6. Shared files and migration chains remain single-owner.
