# Vertical Slice 01 — Owner Approval Pack

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Status:** Decision aid only. **No gate is approved by this document.**<br>
**Related plan:** [Vertical Slice 01 — Evidence-to-Digest Preview](vertical-slice-01-plan.md)

## 1. What the owner is being asked to decide

The first product slice should prove one narrow path: an approved fixture becomes normalized, deduplicated, evidence-linked data and then a digest preview that a person can review. It should not crawl the live internet, call a paid model, deploy a service or publish content.

The six gates below turn that intention into explicit decisions. Each gate must be recorded by the authorized role. Silence, a planning document or agreement between agents is not approval.

### Decision options for every gate

- **APPROVE FIXTURE-ONLY** — allow the narrow local/test scope described below.
- **APPROVE WITH CONDITIONS** — allow it only after named conditions are evidenced.
- **DEFER** — keep the gate open and identify the missing fact or owner.
- **REJECT** — do not proceed; record the reason and any alternative.

A recommendation is not a decision. Do not pre-check a box or insert a person's name until that person actually decides.

## 2. Dependency order

```text
G1 source and mode ─────┐
                       ├─→ G3 contracts and storage → G6 implementation start
G2 retention ───────────┘                 ↑
G4 fake/live AI boundary ────────────────┤
G5 reviewer capacity ───────────────────┘
```

- G1 and G2 evidence can be prepared in parallel.
- G3 needs the source and retention decisions as inputs.
- G4 can approve a deterministic fake adapter while explicitly deferring every live-provider decision.
- G5 can be prepared in parallel, but real reviewers must be confirmed before G6.
- G6 is last. No substantive product code starts before all six decisions are recorded.
- G7 demo acceptance remains after implementation and is not requested here.

## 3. Gate cards

### VS01-G1 — Source, market and execution mode

**Plain-language question:** Which one source profile and market are we allowed to represent, and are we using fixtures only or touching a real source?

**Why it matters:** A source URL is not permission. The slice needs a bounded subject and a clear terms/access decision before any collector behavior is designed.

**Recommendation:** Approve one owner-selected source profile and market in **fixture-only mode**. Use synthetic or explicitly permitted public fixtures. Do not enable network collection.

| Field | Decision material |
|---|---|
| Options | Approve fixture-only; approve with conditions; defer; reject |
| Approval allows | A controlled source-profile record and fixture connector contract |
| Approval does not allow | Live crawling, arbitrary URLs, private communities, paid datasets or scheduled collection |
| Evidence required | Source identity/type, market, terms review state, fixture classification, access method and enabled/disabled status |
| Approver role | Project Owner + Source/Data role |
| Stop condition | No approved profile, no terms review or unresolved fixture permission |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

### VS01-G2 — Data retention and raw/reference storage

**Plain-language question:** What source data may we keep, where, for how long and who can delete or read it?

**Why it matters:** Raw captures can contain copyrighted, personal or confidential material. The database and collector cannot be accepted without a retention boundary.

**Recommendation:** For Slice 01, keep only synthetic/permitted fixture payloads plus hashes and provenance metadata in local/test storage. Defer live raw-text retention and deletion policy until the Data/Security owners approve them.

| Field | Decision material |
|---|---|
| Options | Approve fixture-only retention; approve with conditions; defer; reject |
| Approval allows | Local/test persistence of approved fixtures, content hashes, metadata and immutable references |
| Approval does not allow | Live/private raw storage, production backups, undeclared retention or automatic deletion of evidence |
| Evidence required | Data classification, storage location, access roles, retention period, deletion behavior, raw-versus-reference rule and recovery approach |
| Approver role | Data Owner + Security role |
| Stop condition | Live data policy unresolved; fixture permission or storage location unclear |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

### VS01-G3 — Contracts, architecture and relational store

**Plain-language question:** Do the teams agree on the data/API contracts and the smallest runtime shape before anyone writes dependent code?

**Why it matters:** Parallel work fails when collector, processing, evidence and digest teams invent different IDs, timestamps or state rules.

**Recommendation:** Approve a contract-first, modular-monolith slice with a bounded worker and a relational store. Freeze the contracts and fixtures before implementation. Select the actual language/framework/database only after team-skill and operating-cost review; this gate does not approve a production migration.

| Field | Decision material |
|---|---|
| Options | Approve contract-first fixture architecture; approve with conditions; defer; reject |
| Approval allows | A contract-only PR, fixture validation and dependent branches against the frozen contracts |
| Approval does not allow | Microservice expansion, production schema migration, deployment or unrelated modules |
| Evidence required | Reviewed `SourceProfile`, job/capture/article/claim/evidence/digest/review contracts; state/error model; DB choice rationale; compatibility and rollback notes |
| Approver role | Technical Lead/Architect + Knowledge/API role |
| Stop condition | Contract conflict, unresolved DB choice or no migration/rollback owner |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

### VS01-G4 — AI provider boundary and budget

**Plain-language question:** Are we approving only a deterministic fake model for tests, or also a real provider, its data policy and a spending limit?

**Why it matters:** A model can invent citations or leak source data. Fixture tests must remain deterministic and offline, while live model use needs separate authorization.

**Recommendation:** Approve the **deterministic fake adapter only** for Slice 01 tests. Explicitly defer provider selection, live prompts/data handling, token/cost budget and external calls. A later live-provider decision must be recorded separately.

| Field | Decision material |
|---|---|
| Options | Approve fake adapter only; approve live use with full conditions; defer; reject |
| Approval allows | Provider-neutral interface, deterministic fake outputs and hallucinated-citation rejection tests |
| Approval does not allow | Paid API calls, live source text sent to a provider, model routing, multi-model consensus or fabricated usage/cost metrics |
| Evidence required | Adapter interface, fake fixtures, evidence-validation rules, data-flow boundary and explicit live-provider status |
| Approver role | Security/AI role + Project Owner |
| Stop condition | Fake/live boundary unclear; no citation validation; live provider or budget not separately approved |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

### VS01-G5 — Independent review capacity

**Plain-language question:** Who will review the work, and do they have the independence and specialist knowledge needed for source, data, security and editorial decisions?

**Why it matters:** A passing test written by the same author is not independent acceptance. Missing reviewers turn merge and demo approval into informal decisions.

**Recommendation:** Confirm at least one independent reviewer per task plus the specialist roles required by the change. Record real people only after the owner assigns them. Do not invent a reviewer count in branch protection before authenticated verification.

| Field | Decision material |
|---|---|
| Options | Confirm named capacity; confirm with conditions; defer; reject |
| Approval allows | Review assignments and readiness for G6 |
| Approval does not allow | Self-approval, fictional handles, automatic merge or bypassing specialist review |
| Evidence required | Reviewer roster by role, availability/capacity, conflict-of-interest rule and specialist review map |
| Approver role | Project Owner + Technical Lead |
| Stop condition | No qualified independent reviewer or unresolved review ownership |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

### VS01-G6 — Implementation start

**Plain-language question:** May the team now build the approved fixture-only slice within the recorded boundaries?

**Why it matters:** This is the boundary between planning and product code. It prevents a broad roadmap from being mistaken for permission to implement everything.

**Recommendation:** Approve only when G1–G5 have explicit decisions and evidence, the contract/fixture work package is ready, and the reviewed branch path is available. Approval covers VS01-02 through VS01-07 within fixture-only scope. It does not cover live collection, paid AI, production migration, deployment or publication.

| Field | Decision material |
|---|---|
| Options | Approve fixture-only implementation; approve with conditions; defer; reject |
| Approval allows | Bounded fixture implementation, local/test integration and demo preparation |
| Approval does not allow | Live sources, paid AI, production operations, public release or expansion to M18–M20 |
| Evidence required | G1–G5 records; frozen work packages; allowed/forbidden paths; verification plan; stop/rollback conditions; reviewer assignments |
| Approver role | Project Owner |
| Stop condition | Any prior gate missing, scope ambiguous or review path unavailable |

**Record:** Decision `TBD` · Conditions `TBD` · Evidence link `TBD` · Approver `TBD` · Date `TBD`

## 4. Cross-track readiness

| Track | Relationship to VS01 approval | What can happen before G6 |
|---|---|---|
| A — Team Infrastructure | Supplies real reviewers, Jira keys and the reviewed integration path | PR-stack review, role mapping, Jira authorization request, onboarding test plan |
| B — Minimum Viable DevHarness | Supplies deterministic context/scope/verification/handoff capabilities as they are approved | Plan review and isolated validation; no new runtime command without scope approval |
| C — Ecomdy Product | Consumes G1–G6 decisions | Source/retention/contract/fixture preparation and approval evidence only |

Track C implementation does not wait for every P1 harness capability. It waits for the six product gates and the deterministic controls required by the approved task.

## 5. Approval record template

Copy one row per gate into the owner-approved decision record. Keep the evidence link and actual approver; do not replace them with a role placeholder after approval.

| Gate | Decision | Conditions / expiry | Evidence link or hash | Approver name and role | Decision date | Next action |
|---|---|---|---|---|---|---|
| VS01-G1 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| VS01-G2 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| VS01-G3 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| VS01-G4 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| VS01-G5 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| VS01-G6 | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

## 6. Evidence checklist before G6

- [ ] G1 source profile, market, terms review and fixture-only mode are recorded.
- [ ] G2 fixture retention, storage, access and deletion behavior are recorded.
- [ ] G3 contracts, state/error model, relational-store choice and rollback notes are reviewed.
- [ ] G4 fake adapter is approved and live-provider use is explicitly not approved or separately authorized.
- [ ] G5 real independent reviewers and specialist roles are confirmed.
- [ ] Allowed/forbidden paths, acceptance tests, stop conditions and recovery steps are written.
- [ ] The task branch/PR path and current CI results are verified.
- [ ] No approval is inferred from this pack, an agent response or an unmerged PR.

If any item is missing, record `DEFER` or `APPROVE WITH CONDITIONS`; do not convert uncertainty into approval.
