# Blockers and Open Questions

## Active blockers

| ID | Blocker | Impact | Resolution path |
|---|---|---|---|
| BLK-01 | No authorized Jira Cloud site, connector, CLI or credential is available. | Jira project, board, issues, sprints, automation and GitHub integration cannot be created or verified. | Owner supplies/authorizes the Jira site and approves the model in `JIRA_SETUP_PLAN.md`; record real identifiers only after verification. |
| BLK-02 | Phase 0 API revalidation of branch protection and repository security settings returned HTTP 401. | Current protection/security state cannot be independently accepted from documentation or historical read-back. | Owner provides authenticated read-back; confirm required reviews, CI context, admin enforcement and security features before merge. |
| BLK-03 | No approved/pinned Mermaid parser/render toolchain is installed; Graphviz and `mmdc` are absent. | Thirty Mermaid-only diagrams cannot be locally syntax-checked/rendered; reliable DOT/MMD parity is unavailable. | Owner selects tool/version after license/security review; execute DIAG-01 and inspect new artifacts. |
| BLK-04 | Reviewer group, module owners, approval count and `CODEOWNERS` are not defined. | Independent review and safe parallel development cannot be operationalized. | Owner assigns real people and approves PRGOV-01; do not invent team members. |

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
