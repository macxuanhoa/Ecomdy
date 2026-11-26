# Blockers and Open Questions

## Active blockers

| ID | Blocker | Impact | Resolution path |
|---|---|---|---|
| BLK-01 | GitHub authenticated write access is unverified; `gh` is unavailable. | Cannot claim or confirm a push, PR, or repository settings change. | Attempt normal Git credential-based push after local commit; record exact result. Do not request tokens in chat. |

## Product evidence / owner decisions

These are not blockers to documentation setup, but they are required before the corresponding product claims or implementation work:

- Which Ecomdy-provided sources are authorized for monitoring, and under what access frequency and retention terms?
- Are the recommended source list, brand guidelines, and previously published articles available and approved for this public repository or local-only use?
- What is the approved MVP market, platform set, and acceptance threshold for “significantly reduced” research time and “substantial” draft suitability?
- What are the interview schedule and evidence owner for the required five seller interviews?
- What deployment environment, model/provider budget, data retention, identity, and access-control constraints apply?
- Should DevHarness OS remain a separate repository, or should a reusable subset be packaged under this repository? Current local harness files are in a sibling directory and no second remote was supplied.
