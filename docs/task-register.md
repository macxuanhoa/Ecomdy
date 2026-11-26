# Product Task Register

**State:** Candidate work breakdown; all product tasks are Proposed and unscheduled. No product implementation is claimed.

| ID | Task | Priority | Depends on | Acceptance evidence | State |
|---|---|---|---|---|---|
| ECO-01 | Confirm MVP scope, success thresholds, source owners, retention, identity, provider, budget, and deployment constraints. | P0 | Owner decisions | Approved decision records and updated PRD/SRS. | Proposed |
| ECO-02 | Obtain and review recommended source list, terms, access methods, brand guide, and authorized published articles. | P0 | ECO-01 | Source register with approval and permitted-use evidence; private inputs kept local unless publication approved. | Proposed |
| ECO-03 | Complete at least five seller interviews and record information needs and usual sources. | P1 | Interview owner/schedule | Interview evidence, synthesis, and changes to requirements. | Proposed |
| ECO-04 | Gather Content Team feedback and define draft suitability rubric and research-time baseline. | P1 | ECO-01, ECO-03 | Approved rubric and reproducible baseline protocol. | Proposed |
| ECO-05 | Define source, article-version, event, claim, evidence, and audit contracts. | P0 | ECO-01, ECO-02 | Reviewed schema/API decision records with temporal and retention rules. | Proposed |
| ECO-06 | Implement one permitted connector with rate, timeout, retry, provenance, and fixture tests. | P0 | ECO-02, ECO-05 | Passing connector tests and source agreement evidence. | Proposed |
| ECO-07 | Implement normalization, deduplication, classification, and claim/evidence verification. | P0 | ECO-05, ECO-06 | Deterministic tests for duplicates, dates, conflicts, and unresolved claims. | Proposed |
| ECO-08 | Implement owner-approved automatic weekly digest generation and website/social/video draft generation. | P0 | ECO-04, ECO-07 | A controlled scheduled run produces one weekly sample with citations and per-channel drafts; disabled schedules do not fetch; drafts are reviewed against the rubric. | Proposed |
| ECO-09 | Implement review/edit/approve state transitions with exact-version approval and role checks. | P0 | ECO-01, ECO-08 | Authorization and version-invalidation tests; editor feedback recorded. | Proposed |
| ECO-10 | Implement a freshness audit over authorized published articles. | P0 | ECO-02, ECO-05, ECO-07 | Controlled old/new fixtures produce evidence-linked, dated findings. | Proposed |
| ECO-11 | Prepare weekly functional demo and collect acceptance evidence. | P0 | ECO-03, ECO-04, ECO-08, ECO-09, ECO-10 | Running weekly demo, one-week sample content, source checks, team feedback, and explicit gaps. | Proposed |
| ECO-12 | Evaluate trend, Telegram, vector retrieval, and additional markets only after MVP evidence. | P2 | ECO-11 and separate owner approval | Comparative benchmark and an approved decision record before implementation. | Proposed |

Do not mark these tasks Ready until their prerequisites and Definition of Ready are met. See [Sprint Planning](sprint-planning.md), [Product Task Dependency Graph](diagrams/32-product-task-dependencies.mmd), [Module Dependency Graph](diagrams/18-module-dependencies.mmd), and [Roadmap](05-roadmap.md).
