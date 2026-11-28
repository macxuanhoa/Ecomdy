# System architecture

> Target design / v0.1 / 2026-11-26. Not verified as-built.

## Design
Modular monolith plus background worker and scheduler. All clients use a common API. Eight logical layers: external sources, ingestion, processing, knowledge, AI, business services, API/access control, UI. Deployment does not require one service per module. Development harness is external to runtime.

![System architecture](diagrams/01-system-architecture.svg)

## Candidate stack (not approved)
React/Next.js + TypeScript; Python/FastAPI; PostgreSQL + FTS; SQLAlchemy/Alembic; Pydantic; simple worker then Redis/Celery if needed; HTTPX/RSS and compliant extraction; optional pgvector, object storage, Telegram; model provider adapters; Docker; pytest/Playwright; OpenTelemetry. Retain existing codebase if suitable. No existing code was supplied here.

## Data design
Sources, ingestion jobs, raw articles, article versions, events, event sources, claims, citations, verification results, markets, platforms, topics, trends/signals/snapshots, digests/items, drafts/versions, published articles, audit findings, reviews, approvals, users/roles, AI runs and scheduled jobs. Conceptual model only; cardinalities need review before migrations. Preserve published/observed/effective dates separately. Store source provenance and retrieval timestamps. Keep unverified claims out of asserted facts.

## Boundaries
Source access by allowlist and terms; source snapshots only when lawful/authorized; no private community collection without permission. Avoid storing unnecessary personal data. Role-based editorial controls; immutable approval version; audit logs; rate limits; bounded AI budget; input/output validation; no prompt injection from sources. Cache and dedup deterministic work before AI.

See [all diagrams](diagrams/README.md).

## Architecture assessment

**As of:** 2026-11-28 (Asia/Saigon). This section distinguishes target architecture from as-built evidence. No application component, database, API, worker, scheduler or deployment exists yet.

### Architecture states

| State | Scope | Evidence | Status |
|---|---|---|---|
| As-built | Repository scripts, validators, advisory `.harness/` CLI, GitHub Actions | Executable files and passing local/CI checks | IMPLEMENTED AND VERIFIED for documentation/harness scope only |
| Slice 01 target | One fixture source → capture → normalize/dedup → claim/evidence → store → digest preview → exact-version review | [Vertical Slice 01 plan](vertical-slice-01-plan.md) | SPECIFICATION ONLY |
| MVP target | Approved source set, weekly digest, three channel drafts, freshness audit, editorial workflow and functional demo | Requirements, module specs, workflow catalogue and diagrams | SPECIFICATION ONLY |
| Full target | Multi-platform/method collection, optional trends/assistant/notifications/routing and production operations | Phase 1 proposals and extension diagrams | SPECIFICATION ONLY / owner approval required |

### Logical component interaction contract

| Component | Receives | Produces | Must not do |
|---|---|---|---|
| Source policy/admin | Owner-approved source identity, terms, retention and schedule | Approved/disabled source profile and audit event | Turn a known URL into an approved source implicitly |
| Connector/collector | Approved source profile and bounded job | `RawCapture`, fetch metadata, explicit failure/health state | Fetch arbitrary URLs, bypass rate/retention policy or report empty failure as success |
| Normalizer/deduplicator | Raw capture/reference and connector schema | Immutable normalized article version and duplicate links | Delete distinct versions or contradictory evidence |
| Classifier/event grouper | Normalized article and controlled taxonomy | Candidate labels/events with confidence and rationale | Claim representative market coverage from a small sample |
| Claim extractor | Immutable article version and extraction policy | Claim candidates with source spans and state | Treat extraction as verification |
| Evidence verifier | Claim, linked evidence, authority/effective-date policy | Verification result with supported/contradicted/stale/unresolved/review state | Invent citations or use model agreement as proof |
| Knowledge store | Sources, versions, events, claims, evidence, runs, drafts and decisions | Temporally aware query/audit records | Store unapproved raw/private data or silently overwrite history |
| Aggregation/digest service | Eligible verified claims, audience, period and source snapshot | Versioned draft digest with lineage | Include unsupported claims or auto-publish |
| Channel draft service | Approved event/evidence, brand and channel template | Website/social/video draft versions | Add uncited claims or approve/publish itself |
| Editorial API/UI | Draft versions, reviewer role and decision | New draft on edit; approval bound to exact hash/version | Reuse stale approval after edit |
| Worker/scheduler | Approved jobs, schedules, retry/checkpoint policy | Job attempts, health, bounded progress and failure records | Change permissions, approve content, deploy or delete history |
| AI adapter | Versioned input references, schema, budget and approved provider policy | Validated candidate output plus run/usage/cost metadata where available | Expand source permissions, fabricate evidence or hide failed validation |

### Trust boundaries

1. **External source boundary:** source text, URLs, feeds and documents are untrusted; only approved hosts/methods may be fetched.
2. **Raw/processed boundary:** raw capture is access-controlled and retention-bound; processed records carry provenance and validation state.
3. **Model boundary:** prompts and outputs are untrusted derived data; deterministic schema/evidence checks run before use.
4. **Editorial boundary:** generated content is draft-only; approval binds to one immutable version/hash.
5. **Operations boundary:** jobs can read/write only scoped records; they cannot merge code, change permissions, deploy or publish.
6. **Development/runtime boundary:** `.harness/` is development infrastructure and is not imported by the Ecomdy runtime.

### Deployment posture

The proposed first deployment is one modular application process plus one bounded worker/scheduler and one relational store. Connector-specific queues, Redis/Celery, Kubernetes, vector storage, object storage and a model gateway are not first-slice defaults. Split a component only for a measured scaling, isolation, deployment or ownership constraint.

No host, region, environment, identity provider, backup target, recovery objective, capacity or cost ceiling is approved. These are architecture inputs, not details to invent during coding.

### Failure and recovery contract

- Every job has a stable ID, stage, attempt, timeout, status, error code and checkpoint reference.
- Retry only classified transient failures; permission denial and malformed policy decisions require correction.
- Idempotency keys/content hashes prevent duplicate capture and derived records.
- Partial failure preserves completed stage outputs and blocks/stales downstream work.
- Invalid model output is recorded and rejected; it never becomes a factual assertion.
- A bad content version is superseded, never silently overwritten.
- Database recovery uses a reviewed forward migration/restore plan; destructive automatic rollback is prohibited.

### Architecture decision gaps

| Decision | Why it blocks implementation | Owner role |
|---|---|---|
| First market/platform/source set and access methods | Defines connector and taxonomy scope | Project Owner + Source Owner |
| Raw/reference retention, deletion, encryption and backup | Defines storage schema and legal/privacy boundary | Data Owner + Security |
| Authoritative-source and contradiction policy | Defines verification states and eligibility | Processing/Evidence + Project Owner |
| Provider data policy, evaluation and budget | Defines whether/how AI can run | Security/AI + Project Owner |
| Database/API/event contracts and migration ownership | Defines safe parallel implementation | Technical Lead + Knowledge/API |
| Identity, roles and reviewer model | Defines editorial/admin authorization | Project Owner + Security |
| Host, operating cost and recovery needs | Defines deployment and worker topology | Platform/Quality + Project Owner |

### Completeness verdict

The target is sufficient to design and review a fixture-first vertical slice. It is not sufficient to start live collection, production storage, paid AI or deployment. The architecture becomes implementation-ready only after `ARCH-G01`–`ARCH-G07` and `VS01-G1`–`VS01-G6` are resolved and the first contracts are approved.
