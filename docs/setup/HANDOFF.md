# Handoff

## Current working state

- Repository: `https://github.com/macxuanhoa/Ecomdy.git`
- Remote `main`: `560cf0d2ecaf862749edbe9b8823eebc4e0327a0` at the last verified read-back.
- Phase 0 acceptance package: `f5162302aae3b9ab5e5798d722cfbfa60d9164b9`.
- Preservation commit: `4cfab07b8a163715ad608e5aaff6628b990d59a5` — 33 checkpoint files committed after a hashed backup.
- Current branch: `docs/phase-0-acceptance`. Independent-review fixes at `2dbe287365e2313c7e83daf62a074f0782f13990` were pushed and validated; later review-fix commits are tracked on [PR #2](https://github.com/macxuanhoa/Ecomdy/pull/2), which is authoritative for the moving head.
- PR #1: open and Ready for review, base `main`, head `4bddc925c941979da60b1250ec4d139381776e22`; mergeable/clean; CI success; no submitted reviews or requested reviewers/teams.
- PR #2: open draft, base `setup/phase-0-audit`. The `2dbe287365e2313c7e83daf62a074f0782f13990` checkpoint had successful `validate` runs, mergeable/clean state and zero submitted reviews or requested reviewers/teams. Later status-correction or review-fix commits may supersede that head; re-read PR #2 after each push.
- Neither PR is merged. Owner review/merge remains pending; authenticated protection/security read-back was completed on 2026-11-28 and changed no settings.
- The repository is a documentation/design scaffold plus a bounded advisory harness. No Ecomdy product runtime is implemented.
- Current local checks pass within scope: both validators, 3/3 harness tests, Python compile, harness doctor, JSON/YAML syntax, 39-row Jira CSV integrity, 70-capability matrix integrity, 26 SVG/PNG asset checks, diff whitespace and nonignored-file hygiene.
- Default `main` clone is not usable for onboarding; historical acceptance-branch clone and two isolated workspaces passed documentation/harness checks.
- The 70-capability matrix is unchanged; all M01–M20 remain SPECIFICATION ONLY. All 56 Mermaid sources and 26 DOT/SVG/PNG sets are preserved; one Mermaid edge label was quoted for extractor compatibility and no repository artifact was regenerated.
- Diagram Design Plugin 2.6.131 is installed at user scope. Its extractor passes 56/56 sources: 482 nodes, 499 edges, 101 labeled edges and zero dangling edges. An isolated HTML/SVG/PNG smoke flowchart passed offline self-check and visual/mobile/network checks. No Mermaid source was rendered; the smoke PNG is 960×601 against a 960×600 viewBox.
- Jira remains blocked. The 2026-11-28 recheck found no Jira CLI, Jira/Atlassian MCP tool or Jira/Atlassian environment variable name. No Jira data was fabricated; GitHub Projects V2 is not the primary board.
- Direct tool checks return Git 2.50.1, Python 3.11.9 and Node 22.18.0. An earlier environment notice reported Node 24.22.1; the discrepancy is recorded rather than silently normalized.

## Read first

1. [Comprehensive audit](COMPREHENSIVE_AUDIT.md) — historical snapshot, with a pointer to later remediation.
2. [Repository map](../repository-map.md)
3. [Project Owner guide](../project-owner-guide.md)
4. [Developer operations matrix](../developer-operations.md)
5. [Minimum Viable DevHarness plan](../minimum-viable-harness-plan.md)
6. [Team development readiness](../team-development-readiness.md)
7. [VS01 owner approval pack](../vs01-owner-approval-pack.md)
8. [Diagram tooling](DIAGRAM_TOOLING.md)
9. [Phase 1 transition checkpoint](PHASE_1_TRANSITION.md) — historical checkpoint.
10. [Phase 0 acceptance](PHASE_0_ACCEPTANCE.md)
11. [Capability coverage matrix](CAPABILITY_COVERAGE.md)
12. [Phase 1 requirements delta](../phase1-requirements-delta.md)
13. [Phase 1 architecture delta](../phase1-architecture-delta.md)
14. [First vertical-slice plan](../vertical-slice-01-plan.md)
15. [Execution status](EXECUTION_STATUS.md), [blockers](BLOCKERS.md) and [verification report](VERIFICATION_REPORT.md)
16. [Jira setup plan](JIRA_SETUP_PLAN.md) and [import-ready backlog](JIRA_IMPORT_BACKLOG.csv)

## Completed in the controlled remediation

- Preserved and classified the 33-file Phase 1/comprehensive-audit checkpoint without rewriting Phase 0 history.
- Committed the preserved checkpoint as `4cfab07b8a163715ad608e5aaff6628b990d59a5`.
- Expanded the root README into an operational entry point covering purpose, status, target, architecture, workflows, structure, setup, agents, tools, commands, Jira/GitHub, branching, testing, diagrams, roadmap and next actions.
- Added a 13-action developer operations matrix with what/why/how/tool/skill/harness/status/expected result/verification/recovery/next step.
- Added a dependency-aware P0/P1 Minimum Viable DevHarness proposal; no proposed command is represented as implemented.
- Applied the one-line Mermaid quoted-label compatibility fix and verified 56/56 extraction.
- Generated and inspected an isolated Diagram Design smoke flowchart; documented tool identity, hashes, commands, user-scope/CI boundaries and the PNG dimension anomaly.
- Revalidated Jira availability and recorded the exact owner authorization path without creating data.
- Added the team dependency matrix, shared-file coordination rules, Track A/B/C boundaries, worked developer task and plain-language VS01-G1–G6 approval cards.
- Reconciled current status, task registry, blockers, decisions, capability overlay, repository map and verification evidence while preserving historical audit snapshots.
- Pushed remediation commit `27b628ba1fd6e91ac7365859606c8501c1f4c884`; both `validate` runs passed and PR #2 remained mergeable/clean with zero reviews.
- Addressed the independent review findings at `2dbe287365e2313c7e83daf62a074f0782f13990`: stable task ID reconciliation, historical/current evidence labels, render-claim limits, portal numbering and fail-closed untracked-path semantics. Later review-fix heads are tracked on PR #2 rather than pinned here.
- Completed authenticated GitHub governance/security read-back on 2026-11-28, marked PR #1 Ready for review and updated both PR descriptions with the verified current evidence without changing repository settings.

## Continue with

1. PR #2 follow-up push and CI for `2dbe287…` are verified. After this or any later follow-up push, re-read the PR #2 head, `validate` CI, mergeability and review state; do not infer remote success from local checks.
2. Obtain the Project Owner's explicit human review and merge decision on PR #1. Authenticated governance read-back is complete; the current protection requires zero approving reviews, but the project directive still requires human approval.
3. Keep both PRs unmerged until approved. After PR #1 merges, retarget or rebase PR #2 onto `main` through the normal reviewed process; do not force-push.
4. Assign real reviewers/module owners and approve the review count, `CODEOWNERS`, API/schema ownership and migration ownership.
5. Authorize Jira using `JIRA_SETUP_PLAN.md`; provide the real site/access method through an approved secret channel, import only approved CSV rows and record real keys after verification.
6. Record VS01-G1–G6 decisions using `vs01-owner-approval-pack.md`. No substantive product code starts before G6; fixture approval does not authorize live collection, paid AI, production migration, deployment or publication.
7. Select and pin an independent CI-safe Mermaid parser/renderer if rendering acceptance is required. Preserve existing sources, inspect every changed output and verify PNG dimensions explicitly.
8. Decide whether to implement, defer or reject each H0/P1 capability in `minimum-viable-harness-plan.md`. The harness remains advisory until approved enforcement is implemented and tested.
9. Verify a default-branch clone only after PR #1 merges; do not claim new-contributor onboarding before that test passes.

## Stop boundaries

Do not deploy, auto-publish content, collect from external sources, call paid models, mutate Jira, change protection, merge PRs or perform production migrations without separate authorization. Do not force-push, invent team/Jira/source/test/metric data, or represent target architecture as implemented. At the next safe stop, record the actual commit, changed files, checks, blockers and next task.
