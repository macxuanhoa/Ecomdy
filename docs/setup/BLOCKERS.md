# Blockers and Open Questions

## Active blockers

| ID | Blocker | Impact | Resolution path |
|---|---|---|---|
| BLK-01 | No authorized Jira Cloud site, connector, CLI or credential is available. | Jira project, board, issues, sprints, automation and GitHub integration cannot be created or verified. | Owner supplies/authorizes the Jira site and approves the model in `JIRA_SETUP_PLAN.md`; record real identifiers only after verification. |
| BLK-02 | Phase 0 API revalidation of branch protection and repository security settings returned HTTP 401. | Current protection/security state cannot be independently accepted from documentation or historical read-back. | Owner provides authenticated read-back; confirm required reviews, CI context, admin enforcement and security features before merge. |
| BLK-03 | No approved/pinned CI-safe Mermaid renderer is installed; Graphviz and `mmdc` are absent. Diagram Design Plugin 2.6.131 is installed, enabled and exposed in the current audit session; its bounded extractor ran without rendering. | Parser extraction passed 55/56 sources; `.harness/docs/diagrams/19-debugging-workflow.mmd:11` hit an extractor compatibility limit. Mermaid/DOT parity passed 26/26 and static assets passed 26/26, but no Mermaid source was locally rendered or visually accepted. | Preserve sources; select/pin an independent parser/renderer for DIAG-02, run it in CI, inspect outputs and resolve or independently verify the extractor exception before claiming rendering acceptance. |
| BLK-04 | Reviewer group, module owners, approval count and `CODEOWNERS` are not defined. | Independent review and safe parallel development cannot be operationalized. | Owner assigns real people and approves PRGOV-01; do not invent team members. |
| BLK-05 | First-slice source, platform/market, retention, stack, provider/budget and implementation approval gates are unresolved. | The vertical-slice plan is ready for review but product code, live collection, migrations and paid AI are not authorized. | Owner resolves VS01-G1–G6 in `vertical-slice-01-plan.md`; each live/production action retains a separate approval boundary. |
| BLK-06 | PR #1 remains unmerged, so default `main` contains only a one-line README. | A normal default-branch clone cannot run the documented validator or harness onboarding. | Review and merge the approved baseline through the protected process; verify a default-branch clone before removing the acceptance-branch caveat. |

GitHub Projects V2 is not a blocker for the Jira-first direction. Do not request additional GitHub Projects permissions without a specific approved requirement.

## Product evidence / owner decisions

These are not blockers to documentation setup, but they are required before the corresponding product claims or implementation work:

- Which Ecomdy-provided sources are authorized for monitoring, and under what access frequency and retention terms?
- Are the recommended source list, brand guidelines, and previously published articles available and approved for this public repository or local-only use?
- What is the approved MVP market, platform set, and acceptance threshold for reduced research time and draft suitability?
- What are the interview schedule and evidence owner for the required five seller interviews?
- What deployment environment, model/provider budget, data retention, identity, and access-control constraints apply?
- Should the bundled harness later receive a separate remote or release process? The initial packaging decision is recorded in [DEC-009](DECISION_LOG.md); a separate remote is not required to use the current `.harness/` component.
- Should HARD-01/02/03 and CTX-01 be implemented, deferred or rejected? The harness remains advisory until enforcement is tested.
