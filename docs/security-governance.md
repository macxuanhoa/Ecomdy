# Security and Governance Specification

**State:** Proposed product controls; no Ecomdy runtime or production security controls are implemented. Repository-level GitHub settings are documented separately in the setup audit.

## Trust boundaries

1. **External source content** is untrusted data. It cannot authorize network requests, override system instructions, or supply executable code.
2. **Connectors and worker** use a source allowlist, constrained egress, per-source limits, timeouts, and bounded retries.
3. **AI provider** receives only task-scoped, necessary context after an owner-approved provider policy and data-handling review. Non-public Ecomdy sources, brand assets, drafts, and business data stay out of provider requests until terms, retention/training controls, and applicable contracts are reviewed. Secret-bearing configuration never enters prompts, logs, or content output.
4. **Editorial users** have explicit roles; source/configuration changes and approvals are audited.
5. **Publishing/export** is a separate gated action. The challenge requires a human approval step before generated content leaves draft.

## Required controls before implementation

- Source allowlist, terms review, access method, rate limits, retention, and takedown/contact process.
- Authentication, role-based authorization, session management, CSRF protections where applicable, and secure admin defaults.
- Input validation for URLs, uploads, prompt/source text, templates, generated output, and rich-text rendering.
- Egress controls to prevent SSRF and arbitrary browsing; URL normalization and private/reserved IP blocking.
- Prompt-injection defenses: isolate source text as untrusted; tools and permissions come only from policy, never source instructions.
- Citation validation: ensure cited IDs/URLs exist, relate to the claim, and are visible to the user; do not equate link presence with factual proof.
- Human approval binds to an immutable content version; a post-approval edit requires review again.
- Secrets management, least-privilege service identities, rotation, encrypted transport/storage, backups, and secret scanning.
- Data minimization, no private community data without explicit permission, retention/deletion schedules, and access logs.
- Bounded AI/provider usage, timeout/retry/cost limits, output schema validation, failure states, and fallback behavior.

## Editorial risk tiers

| Tier | Example | Minimum handling |
|---|---|---|
| Routine content | General educational summary with linked sources | Citation checks and human editorial review before approval. |
| High-impact claim | Tax, regulation, fees, shipping restrictions, or numerical/statutory claim | Authoritative evidence, effective-date check, explicit uncertainty handling, second-person review if owner policy requires it. |
| Unsafe/unsupported | No source, conflicting evidence, personal data, or unclear access rights | Stop generation/export or label unresolved; escalate to authorized human. |

## Logging and incident readiness

Log request/run identifiers, actor, source IDs, model/task metadata, status, and errors. Do not log tokens, credentials, unnecessary full source content, or personal data. Define alert ownership, incident severity, containment, secret revocation, source takedown, backup restoration, and user notification before deployment.

## Current repository controls

Authenticated read-back on 2026-11-28 verified GitHub secret scanning/push protection, vulnerability alerts, Dependabot security updates, private vulnerability reporting, and `main` protection requiring PRs, strict `validate` checks and resolved conversations with admin enforcement and no force-pushes/deletions. No repository rulesets are configured, and the current protection requires zero approving reviews; the project nevertheless requires explicit human review before merge. These repository controls do not secure a future product runtime. See the [verification report](setup/VERIFICATION_REPORT.md) for current evidence and [Phase 0 acceptance](setup/PHASE_0_ACCEPTANCE.md) for the historical snapshot.
