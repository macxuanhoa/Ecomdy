# Module Specifications

**State:** Proposed target contracts, not implemented. Module boundaries should be checked against the approved MVP and the existing codebase before implementation.

## Core data-to-draft path

| ID | Module | Responsibility / input | Output | Key constraints and acceptance evidence |
|---|---|---|---|---|
| M01 | Source Management | Maintain source identity, URL, authority, market, access method, terms, and health state | Approved source configuration | Do not fetch a source without an approved access policy; audit configuration changes. |
| M02 | Data Collection | Fetch from approved API/RSS/web connectors | Timestamped raw capture and fetch result | Respect terms and rate limits; record source URL, fetched time, response status, and content hash. |
| M03 | Scheduling | Create bounded per-source collection jobs | Job state and execution history | Disabled until sources, schedule, host, and budget are approved; support timeout and pause. |
| M04 | Normalization | Convert connector formats to a common article/event candidate | Normalized record with source provenance | Preserve source wording/URL and original dates; malformed data fails visibly. |
| M05 | Deduplication | Compare exact hashes, canonical URLs, and candidate similarity | Duplicate links / retained canonical records | Similarity proposes links only; do not discard distinct updates or source evidence. |
| M06 | Classification | Tag topic, platform, market, and content type | Classified article/event with confidence | Low-confidence categories remain reviewable; no unsupported market coverage claim. |
| M07 | Market Intelligence | Relate an event to an approved seller/market/platform context | Relevance rationale | Start with owner-approved market taxonomy; distinguish evidence from inference. |
| M08 | Trend Intelligence | Aggregate timestamped signals by topic and geography | Candidate trend signal and evidence set | Extension; never call a small or biased sample market-wide or viral. |
| M09 | Claim Extraction | Identify figures, policy statements, dates, and affected entities | Claims with source spans and extraction state | Extraction is not verification; retain unknown/ambiguous states. |
| M10 | Source Verification | Compare each claim with linked, authoritative source evidence | Supported / contradicted / stale / unresolved result | Require source links for figures and regulatory claims; unresolved claims cannot be presented as fact. |
| M11 | Seller Impact Analysis | Explain potential seller impact from verified facts and explicit context | Evidence-linked impact note | Label inference and assumptions; do not issue legal, tax, or financial advice as fact. |
| M12 | Knowledge Store | Persist sources, versions, events, claims, evidence, drafts, and audit history | Queryable, temporally aware records | Retention, access, deletion, and backup policies require approval. |
| M13 | Weekly Digest | Select eligible events for a date range and intended audience | Draft digest with one source link per item | Exclude unsupported claims; record generation time and source snapshot/version. |
| M14 | Content Studio | Transform approved events into channel formats | Website, social, and video-script drafts | Preserve evidence references and mark every output draft-only. |
| M15 | SEO Assistant | Suggest structure, metadata, keywords, and readability edits | SEO suggestions tied to a draft version | Suggestions do not introduce uncited claims or override editorial standards. |
| M16 | Freshness Audit | Compare claims in authorized published articles with newer evidence | Findings with evidence and review state | Do not crawl or ingest articles without permission; findings are review candidates. |
| M17 | Editorial Workflow | Manage review, edits, approval, and versioning | Immutable approved version / returned draft | Approval binds to exact content hash/version; any edit invalidates prior approval. |
| M18 | Conversational Assistant | Answer scoped questions from stored, permitted evidence | Cited response or explicit insufficient-evidence result | Extension; authenticate users and never allow source content to grant tools or permissions. |
| M19 | Notifications | Route permitted alerts to configured channels | Delivery record and user-visible alert | No notification channel until auth, consent, privacy, and retry policy are designed. |
| M20 | Analytics and Evaluation | Measure source agreement, timeliness, usability, and cost | Reproducible evaluation report | Use representative samples and human-rated criteria; no fabricated baselines or success rates. |

## Proposed MVP implementation slice

Implement M01–M07, M09–M10, M12–M14, and M17 only as needed for a working ingestion-to-digest-to-approved-draft demonstration. M08, M15, M18–M20 are optional extensions unless owner review changes scope. M16 is a challenge feature and remains required for the product target; it may follow the first vertical slice if the accepted demo sequence allows it. No module is presently implemented.

## Cross-module contracts

- Every derived record links to its source record(s) and processing run.
- Date fields preserve published, fetched, observed, and effective dates separately when present.
- AI extraction/generation output is untrusted until deterministic validation and/or human review passes.
- Every job and model run records status, errors, timestamps, and relevant cost/usage fields where available.
- A state such as `unresolved` or `stale` must not silently become `verified` or disappear from the user interface.
