# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation now starts with the Phase 0 acceptance package and capability matrix. |
| SET-03 | Local validation and security review | Verified (local scope) | Root and harness validators, 3 harness tests, compile checks, source hashes, ignore rules and diff whitespace pass. Mermaid grammar/render and current GitHub protection/security read-back remain incomplete. |
| SET-04 | Commit setup changes | Verified (historical) | Setup commits through `4bddc925…` are on the PR branch; acceptance changes are local and uncommitted. |
| SET-05 | Push / pull request | Verified (draft PR open) | [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1) is open, draft, mergeable and clean; push/PR CI passed. Owner review/merge remains pending. |
| SET-06 | Repository metadata, security, dependency checks, and main protection | Implemented but unverified (current scope) | Earlier authenticated read-back exists; Phase 0 API revalidation returned HTTP 401. Owner-authenticated read-back is required before current acceptance. |
| SET-07 | Jira-first delivery setup | Blocked | No authorized Jira site/connector/credential. Follow `JIRA_SETUP_PLAN.md`; do not request GitHub Projects permissions or fabricate Jira data. |
| SET-08 | Bundle reusable DevHarness and validate its boundaries | Verified (starter scope) | Embedded CLI/tests/validators pass; full orchestration, config enforcement and standalone parity are not implemented. |
| SET-09 | Reconcile status and handoff | Verified | Execution status, task registry, blockers, decision log and handoff reflect baseline `4bddc925…` and the acceptance branch. |
| SET-10 | Phase 0 acceptance package | Verified (local package) | `PHASE_0_ACCEPTANCE.md`, `CAPABILITY_COVERAGE.md` and `JIRA_SETUP_PLAN.md` pass validators, 3/3 tests, compile/config/diff checks, matrix/report integrity checks and credential-pattern scan. Owner decision, commit/push and Jira access remain pending. |
