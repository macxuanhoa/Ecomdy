# Implementation roadmap

> Target design / v0.1 / 2026-11-26. Not verified as-built.

| Stage | Deliverable | Acceptance gate |
|---|---|---|
| 00 | Bootstrap and original source register | documents retained and provenance |
| 01 | Existing code and source access audit | confirmed code baseline, no invented features |
| 02 | Requirements and architecture reconciliation | owner approves scope, stack, risks |
| 03 | Vertical ingestion-to-digest slice | scheduled demo, duplicate removal, links |
| 04 | Content and editorial workflow | three formats, approval controls |
| 05 | Freshness audit | evidence-backed flagged article |
| 06 | Business/design validation | 5 real interviews, calendar, feedback, measured time comparison |
| 07 | Release and functional demo | actual test evidence, one-week samples, review |
| 08 | Extension pack | trend, Telegram, analytics; independently approved |

No stage is marked implemented. Current codebase absent. Interview data must never be invented. Record requirements → implementation → test → evidence. Human approval required before any coding on existing repository.

## Proposed dependency graph

```text
Approved source access + source/brand inputs
                 │
                 ▼
REQ-01 collection ──► REQ-11 normalization/dedup ──► REQ-06 claim/evidence checks
                                                        │
                                                        ▼
REQ-02 weekly digest ──► REQ-03 channel drafts ──► REQ-07 human approval
                                                        │
                                                        ▼
                                                 REQ-08 functional demo

Authorized published articles + current evidence ──► REQ-04 freshness audit
Seller interviews ──► REQ-09 discovery ──► REQ-10 topic/calendar proposal
Editorial prototype ──► REQ-12 Content Team usability feedback
```

Requirements REQ-05 (source terms) and REQ-07 (draft-only until human approval) constrain every branch. REQ-04 needs an authorized corpus. REQ-09 and parts of REQ-10 can proceed in parallel with engineering. The graph is a proposed ordering; owner scope decisions may change it.

## Sprint planning

No dated sprint plan is set because the deadline, team capacity, owner, and stakeholder availability were not supplied. Use the following sequence as planning waves, not calendar commitments:

1. **Discovery and approvals:** confirm sources, brand inputs, user workflow, MVP market, reviewer roles, and success thresholds.
2. **Evidence-backed ingestion:** permitted connector fixture, normalization, deduplication, source versions, and claim/evidence state.
3. **Digest and drafts:** weekly digest plus website/social/video drafts with source links and review/version states.
4. **Freshness and demo:** authorized published-article audit, one-week sample, source spot checks, and usability feedback.
5. **Release readiness:** security, accessibility, recovery, operations, deployment, and evidence review.

Each wave needs a task contract, dependencies, acceptance criteria, resource estimate, and owner before it becomes a committed sprint.
