# Software Requirements Specification

**Version:** 0.1 · **State:** Proposed technical baseline · **Implementation:** None

This SRS converts the challenge requirements into candidate system behavior and quality gates. The official source and states remain in the [Requirements Register](01-requirements.md); no requirement below proves a runtime feature exists.

## System boundary

The target product includes source configuration, permitted collection, processing and provenance, evidence storage/retrieval, digest and content drafting, freshness findings, editorial review, and a user interface. A modular monolith with background work is a candidate; service decomposition and technology choices are not approved. DevHarness is development infrastructure outside this runtime boundary.

## Functional requirements

| SRS ID | Behavior | Trace | Acceptance evidence |
|---|---|---|---|
| SYS-01 | Collect only configured public sources after source terms and access method are approved. | REQ-01, REQ-05 | Connector fixture demonstrates allowlist, request limits, provenance, and rejection of unapproved hosts. |
| SYS-02 | Preserve article identity, source version, observed/published/effective dates, fetch outcome, and content hash where retention is permitted. | REQ-01, REQ-05 | Versioned fixtures and date-integrity tests; retention policy approved. |
| SYS-03 | Normalize, deduplicate, classify, and cluster source records while retaining distinct updates and their source relationships. | REQ-11 | Deterministic fixture tests include exact duplicates and distinct policy versions. |
| SYS-04 | Extract atomic claims with source spans and keep extraction separate from verification. | REQ-06, REQ-11 | Each extracted claim points to a source version and span; ambiguous cases remain unresolved. |
| SYS-05 | Associate evidence with each figure or regulatory claim and represent supported, contradicted, stale, and unresolved outcomes. | REQ-06 | Source-agreement sample and conflict fixtures; unsupported claims cannot be presented as verified. |
| SYS-06 | Automatically generate a weekly digest for a configured period and audience on an owner-approved schedule; every item includes a source link and eligible evidence. Scheduling remains disabled until sources, runtime, and schedule are approved. | REQ-02, REQ-08 | Controlled scheduler test proves a scheduled run creates the weekly digest and one-week sample with eligible items, links, freshness, and no unsupported claims; disabled configuration performs no fetch. |
| SYS-07 | Produce separate website, social, and short-video-script drafts for a selected digest item. | REQ-03, REQ-11 | Schema and citation-preservation tests for each format. |
| SYS-08 | Import only authorized published articles, compare their claims with newer evidence, and return reviewable freshness findings. | REQ-04, REQ-12 | Old/new article fixtures create dated findings; unauthorized URLs are rejected. |
| SYS-09 | Support review, edit, return, and approval against an immutable content version/hash. | REQ-07, REQ-12 | State-transition and authorization tests; any edit invalidates a previous approval. |
| SYS-10 | Record source, processing, AI-run, editorial, and approval provenance with visible failure status. | REQ-06, REQ-07 | Audit fixtures connect action, actor, version, evidence, outcome, and timestamp. |

## Quality and security requirements

| SRS ID | Requirement | State / verification approach |
|---|---|---|
| Q-01 | Accuracy must be measured against original evidence and reported with sample size and results. | Method proposed; benchmark and acceptance thresholds TBD. |
| Q-02 | Collection must respect approved source terms, per-source limits, timeouts, bounded retries, and constrained egress. | Proposed; source allowlist and runtime controls not implemented. |
| Q-03 | External text and generated output are untrusted; no source text may authorize a tool or permission. | Proposed security gate; adversarial fixtures required. |
| Q-04 | User identity and role must govern source configuration, review, approval, and export. | Identity provider and role mapping TBD. |
| Q-05 | Secrets and unnecessary private data must not enter prompts or logs; provider requests require a data-handling review. | Provider not selected; no model calls implemented. |
| Q-06 | Every operation must expose status, timestamps, and actionable errors; retries and model usage are bounded. | Thresholds, retention, and operational ownership TBD. |
| Q-07 | User-visible generated material stays draft-only until the exact version is approved by an authorized person. | Mandatory policy; workflow not implemented. |
| Q-08 | Product behavior is tested with reproducible fixtures, regression tests, security checks, and human-rated Vietnamese quality samples. | Strategy in [Validation](06-validation.md); no product tests exist yet. |

## Interfaces and data contracts

The candidate API is documented in [API Design](api-design.md); proposed entities are in [Database Design](database-design.md). Request schemas, source connector protocols, identity provider, deployment environment, and model provider remain TBD. No endpoint or schema is currently implemented.

## Verification states

Requirements move from proposed/open to implemented only with code and tests, and to verified only with recorded acceptance evidence. Owner-approved source access, product scope, provider policy, and retention decisions are prerequisites, not implied by this SRS.
