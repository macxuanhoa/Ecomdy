# Product Requirements Document

**Version:** 0.1 · **State:** Evidence-based draft; owner approval pending · **Implementation:** None

## Product purpose

Help the Ecomdy Marketing / Content Team find relevant cross-border marketplace, tax, and shipping information; prepare source-linked weekly digests and channel-specific drafts; and identify published articles that may need correction or refresh. Vietnamese sellers who sell internationally are the intended beneficiaries. These needs come from Greenwich Industry Challenge 2026, Challenge 2, and have not yet been validated through company interviews.

## Problem and opportunity

The challenge brief describes frequent policy and marketplace changes, manual research across sources, and a risk that published content becomes stale. This document makes no claim about Ecomdy's current research time, error rate, audience size, or content-team workflow; those baselines are not in the supplied materials.

## Users

| User | Need | Evidence state |
|---|---|---|
| Ecomdy Marketing / Content Team | Find, verify, review, edit, and approve useful content | Named by the official challenge; usability feedback outstanding |
| Vietnamese cross-border sellers | Receive accurate, timely information relevant to selling internationally | Intended beneficiary; at least five interviews required and outstanding |
| Maintainer / source administrator | Configure authorized sources and maintain access policies | Proposed operating role; owner and access model TBD |

## Goals and success measures

- Monitor approved public sources for marketplace, tax, and shipping news.
- Deliver a functional weekly demonstration with an automatically generated digest and one week of sample content.
- Link every digest item and each figure or regulatory claim to source evidence.
- Produce website, social, and short-form video content drafts for each selected item.
- Flag outdated or inaccurate claims in authorized published articles.
- Keep generated content in draft until a person reviews and approves it.
- Measure assisted versus manual research/writing time, source agreement by random checks, and draft suitability with a defined team rubric. Thresholds and baselines remain TBD; no improvement is claimed.

Official requirement IDs REQ-01 through REQ-12 and success criteria SC-01 through SC-03 are authoritative in the [Requirements Register](01-requirements.md).

## Scope

### Challenge core

1. Public-source monitoring subject to source terms and an owner-approved allowlist.
2. Weekly seller-focused news digest with one source link per item.
3. Per-item website, social, and short-form video drafts.
4. Identification of stale or inaccurate claims in authorized published articles.
5. Evidence-linked review/edit/approve flow and a functional weekly demo.

### Proposed extensions

Trend signals, regional relevance, Telegram, frequent refresh beyond the accepted demo schedule, and task-specific model routing remain proposed extensions. They do not enter the approved MVP until the owner resolves the questions in [Open Questions](open-questions.md).

### Out of scope for this draft

Automatic publication; private/community source collection; legal, tax, or financial advice; unapproved markets or platforms; and claims of real-time coverage or productivity improvement.

## Product constraints and dependencies

- Use public sources only and comply with each source's terms.
- Do not fabricate information or statistics; figures and regulatory claims need linked sources.
- Human approval is required before generated content leaves draft.
- Ecomdy recommended sources, brand guidelines, and previously published articles are dependencies not present in the supplied inputs.
- Product market, source cadence, deployment, identity, provider, budget, retention, and success thresholds require owner decisions.

## Release acceptance

The challenge demo is not accepted until a running implementation generates the weekly digest and a week of sample content from authorized evidence, supplies source links, exposes review/edit/approve behavior, supports the freshness-audit requirement to the accepted demo scope, and has actual interview and Content Team feedback evidence recorded. The exact demo sequence and quantitative thresholds remain subject to owner approval.

## Traceability

See [Requirements Traceability Matrix](requirements-traceability.md), [Module Specifications](module-specifications.md), [Roadmap](05-roadmap.md), and the proposed [Task Register](task-register.md). This PRD is not an authorization to collect sources or deploy a service.
