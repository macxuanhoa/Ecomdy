# Database Design

**State:** Conceptual target model only. No schema, migration, database instance, or retention policy is implemented or approved.

## Design principles

- Make provenance and temporal history first-class.
- Preserve the distinction between source article, event, extracted claim, evidence, draft, and published content.
- Store model output as a derived artifact with its input/version metadata; do not overwrite source data.
- Keep market/platform taxonomies controlled and versioned.
- Start with relational constraints and full-text search; add vector retrieval only if an evaluation demonstrates a need.

## Proposed entities

| Entity | Key fields (candidate) | Purpose / relationships |
|---|---|---|
| `sources` | `id`, `name`, `canonical_url`, `source_type`, `authority_level`, `terms_reviewed_at`, `access_method`, `status` | Approved source profile; one source has many fetch jobs and articles. |
| `ingestion_jobs` | `id`, `source_id`, `started_at`, `completed_at`, `status`, `http_status`, `error_code` | Bounded, auditable collection attempt. |
| `articles` | `id`, `source_id`, `canonical_url`, `title`, `language`, `published_at`, `first_fetched_at`, `current_version_id` | Logical source article; immutable article versions preserve changes. |
| `article_versions` | `id`, `article_id`, `content_hash`, `observed_at`, `effective_at`, `text_ref`, `metadata_json` | Versioned captured content or permitted reference to it. `text_ref` storage policy remains TBD. |
| `events` | `id`, `topic_id`, `market_id`, `first_observed_at`, `last_observed_at`, `status` | Clustered real-world/market event, distinct from articles reporting it. |
| `event_sources` | `event_id`, `article_version_id`, `relationship`, `confidence` | Many-to-many evidence that articles concern an event. |
| `claims` | `id`, `event_id`, `claim_text`, `claim_type`, `effective_from`, `effective_to`, `verification_state` | Atomic factual or regulatory statements requiring evidence. |
| `evidence` | `id`, `claim_id`, `article_version_id`, `source_span`, `captured_at`, `support_type`, `review_state` | Citation/evidence relationship; one claim can have supporting and contradicting evidence. |
| `digests` / `digest_items` | `id`, `period_start`, `period_end`, `market_id`, `status`; item rows link event/claim/evidence | Versioned digest draft and selected items. |
| `content_drafts` / `content_versions` | `id`, `format`, `status`; version row stores text, content hash, created_at, author/run | Multi-channel drafts with immutable versions and evidence references. |
| `reviews` / `approvals` | `id`, `content_version_id`, `reviewer_id`, `decision`, `created_at`, `comment` | Human review; approval references one exact version and can be superseded, never silently reused after edits. |
| `published_articles` / `audit_findings` | `id`, `authorized_url`, `imported_at`; finding links claim/evidence and review state | Authorized articles and freshness audit output. |
| `markets`, `platforms`, `topics` | `id`, `slug`, `label`, `taxonomy_version`, `active` | Controlled domain classifications. |
| `ai_runs` | `id`, `task_type`, `provider`, `model`, `input_version_refs`, `started_at`, `completed_at`, `status`, `usage_json` | Reproducibility, quality, and cost measurement. Provider/model fields are candidates, not selections. |
| `users`, `roles`, `audit_log` | `id`, `role`, `actor_id`, `action`, `resource_type`, `resource_id`, `created_at` | Access control and traceable editorial/configuration actions. Identity provider and retention are TBD. |

## Relationship outline

`source 1:N ingestion_job`; `source 1:N article`; `article 1:N article_version`; `event N:M article_version` through `event_sources`; `event 1:N claim`; `claim 1:N evidence`; digest items link events and evidence; content versions link claims/evidence and have reviews/approvals; audit findings link published articles, claims, and evidence. These are target relationships, not migration-ready cardinalities.

## Temporal and integrity rules

- Do not conflate `published_at`, `first_fetched_at`, `observed_at`, and `effective_from/to`.
- Make source URL and captured version available from every digest/content claim.
- Enforce foreign keys for event/source, claim/evidence, and content/version/review links.
- Store an approval against the content version ID and content hash; updates create a new version.
- Keep unsupported, contradicted, and expired claims queryable for review and audit.
- Define deletion, retention, encryption, backup, access logging, and handling of permitted source text before selecting storage.

## Unresolved schema choices

Whether to store full source text or permitted excerpts; object storage use; PostgreSQL extensions; semantic embeddings; retention windows; multi-tenant support; PII minimization; audit-log retention; and database hosting all require evidence or owner decisions. Do not create migrations until those choices and module contracts are reviewed.
