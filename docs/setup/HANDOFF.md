# Handoff

## Current working state

- Repository: `https://github.com/macxuanhoa/Ecomdy.git`
- Audited setup baseline: `4bddc925c941979da60b1250ec4d139381776e22`.
- Remote `main`: `560cf0d2ecaf862749edbe9b8823eebc4e0327a0`.
- PR #1 head: `setup/phase-0-audit`, open, draft and unmerged; owner approval is required before merge.
- Acceptance work: local branch `docs/phase-0-acceptance`, based on the audited setup head; no commit, push, merge, installation or paid-service action has been performed.
- Public repository; original source files must remain excluded.
- Current repository is a documentation/design scaffold plus a bounded advisory harness. No Ecomdy runtime is implemented.
- Product/harness validators, 3/3 harness tests and two fresh-clone checks passed for the audited baseline. Push and PR CI runs passed.
- Diagram evidence covers 56 Mermaid IDs and 26 static DOT/SVG/PNG sets. Existing static artifacts were inspected; 30 Mermaid-only diagrams still need approved parser/render tooling.
- Jira is blocked by missing authorized access. No Jira data was fabricated; GitHub Projects V2 is not the primary board.
- Current branch-protection/security settings need owner-authenticated revalidation; Phase 0 API revalidation was denied.

## Read first

1. [Phase 0 acceptance](PHASE_0_ACCEPTANCE.md)
2. [Capability coverage matrix](CAPABILITY_COVERAGE.md)
3. [Jira setup plan](JIRA_SETUP_PLAN.md)
4. [Execution status](EXECUTION_STATUS.md)
5. [Blockers](BLOCKERS.md)

## Continue with

1. Obtain the Project Owner's decision on the acceptance package and PR #1.
2. Keep PR #1 unmerged until approval. Use one setup PR or a clean post-merge acceptance PR; do not create overlapping PRs to `main`.
3. Authorize Jira and execute the setup plan only after the owner supplies the real site/project/permission details.
4. Assign real reviewers/module owners and decide the branch/PR/CODEOWNERS policy.
5. Select and pin diagram tooling before any regeneration; preserve existing valid artifacts.
6. Approve or defer HARD-01/02/03 and CTX-01; the harness remains advisory until enforcement is implemented and tested.
7. Do not start product implementation until MVP, sources, provider/data policy, budget and deployment constraints are approved.

Do not deploy, auto-publish content, collect from external sources, enable paid services, force-push, or represent target architecture as implemented. At the next safe stop, record the actual commit, changed files, checks, blockers and next task.
