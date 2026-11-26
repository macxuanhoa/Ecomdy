# Project Context

**Project:** Ecomdy — AI-Powered Cross-Border Commerce Intelligence & Content Platform<br>
**Product challenge:** AI-Powered News Digest and Content Assistant for Cross-Border Sellers<br>
**Context version:** 0.1, 2026-11-26<br>
**State:** Target / proposed; application behavior is not implemented or verified in this repository.

## Users and problem

The official challenge names the Ecomdy Marketing / Content Team as direct users and Vietnamese sellers who sell internationally as beneficiaries. The brief describes frequent changes in marketplace, tax, and shipping information, the research burden of checking multiple sources, and the risk that published content becomes outdated. These are challenge-stated needs, not independently measured company research.

## Official scope

The product challenge calls for public-source monitoring, cited weekly news digests, per-item multi-channel content drafts, stale/inaccurate published-article identification, and a functional weekly demo. Public-source terms, source links for figures and regulatory claims, no fabricated information, and human review/approval are mandatory constraints. Full requirement IDs and states are in [Requirements Register](01-requirements.md).

## Proposed product direction

Evidence-first, multilingual, market-aware intelligence; database-backed history; modular services; human-controlled editorial workflow. A modular monolith with background processing is a candidate architecture, not an approved or deployed design. Candidate technology choices are listed in [Architecture](03-architecture.md) and require assessment against actual constraints before implementation.

The user-provided notes and blueprint additionally propose early social trend signals, regional relevance, Ecomdy-first sources, periodic collection, task-specific model routing, and a conversational assistant. These remain **proposed extensions**. Specific markets, platforms, refresh intervals, AI providers, and product economics are not verified or approved.

## Constraints and governance

- Preserve source provenance and distinguish observed, published, and effective dates.
- Respect source access terms and use an approved source allowlist before collection.
- Do not expose original challenge materials, credentials, or private business data in this public repository without approval.
- Generated content remains a draft until a human approves the specific version.
- No interviews, user feedback, performance measurements, operational schedules, or product tests are claimed as complete.
- DevHarness OS is packaged in `.harness/` as development infrastructure. It must not become a runtime dependency or be mixed with Ecomdy business logic.

## Current state

The local Ecomdy tree is a documentation and diagram starter. The public remote currently has one initial README commit. There is no application code, database, API, UI, source collector, model integration, deployment, or runtime evidence. See [Environment Audit](setup/00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md).
