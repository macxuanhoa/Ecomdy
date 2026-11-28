# Vertical Slice 01 — Evidence-to-Digest Preview

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Status:** Implementation plan for approval only. No product code, schema, migration, API, live collection or AI call is implemented by this document.<br>
**Traceability:** partial REQ-01, REQ-02, REQ-05, REQ-06, REQ-07 and REQ-11; M01, M02, M04–M06, M09–M10, M12–M13 and M17.

## 1. Objective

Demonstrate the smallest controlled end-to-end path:

```text
Approved source fixture
  → collector
  → raw capture/reference
  → normalization
  → deterministic deduplication
  → deterministic claim candidate extraction
  → evidence-grounded LLM verification adapter
  → central relational store
  → event/claim aggregation
  → digest preview
  → human review of an exact digest version
```

The slice must prove provenance, visible failure states, source-permission enforcement and human approval. It must not imply that Ecomdy has a live crawler, production AI integration, weekly scheduler or publishable content product.

## 2. Scope boundaries

### Included

- One owner-approved source profile and one controlled source type for the first implementation; fixture execution is the default.
- One connector contract and one reference connector implementation.
- Immutable raw capture metadata and permitted raw payload/reference.
- Deterministic normalization, exact deduplication and controlled taxonomy tagging.
- Claim candidates with source spans and immutable article-version references.
- Evidence-grounded verification with explicit supported, contradicted, unresolved, stale and insufficient-evidence states.
- A provider-neutral LLM adapter with a deterministic fake adapter for tests; live provider execution remains disabled until separately approved.
- Relational persistence for source, job, capture, article version, event, claim, evidence, verification, digest, digest item, review and audit records.
- Event/claim aggregation into a read-only digest preview.
- Human review/edit/approve state transitions for an exact digest version; no publication.

### Excluded from Slice 01

- Live internet collection, social-platform APIs, private communities, paid datasets or internal feeds.
- Multiple real platforms, per-source deployed workers or a crawling organization.
- Scheduled recurring collection and production queues.
- Multi-agent orchestration, model routing, multi-model consensus or vector retrieval.
- Website/social/video draft generation, SEO, seller-impact inference and freshness audit.
- Production authentication, hosting, monitoring, backup, encryption policy and deployment.
- Full Ecomdy MVP acceptance, seller interviews, Content Team feedback and success-criteria measurement.

## 3. First slice versus MVP and full target

| Layer | Slice 01 | Complete MVP | Full product target |
|---|---|---|---|
| Sources | One approved profile; fixtures by default | Approved source set with terms and schedules | Multi-platform/multi-method collectors with operating teams |
| Processing | Deterministic normalization/dedup/claim candidates | Classification, evidence verification and digest pipeline | Entity resolution, event clustering, trends and synthesis |
| AI | Adapter plus fake model; evidence required | Approved provider and measured quality/cost | Routed multi-model assistance with human escalation |
| Content | Digest preview only | Weekly digest plus website/social/video drafts and editorial UI | Content operations, freshness audit and optional assistant/notifications |
| Runtime | Local/test integration only | Functional scheduled demo and one-week sample | Production deployment, operations and governance |
| Evidence | Synthetic and controlled fixtures | Real approved sources plus sampled source agreement | Representative evaluation and ongoing audit |

## 4. Module responsibilities

| Module | Slice responsibility | Explicit boundary |
|---|---|---|
| M01 Source Management | Approved source profile, access method, terms review state, enabled flag | No URL becomes fetchable without approval |
| M02 Data Collection | Execute bounded fixture/connector job and record fetch metadata | No arbitrary URL input; no schedule |
| M04 Normalization | Normalize URL, title, language, timestamps and payload shape | Preserve source wording/reference and original dates |
| M05 Deduplication | Exact hash and canonical-URL duplicate links | Similarity is not used to delete evidence |
| M06 Classification | Apply controlled topic/platform/market labels with confidence | Unknown labels remain reviewable |
| M09 Claim Extraction | Produce atomic claim candidates with spans | Extraction is not verification |
| M10 Source Verification | Link evidence and assign verification state | No claim is promoted without evidence; no model-consensus proof |
| M12 Knowledge Store | Persist immutable versions, provenance, evidence and runs | Retention policy still requires approval |
| M13 Weekly Digest | Aggregate eligible claims into a versioned preview | No automatic schedule or publication |
| M17 Editorial Workflow | Review/edit/approve exact digest version | Any edit creates a new draft and invalidates prior current approval |

## 5. Shared contracts

All contracts are versioned and use opaque IDs plus UTC ISO 8601 timestamps. These are proposed schemas, not migration-ready DDL.

| Contract | Required fields | Validation |
|---|---|---|
| `SourceProfile` | `source_id`, `name`, `canonical_url`, `source_type`, `market_id`, `access_method`, `terms_reviewed_at`, `retention_class`, `status` | Fetch allowed only when `status=approved`; no private field inference |
| `IngestionJob` | `job_id`, `source_id`, `mode`, `attempt`, `status`, `started_at`, `completed_at`, `error_code`, `request_id` | Bounded attempt/timeout; terminal state required |
| `RawCapture` | `capture_id`, `job_id`, `source_id`, `fetched_at`, `content_hash`, `raw_ref`, `access_metadata` | Hash required; raw text only if retention permits |
| `NormalizedArticleVersion` | `article_version_id`, `article_id`, `capture_id`, `canonical_url`, `title`, `language`, `published_at`, `observed_at`, `text_ref`, `normalization_version` | Immutable after creation; malformed input fails visibly |
| `EventCandidate` | `event_id`, `title`, `topic_id`, `platform_id`, `market_id`, `first_observed_at`, `last_observed_at`, `status` | Controlled taxonomy; candidate is not a verified event |
| `ClaimCandidate` | `claim_id`, `event_id`, `article_version_id`, `claim_text`, `claim_type`, `source_span`, `effective_from`, `effective_to`, `extraction_state` | Non-empty source span and immutable source reference |
| `EvidenceLink` | `evidence_id`, `claim_id`, `article_version_id`, `source_span`, `support_type`, `authority_level`, `captured_at` | Supporting and contradicting evidence retained |
| `VerificationResult` | `verification_id`, `claim_id`, `evidence_ids`, `policy_version`, `state`, `reason_code`, `ai_run_id`, `review_state` | State cannot be `supported` without evidence and passed deterministic checks |
| `DigestVersion` | `digest_id`, `digest_version_id`, `period_start`, `period_end`, `market_id`, `status`, `content_hash`, `created_at` | Immutable versions; new edit creates new draft |
| `DigestItem` | `digest_item_id`, `digest_version_id`, `event_id`, `claim_ids`, `evidence_ids`, `source_snapshot_ref` | Only eligible verified claims; citation required |
| `ReviewDecision` | `review_id`, `digest_version_id`, `content_hash`, `reviewer_role`, `decision`, `comment`, `created_at` | Approval binds exact version/hash |
| `AIRun` | `ai_run_id`, `task_type`, `provider`, `model`, `template_version`, `input_version_refs`, `output_hash`, `status`, `usage_json` | Fake provider in tests; usage/cost may be null, never fabricated |

### Verification policy

- Deterministic checks run first: source allowlist, span existence, citation resolution, date consistency and contradiction detection.
- The LLM adapter may classify or compare already-linked evidence. It cannot create a source citation or change source text.
- `supported` requires at least one permitted evidence link, a valid span, no unresolved authoritative contradiction and a passed policy version.
- Cross-source agreement is supporting evidence only under an approved authority policy; it is not proof by itself.
- `needs_human_review` is used for ambiguity, low authority, conflicts or model uncertainty.

## 6. Proposed API contracts

No server exists yet. The first API should expose only controlled resources.

| Route | Purpose | Key behavior |
|---|---|---|
| `POST /ingestion-jobs` | Start a fixture or approved connector job | Body accepts `source_id` and `mode`, never an arbitrary URL; authorization and source status checked |
| `GET /ingestion-jobs/{job_id}` | Inspect stage/attempt/error state | Explicit terminal or blocked state; no empty success |
| `GET /events/{event_id}` | Inspect event and source references | Candidate/verified state visible |
| `GET /claims/{claim_id}` | Inspect claim and verification | Evidence links and unresolved reasons visible |
| `GET /claims/{claim_id}/evidence` | Inspect supporting/contradicting evidence | Source URL/span/observed/effective dates visible |
| `POST /digests` | Aggregate eligible evidence into a draft preview | Authorized period/market; records source snapshot |
| `GET /digests/{digest_id}` | Read digest and versions | Draft/current-version state visible |
| `POST /digest-versions/{version_id}/reviews` | Record review decision | Reviewer role and exact content hash required |
| `POST /digest-versions/{version_id}/edits` | Create a new draft version | Prior approval cannot be reused as current |
| `POST /digest-versions/{version_id}/approvals` | Approve exact version | Authorization and state checks; no publication |

Error responses use stable codes such as `source_not_approved`, `source_unavailable`, `parse_failed`, `insufficient_evidence`, `stale_evidence`, `invalid_state_transition` and `approval_version_mismatch`. External URLs and source text are untrusted and rendered safely.

## 7. Test fixtures

Store only synthetic or explicitly permitted public fixtures. No secrets, private source text or personal data.

| Fixture | Purpose | Expected outcome |
|---|---|---|
| `articles-basic.json` | Two distinct permitted articles with dates, URLs and claims | Normalized versions and candidate events created |
| `articles-duplicate.json` | Same canonical URL/hash with a later fetch | Duplicate linked; original evidence preserved |
| `articles-update.json` | Same event with a newer authoritative version | New article version; prior claim can become stale |
| `articles-contradiction.json` | Authoritative contradiction for one claim | Claim becomes contradicted/needs review; excluded from asserted digest |
| `articles-unsupported.json` | Claim candidate without a valid span or evidence | `insufficient_evidence`/`unverified`; excluded |
| `articles-malformed.json` | Invalid date/URL/schema | Visible `parse_failed`; no silent empty success |
| `connector-timeout.json` | Simulated transient timeout | Bounded retry then failed/partial state with error code |
| `llm-hallucinated-citation.json` | Model returns a citation not present in input | Output rejected; run recorded as failed validation |
| `llm-ambiguous.json` | Model is uncertain or evidence conflicts | `needs_human_review`; no forced supported state |

The fake LLM adapter returns deterministic outputs for tests. A live provider is not required for CI and must not be enabled by fixture data.

## 8. Acceptance criteria

### Happy path

1. An approved fixture source completes a bounded job and creates a raw capture with SHA-256, fetch time and source/job IDs.
2. Two unique events and one exact duplicate are processed without deleting source evidence.
3. Each claim candidate points to an immutable article version and source span.
4. At least one supported claim, one contradicted claim and one unresolved claim are produced from the fixture set.
5. The digest preview contains only eligible claims, with source links, evidence IDs and generation snapshot.
6. A reviewer can approve the exact digest version/hash.

### Error and boundary cases

7. Disabled/unapproved sources cannot be fetched through the API or worker.
8. Malformed input, timeout and permission denial produce explicit non-success states.
9. LLM output without valid evidence or with a fabricated citation is rejected.
10. Model agreement cannot override an authoritative contradiction or missing source span.
11. Editing an approved digest creates a new draft version; the previous approval is not current.
12. Duplicate job delivery is idempotent and does not create duplicate captures/events.
13. API input cannot expand connector permissions or introduce arbitrary URLs.

### Security and compliance

14. Default tests make no external network or paid AI calls.
15. Source text, prompts and model output are treated as untrusted input.
16. Raw/processed retention and access behavior follows the approved policy; unresolved policy blocks live storage.
17. Review, approval and configuration actions write audit records with actor/role, resource/version, request ID and timestamp.
18. No content is published automatically.

### Engineering evidence

19. Unit, contract and end-to-end fixture tests pass in CI.
20. API/schema compatibility and rollback checks are recorded.
21. Requirements/capability traceability and user/developer documentation are updated.
22. Independent review is recorded; unresolved blockers are not silently waived.

## 9. Implementation work packages

| ID | Work package | Depends on | Suggested owner role | Acceptance evidence |
|---|---|---|---|---|
| VS01-01 | Approve source/platform/retention/provider decisions and stack | Owner | Project Owner + Source/Data roles | Signed decision record and updated open questions |
| VS01-02 | Freeze contracts, verification policy and fixture corpus | VS01-01 | Architecture + Data roles | Reviewed contracts and passing fixture validation |
| VS01-03 | Implement source/job/raw capture and reference connector | VS01-02 | Collection role | Connector, idempotency, timeout and permission tests |
| VS01-04 | Implement normalization, exact dedup, taxonomy and claim candidates | VS01-02 | Processing role | Deterministic fixture tests |
| VS01-05 | Implement evidence store and LLM verification adapter/fake provider | VS01-02 | Verification + Data roles | Evidence/contradiction/hallucination tests |
| VS01-06 | Implement aggregation, digest versioning and review API | VS01-02, VS01-04, VS01-05 | API + Editorial roles | End-to-end digest and approval-invalidation tests |
| VS01-07 | Add integration CI, security checks, telemetry and recovery tests | VS01-03–06 | Platform/Quality role | CI evidence and bounded failure tests |
| VS01-08 | Run demo rehearsal, source spot-check and handoff | VS01-07 | Project Owner + Reviewer roles | Recorded demo evidence, gaps and next decision |

## 10. Parallel work and integration cadence

- VS01-02 must land first as a contract-only change.
- After VS01-02, VS01-03, VS01-04 and VS01-05 can proceed in parallel against fixtures.
- VS01-06 integrates only after the contracts are stable; avoid simultaneous edits to shared models.
- Merge small task branches at least twice per week during active implementation, or more often if CI and review capacity allow; cadence is proposed, not scheduled.
- Contract changes require a new reviewed version, compatibility tests and an explicit migration/rollback note before dependent branches continue.
- Database migrations are single-owner, forward-only and reviewed; no destructive migration in Slice 01.

## 11. Effort estimate

Planning ranges, not commitments; actual effort depends on stack, source complexity and review capacity.

| Workstream | Engineer-days |
|---|---:|
| Decisions, contracts and fixtures | 3–5 |
| Collector and raw capture | 3–5 |
| Normalization/dedup/claim candidates | 4–6 |
| Evidence store and verification adapter | 4–7 |
| Digest aggregation and editorial state | 4–6 |
| Integration CI, security, docs and rehearsal | 3–5 |
| **Total** | **21–34** |

Parallelization can reduce elapsed time but not total effort. Add contingency for source-policy or provider decisions; do not hide that work inside implementation estimates.

## 12. Approval gates and stop conditions

| Gate | Required approval/evidence | Stop condition |
|---|---|---|
| VS01-G1 | Owner approves platform/market/source profile and fixture/live mode | No approved source or terms review |
| VS01-G2 | Data owner approves retention, raw/reference storage and deletion behavior | Policy unresolved for live data |
| VS01-G3 | Architecture review approves contracts and relational DB choice | Contract/schema conflict |
| VS01-G4 | Security/AI owner approves provider data policy and budget before live model use | No provider approval or budget |
| VS01-G5 | Reviewer roles and independent review capacity confirmed | No qualified reviewer |
| VS01-G6 | Owner approves implementation start | No substantive product code before this gate |
| VS01-G7 | Demo acceptance and remaining gaps recorded | Failed evidence/security criteria |

No live source collection, paid AI use, production migration, deployment or publication is implied by approval of fixture-only implementation. Each broader action requires its own authorization. Use the [VS01 owner approval pack](vs01-owner-approval-pack.md) for plain-language G1–G6 decision cards and the approval record template; that pack does not approve any gate by itself.

## 13. Rollback and recovery

- Disable the source/job by configuration without deleting historical audit records.
- Idempotency keys and content hashes allow safe replay after transient failure.
- Failed derived artifacts are marked invalid; source captures and prior versions remain immutable.
- A bad digest version is superseded, never silently overwritten.
- Roll back application code through normal reviewed commits; database rollback uses a reviewed forward migration/restore plan rather than destructive automatic rollback.

## 14. Definition of Done for Slice 01

All acceptance criteria are evidenced, CI passes, independent review is recorded, source/retention/provider boundaries are explicit, and the owner accepts the fixture-only demo. Completion does not mark the full MVP or any excluded capability as implemented.
