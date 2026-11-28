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

## Master roadmap and critical path

**As of:** 2026-11-28 (Asia/Saigon). This is a dependency-aware sequence, not a dated commitment. Capacity, deadline, staffing and source/provider decisions remain unapproved.

### Milestones

| Milestone | Outcome | Depends on | Exit gate | Current state |
|---|---|---|---|---|
| MS0 — Integrable baseline | Accepted setup/docs are on default `main`; fresh clone follows Quick Start | PR #1 review, authenticated protection/security read-back, normal merge | Default clone passes validator, doctor, 3 tests and harness validator | BLOCKED by owner review/merge |
| MS1 — Accountable delivery | Real owners/reviewers and Jira-first task flow operate | MS0; role mapping; Jira authorization | One real task links requirement → branch → PR → checks → decision | BLOCKED by Jira/owners |
| MS2 — Approved slice contract | Source/market/retention/verification/provider/stack decisions and fixtures are approved | MS1 for assignments; owner/source/data/security decisions | `VS01-G1`–`VS01-G6` signed; contracts reviewed | PREPARED, not approved |
| MS3 — Evidence vertical slice | Fixture source produces traceable digest preview and exact-version review | MS2 | All Slice 01 acceptance tests and independent review pass | NOT IMPLEMENTED |
| MS4 — Editorial MVP | Weekly digest, website/social/video drafts and editorial controls work on approved inputs | MS3; brand guidance; editorial roles; controlled demo schedule | Three cited formats, approval invalidation and one-week sample evidenced | NOT IMPLEMENTED |
| MS5 — Freshness and validation | Authorized article audit, five seller interviews, Content Team feedback and measured rubric | MS3/MS4; authorized article corpus; research owners | REQ-04/09/12 and SC-01–SC-03 evidence accepted | NOT IMPLEMENTED |
| MS6 — Functional demo/release candidate | Reproducible demo with security, recovery, accessibility and operating evidence | MS4/MS5; deployment/operations decisions | Owner accepts demo and residual gaps; no hidden manual claims | NOT IMPLEMENTED |
| MS7 — Evidence-led extensions | Trends, Telegram, assistant, notifications, routing or multi-agent patterns evaluated separately | MS6; task-specific quality/cost/permission/failure benchmarks | Each extension independently approved or rejected | DEFERRED |

### Critical path

```text
PR #1 owner review + authenticated governance verification
        │
        ▼
MS0 default-branch baseline merge
        │
        ▼
Real owners/reviewers + Jira authorization (MS1)
        │
        ▼
Source/market/retention/verification/provider/stack decisions
        │
        ▼
Reviewed contracts + fixtures + VS01-G6 (MS2)
        │
        ▼
Collector → normalize/dedup → claim/evidence → store → digest/review (MS3)
        │
        ▼
Channel drafts + editorial workflow (MS4)
        │
        ├── Authorized freshness audit ───────────────┐
        ├── Five seller interviews ──────────────────┤
        └── Content Team feedback + rubric ───────────┘
                                               ▼
                              Measured acceptance + demo (MS5/MS6)
                                               ▼
                              Optional extensions (MS7)
```

Source/policy decisions and user research can proceed in parallel with contract design, but live collection, non-public storage and paid AI remain blocked until their gates pass.

### Workstreams

| Workstream | Scope | Can start now | Blocking dependency | Proposed branch pattern |
|---|---|---|---|---|
| W0 Governance/integration | PR review, protection/security read-back, owners, Jira | Review and evidence collection only | Owner authorization | `docs/phase-0-acceptance`, then approved task branches |
| W1 Product discovery | Market/source/brand/article inputs, five interviews, success rubric | Planning and authorized interviews | Named research/source owners | `docs/discovery-<id>` or `spike/<id>` |
| W2 Contracts/data | Source/job/capture/article/event/claim/evidence/digest/review schemas and API | Specification and fixture design | MS1/MS2 decisions | `docs/contracts-<id>` before `feat/<id>` |
| W3 Collection/processing | Reference connector, normalization, exact dedup, taxonomy, claim candidates | Fixture-only design | W2 contract approval | `feat/vs01-<id>` |
| W4 Verification/store | Evidence states, relational store, fake provider, policy tests | Fixture/schema design | W2; provider approval only for live AI | `feat/vs01-<id>` |
| W5 Digest/editorial | Aggregation, digest versioning, review/approval API/UI | Contract and UX specification | W2–W4 stable contracts | `feat/vs01-<id>` |
| W6 Quality/operations | CI, security, recovery, accessibility, deployment readiness | Documentation/check design | Implemented slice and approved environment | `test/<id>`, `ci/<id>`, `chore/<id>` |
| W7 Diagram/harness | Pinned Mermaid validation, selective harness hardening | Plugin/parser audit complete | Separate tool/security/owner decisions | `diag/<id>`, `chore/harness-<id>` |
| W8 Extensions | Trends, Telegram, assistant, notifications, routing | None beyond evaluation design | MS6 and task-specific benchmark | `spike/<id>` then approved feature branch |

### Branch and integration plan

1. Keep `main` as the only permanent integration branch.
2. Resolve PR #1 first; keep PR #2 stacked until PR #1 merges, then retarget/rebase normally.
3. Land contract-only changes before dependent implementation branches.
4. After contract approval, collection, processing and verification work can proceed in parallel against shared fixtures.
5. Digest/editorial integration starts only after upstream contracts stabilize.
6. Use one migration owner and forward-compatible migrations; no destructive migration in Slice 01.
7. Merge small reviewed branches at a proposed twice-weekly cadence only after reviewer capacity is confirmed.

### Effort and capacity assumptions

- Vertical Slice 01 estimate remains **21–34 engineer-days**, not a commitment.
- Parallelization can reduce elapsed time but not total effort.
- Add explicit capacity for source-policy review, security/provider review, interview synthesis, independent review and demo rehearsal.
- Do not convert the estimate into dates until team availability, challenge deadline and reviewer capacity are approved.
- Extension work is excluded from the first-slice estimate and requires its own benchmark and approval.

### Immediate action sequence

| Order | Action | Owner role | Evidence produced |
|---:|---|---|---|
| 1 | Review PR #1 and verify current protection/security | Project Owner + Platform/Security | Merge decision and authenticated read-back |
| 2 | Assign real reviewers/module owners and approve review count | Project Owner | Role-to-person map and review policy |
| 3 | Authorize Jira and import approved backlog rows | Project Owner + Jira admin | Real project/keys and one linked PR test |
| 4 | Approve first market/platform/source and retention/verification policy | Project Owner + Source/Data/Evidence | VS01-G1/G2 and ARCH-G01–G03 records |
| 5 | Approve provider/budget/evaluation and stack/contracts | Project Owner + Security/AI + Technical Lead | VS01-G3/G4 and ADR/contracts |
| 6 | Approve implementation start | Project Owner | VS01-G6 decision |
| 7 | Implement and verify Slice 01 | Assigned workstream owners | Passing tests, review and fixture demo |
| 8 | Expand to editorial MVP, freshness and user validation | Product/Content/Research owners | REQ-02/03/04/09/12 and success evidence |

### Replanning rules

- Replan when a prerequisite is blocked; do not weaken the gate to preserve a date.
- Promote an extension only with owner approval, requirement traceability and task-specific quality/cost/permission/failure evidence.
- A successful documentation check, generated diagram, imported backlog or fixture demo does not mark the next milestone complete.
- Preserve rejected/deferred decisions in the decision log and update the handoff from observed state.
