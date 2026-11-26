# Blockers and Open Questions

## Active blockers

| ID | Blocker | Impact | Resolution path |
|---|---|---|---|
| BLK-01 | Current GitHub authorization lacks `read:project` / `write:project`; Projects V2 GraphQL requests are denied. | No GitHub Project board can be created or linked through the current credential. Other repository API writes work. | Reauthorize the GitHub integration with Projects access or provide a connected Projects-capable app. Do not paste a PAT into chat. |

This blocker does not prevent the repository branch, pull request, labels, milestones, security settings, or CI setup.

## Product evidence / owner decisions

These are not blockers to documentation setup, but they are required before the corresponding product claims or implementation work:

- Which Ecomdy-provided sources are authorized for monitoring, and under what access frequency and retention terms?
- Are the recommended source list, brand guidelines, and previously published articles available and approved for this public repository or local-only use?
- What is the approved MVP market, platform set, and acceptance threshold for “significantly reduced” research time and “substantial” draft suitability?
- What are the interview schedule and evidence owner for the required five seller interviews?
- What deployment environment, model/provider budget, data retention, identity, and access-control constraints apply?
- Should the bundled harness later receive a separate remote or release process? The initial packaging decision is recorded in [DEC-009](DECISION_LOG.md); a separate remote is not required to use the current `.harness/` component.
