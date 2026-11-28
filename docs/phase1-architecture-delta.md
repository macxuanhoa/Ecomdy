# Phase 1 Architecture Delta

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Baseline:** [03-architecture.md](03-architecture.md), modular monolith plus background worker/scheduler.<br>
**Status:** Targeted change proposal only. No runtime, database, service or model integration is implemented.

## 1. Delta summary

Retain the existing modular monolith and simple worker/scheduler. Add explicit contracts and responsibility boundaries for multi-source collection, deterministic processing, evidence-based LLM assistance, verification, aggregation and governance. The proposed nine “teams” are logical ownership boundaries inside the application and worker, not nine independently deployed microservices.

This delta changes the target design only where the new directions require it. Existing provenance, temporal, source-permission, editorial-approval and audit constraints remain in force.

## 2. Responsibility mapping

| Proposed responsibility | Placement in current architecture | Owns | Must not own |
|---|---|---|---|
| Master Orchestration | Business/application service plus worker job dispatcher | Bounded run plan, stage ordering, dependency resolution, budgets, checkpoints | Source-specific parsing, factual verification decisions |
| Data Collection Team | Ingestion layer and per-source worker tasks | Approved source allowlist, connector execution, raw capture, fetch metadata, rate limits | Claim truth, editorial approval |
| Data Processing Team | Processing layer | Normalization, exact deduplication, canonicalization, entity-resolution candidates, event-clustering candidates | Uncited factual assertions |
| Verification Team | Processing and AI adapter layer | Claim/evidence checks, cross-source comparison, unresolved/contradicted states, human escalation | Proof by LLM consensus or silent promotion to verified |
| Intelligence Synthesis Team | Business services | Event summaries, eligible-item selection, digest aggregation, explicit inference labels | New claims without evidence |
| Central Knowledge and Evidence Store | Knowledge layer and relational store | Sources, versions, raw/processed references, events, claims, evidence, runs, drafts, approvals, audit | Unbounded or unapproved source retention |
| Content Production Services | Business services and AI adapters | Channel-specific drafts tied to selected evidence and source snapshot | Publication or approval bypass |
| Editorial and User Interaction Services | API/access-control and UI layers | Review, edit, new-version creation, exact-version approval, safe citation rendering | Automatic publication |
| Automation and Governance | Cross-cutting controls, worker scheduler, admin API | Retry/recovery, permissions, rate limits, budget caps, audit events, health and quality metrics | Hidden privilege expansion or unaudited configuration changes |

## 3. Component and interface deltas

### 3.1 Source and connector boundary

- Keep `sources` as the approved identity and access-policy record. A source cannot be fetched merely because a URL is known.
- Introduce one shared connector interface with: `source_id`, approved `access_method`, request/feed metadata, bounded timeout, permitted rate, `fetched_at`, response status, content hash and normalized payload.
- Implement one connector per approved source type. Per-source collectors are configuration plus worker jobs, not separate long-lived services by default.
- Store raw capture only within the approved retention policy. Otherwise store the permitted reference/hash and minimal fetch metadata.
- Separate `source_available`, `source_blocked`, `source_changed` and `parse_failed` outcomes; do not report an empty run as success.

### 3.2 Processing and intermediate contracts

Use versioned shared records, independent of connector and model provider:

- `RawCapture`: source/version identity, acquisition method, observed time, permitted payload/reference, hash and access metadata.
- `NormalizedArticle`: canonical URL, title, language, published/observed times, source wording reference and validation state.
- `EventCandidate`: normalized article references, market/platform/topic candidates, time bounds and clustering rationale.
- `ClaimCandidate`: atomic statement, type, affected entities, source span and extraction state.
- `EvidenceLink`: claim/version reference, source span, support/contradiction type, authority and review state.
- `VerificationResult`: claim reference, evidence set, policy version, result state, reviewer/model run and unresolved reason.
- `DigestCandidate`: event/claim/evidence references, source snapshot, generation time and eligibility reason.

AI output remains an untrusted derived artifact until deterministic schema/evidence checks and, where required, human review pass.

### 3.3 Deterministic-first processing

Perform these steps without an LLM first:

1. Allowlist and terms check.
2. Fetch, hash and timestamp capture.
3. Parse and validate connector payload.
4. Normalize dates, URLs, language and marketplace/platform taxonomy.
5. Exact hash and canonical-URL deduplication.
6. Deterministic entity aliases and event-grouping candidates.
7. Evidence presence, span, URL and temporal consistency checks.

Similarity-based deduplication may propose links only; it must not discard distinct source evidence or updates. Low-confidence entity resolution and clustering enter a review queue.

### 3.4 LLM-assisted extraction and verification

- Use provider-neutral adapters and record provider/model, prompt/template version, input-version references, output hash, timestamps, usage and cost where available.
- Extraction may identify candidate claims and spans. Verification must compare claims with linked source evidence; it cannot invent citations.
- Multiple models may be used for evaluation or escalation, but agreement is not factual proof. Verification state depends on evidence quality, source authority, recency and contradictions.
- Explicit states include `unverified`, `supported`, `contradicted`, `stale`, `insufficient_evidence` and `needs_human_review`.
- Route work by measured task quality and cost. Keep deterministic tasks deterministic; do not add a router before evaluation data exists.
- Bound retries, context size, token spend and elapsed time. A failed model run is a recorded failure, not a reason to assert the claim.

### 3.5 Cross-source verification and synthesis

- Evidence is many-to-many across claims and immutable article versions.
- Preserve supporting and contradicting evidence, authority level and effective/observed times.
- Cross-source agreement strengthens confidence only under an approved source-authority policy; it never overrides a contradictory authoritative source.
- Aggregation links every digest item to events, claims, evidence and the source snapshot. Inference and assumptions remain labeled.
- Trends, viral/market-wide claims and platform coverage are prohibited unless representative evidence supports them.

### 3.6 Retry, recovery and checkpoints

- Every job has a stable ID, stage, attempt, timeout, status, error code and checkpoint reference.
- Retry only classified transient failures. Do not retry permission denials, malformed policy decisions or unsafe input without correction.
- Idempotency keys or content hashes prevent duplicate capture and duplicate derived records.
- Partial failure preserves completed stage outputs and marks downstream work blocked or stale.
- DevHarness remains advisory until task-scope, budget and checkpoint enforcement are implemented and tested; do not imply runtime enforcement from configuration files alone.

## 4. Data and API impact

The conceptual entities in [database-design.md](database-design.md) remain suitable. Before migrations, refine:

- source access-policy fields and connector configuration boundaries;
- raw-capture retention/reference policy;
- event-clustering candidates and review state;
- claim/evidence support, contradiction, authority and source-span contracts;
- AI-run prompt/model/input/output/usage references;
- job attempts, idempotency and checkpoint records;
- approval binding to exact content version and hash.

The proposed resources in [api-design.md](api-design.md) remain valid. Add contract tests before implementation for connector/job creation, claim/evidence retrieval, aggregation preview and editorial state transitions. Do not expose an arbitrary URL fetcher or allow API input to expand connector permissions.

## 5. Security, provenance and governance

- External URLs, source text, prompts and model output are untrusted input.
- Source permissions, retention and citation rules are enforced server-side.
- Raw and processed data are separated by purpose and access policy; do not store unnecessary personal data.
- Approval binds to one content version/hash. Any edit creates a new draft version and invalidates the earlier version as current.
- Record actor, action, resource/version, request ID and timestamp for review, approval and configuration changes.
- Telemetry must not contain secrets, unrestricted source text or unnecessary personal data.

## 6. Deployment and scaling posture

1. Start with one application process/modular monolith and one bounded worker/scheduler.
2. Use connector-specific queues or worker concurrency only after source volume and fairness require it.
3. Split a service only for a measured scaling, isolation, deployment or ownership constraint.
4. Keep central evidence and provenance contracts stable if a component is later extracted.
5. Do not select Redis/Celery, Kubernetes, vector storage or a model gateway for the first slice without evidence.

## 7. Decision points before implementation

| Gate | Required decision/evidence |
|---|---|
| ARCH-G01 | Owner-approved first platform/market/source list and access methods. |
| ARCH-G02 | Raw-text/reference retention, deletion, encryption and backup policy. |
| ARCH-G03 | Authoritative-source and cross-source verification policy. |
| ARCH-G04 | AI provider/data policy, task evaluation, token/cost budget and human escalation. |
| ARCH-G05 | Database/API contracts and migration ownership. |
| ARCH-G06 | Role-based ownership, review requirements and operating responsibilities. |
| ARCH-G07 | Vertical-slice plan approval before product code. |

## 8. Explicit non-goals for Phase 1

- No microservice-per-team deployment.
- No unrestricted crawler, private-community collector or arbitrary URL ingestion.
- No automatic publication or approval.
- No factual-verification claim based on model agreement.
- No full redraw of the 56 existing diagrams.
- No database migration or live external collection before the relevant gates are approved.

See [vertical-slice-01-plan.md](vertical-slice-01-plan.md) for the smallest implementation sequence that exercises these contracts with controlled fixtures.
