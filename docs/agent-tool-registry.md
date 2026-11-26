# Agent and Tool Registry

**State:** Proposed product-side roles and tool boundaries. No product agents, provider adapters, or tool executor are implemented. DevHarness OS roles belong to a separate development harness.

## Product role profiles

| ID | Role | Responsibility | Allowed evidence / output | Approval boundary |
|---|---|---|---|---|
| PA-01 | Source Researcher | Summarize newly collected source material | Permitted article versions and source metadata | Cannot approve source access or fetch arbitrary URLs. |
| PA-02 | Market Analyst | Relate verified events to market/platform context | Controlled taxonomy and cited event records | Must mark seller-impact reasoning as inference. |
| PA-03 | Claim Extractor | Extract figures, policy claims, and effective dates | Source spans linked to a version | Extraction does not establish truth. |
| PA-04 | Evidence Verifier | Compare claim with evidence and identify conflict/staleness | Claim/evidence records and source authority rules | Cannot mark unresolved claims verified without evidence. |
| PA-05 | Digest Composer | Draft an audience-specific digest from eligible events | Verified/qualified event set with citations | Output remains a draft. |
| PA-06 | Channel Writer / SEO Assistant | Produce web/social/video format variants | Approved facts, brand guide, channel template | Cannot add uncited figures or publish. |
| PA-07 | Content Auditor | Identify changed/stale claims in authorized published material | Authorized article and newer evidence | Findings are review candidates, not automatic edits. |
| PA-08 | Editorial Quality Reviewer | Check citations, structure, language, and policy compliance | Draft version plus all supporting evidence | Human editor retains final approval. |

Roles may be deterministic services, model calls, or human activities. They are not assumed to be separate long-running agents. Model/provider selection is deferred to task-level benchmark evidence.

## Tool boundary registry

| Tool family | Target permission | Guardrail / check |
|---|---|---|
| Source connector | Read approved hosts/configured endpoints only | Per-source allowlist, terms, rate limit, timeout, egress restriction. |
| Evidence retrieval | Read records visible to current user/task | Tenant/role checks and citation provenance. |
| Draft generation | Create draft/version only | No publication permission; schema and citation validation. |
| Editorial actions | Review/approve exact version | Role check, audit event, approval invalidated by edit. |
| Notifications | Send only configured approved content | Consent, target validation, rate limit, no secret or private source text. |
| Administration | Manage source configuration and roles | Least privilege, confirmation for high-impact changes, audit trail. |

Provider adapters, web search, Telegram, and social-network connectors are candidates only. Do not install or grant access until the need, permission, data handling, cost, and verification method are documented.
