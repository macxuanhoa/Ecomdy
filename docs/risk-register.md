# Risk Register

Scores are qualitative proposals, not measured probabilities. Reassess after owner decisions and technical discovery.

| ID | Risk | Likelihood / impact | Mitigation / evidence gate | State |
|---|---|---|---|---|
| R-01 | Source terms or rate limits prohibit planned collection | Medium / High | Approve per-source access profile, rate limit, retention, and sample connector before enabling collection. | Open |
| R-02 | Unsupported or outdated regulatory/fee claim reaches a draft | Medium / High | Claim-level citations, effective-date handling, conflict state, sampled source checks, and human approval. | Open |
| R-03 | Source content injects instructions or triggers unsafe fetches | Medium / High | Treat content as untrusted, allowlist sources, block arbitrary URLs/egress, keep tool permissions policy-bound. | Open |
| R-04 | Changes in policy are missed or detected late | Medium / High | Measure source coverage and observed lag; show last-success timestamps and coverage limits. | Open |
| R-05 | Deduplication collapses distinct policy versions | Medium / Medium | Preserve all source versions, use explicit supersession links, and test near-duplicate fixtures. | Open |
| R-06 | Inferred seller impact is presented as verified fact | Medium / High | Separate sourced claim from impact inference; show rationale and uncertainty; require review. | Open |
| R-07 | Product scope expands before challenge demo | High / Medium | Prioritize official requirements, define acceptance and defer extensions until demo evidence. | Open |
| R-08 | Missing sources, brand assets, or published articles delay implementation | High / High | Resolve input ownership and access before connector, content-style, or audit work. | Open |
| R-09 | Unverified seller/team needs lead to low adoption | Medium / High | Complete required five interviews and Content Team usability feedback; record evidence and changes. | Open |
| R-10 | AI cost, latency, or Vietnamese quality misses constraints | Medium / Medium | Build task-specific evaluation set; benchmark candidate providers by accuracy, citation retention, latency, and cost. | Open |
| R-11 | Sensitive or private data is exposed in public GitHub | Low / High | Keep originals ignored, use push protection, inspect staged files, minimize source/personal data, scan before push. | Controlled; monitor |
| R-12 | Approval becomes stale after an edit | Medium / High | Bind approval to exact content hash/version; any edit returns to draft/review. | Open |
| R-13 | No second maintainer is available to review changes | Medium / Medium | Branch protection requires CI and PR; recruit/confirm reviewers before setting a required approval count above zero. | Open |
| R-14 | A model provider retains, reviews, or uses non-public Ecomdy material beyond the task's intended processing | Medium / High | Before sending non-public source lists, brand material, drafts, or other internal data, review provider terms, retention/training controls, region, and contract; minimize/redact context and record an owner-approved provider decision. Until then, use only approved public or synthetic fixtures. | Open; provider not selected |

## Escalation conditions

Stop and request an owner decision for an unapproved source, private/community data, unresolved legal/high-impact claim, permission expansion, budget increase, production deployment, or a security control that cannot be enforced without changing project scope.
