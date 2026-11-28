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

Prerequisites verified in the current environment: Git 2.50.1, Python 3.11.9 and Node 22.18.0. Graphviz and Mermaid CLI are not installed. Default `main` currently contains only a one-line README because PR #1 is unmerged. The following commands are verified for the acceptance-branch documentation/harness baseline:

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
- Its reviewed bounded extractor parsed 55/56 Mermaid sources; one source hit an extractor compatibility exception. Mermaid/DOT parity passed 26/26 and static assets passed 26/26. No Mermaid source was rendered locally.
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
