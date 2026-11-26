# Requirements Register

**Baseline:** Greenwich Industry Challenge 2026 × Ecomdy, Challenge 2.<br>
**Source:** `docs/00-original/challenge-brief.xlsx` (both sheets). Original workbook is local-only and ignored by Git.<br>
**As of:** 2026-11-26. **Implementation status:** all requirements below are open; this repository has no Ecomdy application implementation.

## Priority and state definitions

- **P0 — Challenge core:** necessary for the required functional demo or mandatory product constraints.
- **P1 — Discipline / validation:** explicitly required task or success measure that needs stakeholder activity or evidence.
- **Open — Not implemented / not verified:** no implementation or acceptance evidence is present.

## Official requirement register

| ID | Requirement | Type | Priority | Source | State |
|---|---|---|---|---|---|
| REQ-01 | Automatically monitor public sources for marketplace, tax, and shipping news. | Functional | P0 | Challenge Briefs!B8, item 1 | Open — no collector or source allowlist |
| REQ-02 | Compile a weekly digest for Vietnamese sellers and provide a source link for every news item. | Functional | P0 | Challenge Briefs!B8, item 2 | Open — no digest runtime or evidence records |
| REQ-03 | Produce per-item draft content for discoverable website articles, social posts, and short-form video scripts. | Functional | P0 | Challenge Briefs!B8, item 3 | Open — no content runtime |
| REQ-04 | Identify published articles containing outdated or inaccurate information that needs an update. | Functional | P0 | Challenge Briefs!B8, item 4 | Open — no audit runtime or authorized article corpus |
| REQ-05 | Use only public sources and comply with each source's terms. | Mandatory constraint | P0 | Challenge Briefs!B12, item 1 | Open — source policy and collection controls not implemented |
| REQ-06 | Link every figure and regulatory claim to a source; do not fabricate facts or statistics. | Mandatory constraint | P0 | Challenge Briefs!B12, item 2 | Open — no claim/evidence verifier |
| REQ-07 | Keep generated content in draft form until a person reviews and approves it. | Mandatory constraint | P0 | Challenge Briefs!B12, item 3 | Open — no editorial workflow |
| REQ-08 | Deliver a functional demo with an automatically generated weekly digest and one week of sample content. | Required deliverable | P0 | Challenge Briefs, B9 | Open — no running application/demo |
| REQ-09 | Interview at least five online sellers about information needs and usual sources. | Business discipline task | P1 | Tasks by Discipline!B7, item 1 | Open — no interview evidence |
| REQ-10 | Identify highest-priority topics, create a publishing calendar, and propose how content can attract customers to Ecomdy. | Business discipline task | P1 | Tasks by Discipline!B7, items 2–3 | Open — no validated calendar/proposal |
| REQ-11 | Collect public news, create accurate source-cited summaries, remove duplicates/outdated news, and draft channel-specific content. | Technology discipline task | P1 | Tasks by Discipline!B8, items 1–4 | Open — no processing pipeline |
| REQ-12 | Provide readable templates and a review/edit/approve interface; obtain Ecomdy Content Team feedback. | Design discipline task | P1 | Tasks by Discipline!B9, items 1–3 | Open — no UI or feedback evidence |

## Success criteria and dependencies

| ID | Criterion / dependency | Source | State |
|---|---|---|---|
| SC-01 | Research and writing time is significantly reduced versus the manual process. | Challenge Briefs!B10, item 1 | Measurement method and baseline are not supplied; no result claimed. |
| SC-02 | Digest information agrees with original sources through random checks. | Challenge Briefs!B10, item 2 | Sampling protocol and results are not supplied. |
| SC-03 | Ecomdy Content Team considers a substantial number of drafts suitable. | Challenge Briefs!B10, item 3 | “Substantial” threshold requires owner definition; no feedback evidence. |
| DEP-01 | Ecomdy recommended news sources. | Challenge Briefs!B11, item 1 | Not present in supplied materials. |
| DEP-02 | Ecomdy brand guidelines. | Challenge Briefs!B11, item 2 | Not present in supplied materials. |
| DEP-03 | Previously published Ecomdy articles for freshness audit reference. | Challenge Briefs!B11, item 3 | Not present in supplied materials. |

## Proposed extensions (not official requirements)

The supplied JPG and master blueprint propose social trend signals, market/region relevance, database-first collection, frequent refresh, task-specific model routing, and a plain-text/Telegram assistant. These ideas are recorded as **proposed** in [Project Context](project-context.md); they do not change this official requirements register without owner approval.
