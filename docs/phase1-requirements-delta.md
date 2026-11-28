# Phase 1 Requirements Delta

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Baseline:** Phase 0 conditional acceptance at `f516230`; PR #1 remains unmerged.<br>
**Status:** Reconciliation proposal for owner and delivery review. This document does not amend the official challenge requirements or approve product implementation.

## 1. Authority and precedence

1. The public challenge workbook remains the authority for official requirements in [01-requirements.md](01-requirements.md).
2. The Project Owner's Phase 1 decisions are authoritative for repository governance and continuation scope.
3. The new industry-context directions are inputs to reconcile. They become mandatory product requirements only after an explicit owner decision and traceability update.
4. The [70-capability coverage matrix](setup/CAPABILITY_COVERAGE.md) remains the capability baseline. New proposal IDs below are not additional implemented capabilities.

## 2. Confirmed Phase 1 governance decisions

These decisions are confirmed but are not new product requirements.

| ID | Confirmed decision | Effect |
|---|---|---|
| GOV-P1-01 | Accept Phase 0 only as a conditional documentation and engineering foundation baseline. | Product runtime and demo acceptance remain open. |
| GOV-P1-02 | Jira is the primary work-management system; GitHub Projects V2 is not required. | Prepare an import-ready backlog until authorized Jira access exists. |
| GOV-P1-03 | Preserve the capability matrix, 56 diagram sources and valid rendered artifacts. | No wholesale redraw, deletion or replacement of valid diagram work. |
| GOV-P1-04 | Proceed with selective Diagram Engineering installation after candidate checks. | Install only a selected and pinned candidate; preserve existing assets. |
| GOV-P1-05 | Prioritize practical team readiness and incremental DevHarness development. | Complete branch, ownership, review, onboarding and handoff controls before broad implementation. |
| GOV-P1-06 | Avoid infrastructure over-engineering that delays product development. | Retain modular-monolith and simple-worker direction unless measured constraints justify change. |
| GOV-P1-07 | Prepare the first vertical-slice plan for approval before substantive product development. | Documentation and design may proceed; product feature implementation is not yet authorized. |
| GOV-P1-08 | Do not bypass branch protection or required human review. | PR #1 and later PRs stop at the human approval boundary. |

## 3. Official requirements unchanged

REQ-01–REQ-12, SC-01–SC-03 and DEP-01–DEP-03 remain open and unchanged. In particular:

- REQ-01 supports monitoring approved public sources; it does not mandate a specific number of agents or an internal crawling organization.
- REQ-05 and REQ-06 require permitted source access and source-linked claims. These constraints apply to every new collector and verification design.
- REQ-07 requires draft content until human approval. LLM verification cannot replace editorial approval.
- REQ-08, REQ-09, REQ-10 and REQ-12 remain unevidenced deliverables or stakeholder tasks.

## 4. Proposed product-direction delta

| Proposal ID | Direction | Existing traceability | Classification | Minimal acceptance evidence if approved |
|---|---|---|---|---|
| P1-PROD-01 | Collect from multiple marketplace/platform domains. | REQ-01, REQ-05, REQ-11; M01–M04 | Proposed extension; platform list is unapproved | At least two owner-approved public source fixtures pass through one shared connector contract without weakening permissions. |
| P1-PROD-02 | Support multiple acquisition methods and source types. | REQ-01, REQ-05; M01–M04 | Proposed extension; API/RSS/web/community access is not assumed | Connector allowlist, terms review, timeout, rate-limit and error tests for each approved method. |
| P1-PROD-03 | Operate independent collectors for individual platforms or sources. | M02–M03; SET-08 harness boundary | Proposed internal responsibility pattern, not necessarily separate deployed services | Bounded per-source job record, retry policy, health state and isolated failure test. |
| P1-PROD-04 | Use multi-agent intelligence processing. | M04–M11, M13–M14; HAR-09, CTX-01, CTX-02, COL-04 | Proposed processing pattern; no mandatory agent count or framework | Each agent-like stage has a deterministic boundary, input/output contract, bounded execution and audit record. |
| P1-PROD-05 | Use LLM-assisted claim extraction and verification. | REQ-06, REQ-11; M09–M10; HAR-09, HAR-12 | Proposed implementation technique with mandatory evidence constraints | Claims retain source spans; unsupported or ambiguous claims remain unresolved; model/run/input references are recorded. |
| P1-PROD-06 | Verify claims across sources. | REQ-06, SC-02; M10 | Proposed strengthening of verification, not proof by model agreement | Supporting and contradicting evidence are linked; authoritative-source policy and human escalation are tested. |
| P1-PROD-07 | Aggregate and synthesize collected information into events, trends and digests. | REQ-02, REQ-11; M07–M08, M13–M14 | Aggregation is proposed for the first slice; trend intelligence remains optional | Event/claim/evidence lineage survives aggregation; digest items expose source links and generation snapshot. |
| P1-PROD-08 | Process multi-modal source material. | M04, M09; CON-01, CON-04 | Deferred unless a real approved source requires it | Source-type and retention decision plus extraction quality and permission evidence; no speculative pipeline. |
| P1-PROD-09 | Route tasks to different models. | M09–M11, M14; M20; HAR-09, HAR-12, CTX-03 | Optional optimization; provider and budget are unapproved | Representative evaluation shows quality/cost benefit; deterministic work is not routed to an LLM without justification. |

## 5. Questions requiring owner or stakeholder decisions

| Question ID | Open question | Why it matters | Blocks |
|---|---|---|---|
| OQ-P1-01 | Does Ecomdy already operate a crawling team, or is the proposed product expected to create one? | Determines whether collectors are an internal organizational dependency or a product module. | Collector ownership and staffing model; does not block interface design. |
| OQ-P1-02 | Which platforms, markets and seller segments are in the first slice? | Prevents unsupported coverage claims and unbounded connector work. | Approved source/platform scope. |
| OQ-P1-03 | Which exact public source URLs and access methods are approved, and what do their terms permit? | Required before any live collection, snapshot storage or redistribution. | Live collector execution and source corpus. |
| OQ-P1-04 | Are social-platform APIs, private communities, paid datasets or internal feeds available and authorized? | None may be assumed. | Non-public or paid connectors. |
| OQ-P1-05 | Which model provider, data-handling policy, token budget and cost ceiling apply? | Required before AI execution or provider credentials. | LLM-assisted extraction/verification implementation. |
| OQ-P1-06 | What qualifies as an authoritative source and when is cross-source agreement sufficient? | Prevents model agreement from being misrepresented as factual proof. | Verification policy and acceptance thresholds. |
| OQ-P1-07 | Who owns source policy, verification review, editorial approval and connector operations? | Role-based placeholders are not assignments. | CODEOWNERS approval and production operating model. |
| OQ-P1-08 | Which retention, deletion, encryption, backup and audit-log policies apply? | Required before database, raw-text storage or deployment decisions. | Storage implementation and production hosting. |
| OQ-P1-09 | Are authenticated Jira access and the GitHub–Jira integration authorized? | No Jira site, project or connector has been verified. | Jira project creation and issue import. |

## 6. First-slice requirement posture

The proposed first vertical slice may satisfy part of REQ-01, REQ-02, REQ-05, REQ-06, REQ-07 and REQ-11 using controlled fixtures. It does **not** satisfy REQ-04 freshness audit, REQ-08 demo delivery, REQ-09 interviews, REQ-10 strategy, REQ-12 editorial UI/feedback or any success criterion without separate evidence.

No live source collection, paid AI call, social API access, private-community ingestion or publication is authorized by this delta. The implementation sequence and acceptance gates are specified in [vertical-slice-01-plan.md](vertical-slice-01-plan.md).

## 7. Change control

- Promote a proposed product direction only through an owner decision, an update to the official/proposed register, capability-matrix review and acceptance evidence.
- Do not create duplicate official requirement IDs for the same challenge obligation.
- Record rejected, deferred or superseded directions in the [decision log](setup/DECISION_LOG.md) rather than silently removing them.
- Keep internal backlog IDs stable; they are not Jira keys.
