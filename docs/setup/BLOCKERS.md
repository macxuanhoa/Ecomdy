# Blockers and Open Questions

## Active blockers

| ID | Blocker | Impact | Resolution path |
|---|---|---|---|
| BLK-01 | No authorized Jira Cloud site, connector, CLI or credential is available. The 2026-11-28 recheck found no Jira CLI, Jira/Atlassian MCP tool or Jira/Atlassian environment variable name. | Jira project, board, issues, sprints, automation and GitHub integration cannot be created or verified. | Owner supplies/authorizes the real site and access method, designates the administrator and approves the project model in `JIRA_SETUP_PLAN.md`; provide credentials through an approved secret store/connector and record real identifiers only after verification. |
| BLK-02 | Phase 0 API revalidation of branch protection and repository security settings returned HTTP 401. | Current protection/security state cannot be independently accepted from documentation or historical read-back. | Owner provides authenticated read-back; confirm required reviews, CI context, admin enforcement and security features before merge. |
| BLK-03 | No approved/pinned CI-safe Mermaid renderer is installed; Graphviz, `mmdc` and locally resolvable Mermaid packages are absent. Diagram Design Plugin 2.6.131 is installed at user scope and generated/exported an isolated HTML/SVG/PNG smoke flowchart. | Bounded extraction now passes 56/56 sources after a one-line quoted-label compatibility fix: 482 nodes, 499 edges and zero dangling edges. Mermaid/DOT parity passed 26/26 on unchanged paired inputs and static assets passed 26/26. No Mermaid source was locally rendered or visually accepted. | Preserve sources; select/pin an independent Mermaid parser/renderer, run it in an approved environment/CI, inspect outputs and record dimensions before claiming rendering acceptance. The smoke PNG's 960×601 result against a 960×600 viewBox remains an export detail to verify. |
| BLK-04 | Reviewer group, module owners, approval count and `CODEOWNERS` are not defined. | Independent review and safe parallel development cannot be operationalized. | Owner assigns real people and approves PRGOV-01; do not invent team members. |
| BLK-05 | First-slice source, platform/market, retention, stack, provider/budget and implementation approval gates are unresolved. | The vertical-slice plan and plain-language approval pack are ready for review, but product code, live collection, migrations and paid AI are not authorized. | Owner records VS01-G1–G6 decisions using `vs01-owner-approval-pack.md`; each live/production action retains a separate approval boundary. |
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
