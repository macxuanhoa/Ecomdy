# Ecomdy Engineering Technique Mapping

**Status:** Proposed mapping / 2026-11-28. No Ecomdy product module is implemented by this document.<br>
**Authority:** Module IDs M01–M20 remain defined in [Product vision](02-product-vision.md); workflow IDs remain defined in [Workflows](04-workflows.md).<br>
**Machine-readable source:** [Ecomdy mapping registry](../.harness/registry/ecomdy-mapping.json).

## Purpose and boundary

This mapping recommends which DevHarness techniques, skills, tools, roles, tests and evidence are relevant to each proposed Ecomdy module. It does **not**:

- turn a suggested technique into a mandatory product requirement;
- approve a source, provider, crawler, paid service, database, deployment or notification channel;
- change the 70-capability matrix, official requirements, architecture or Jira backlog;
- claim that a proposed module, agent or workflow is implemented.

DevHarness remains development infrastructure under `.harness/`; it is not an Ecomdy runtime dependency.

## How to use

1. Start from the approved requirement and module/workflow ID.
2. Read the module row below and the full JSON record for techniques, roles, tests and evidence.
3. Select only techniques relevant to the approved task; do not activate the entire registry.
4. Use the [routing guide](../.harness/docs/06-technique-routing.md) to choose an advisory profile and recipe.
5. Keep selected, attempted, executed and verified states separate in the execution trace.
6. Stop when source authority, provider policy, permissions or acceptance evidence is missing.

## Module mapping

| Module | Lifecycle area | Recommended techniques | Minimum verification | Evidence to retain |
|---|---|---|---|---|
| M01 Source Management | Data source registration | TECH-002, TECH-018, TECH-026, TECH-036, TECH-037 | Terms/authority decision; URL and private/reserved IP controls; least-privilege audit | Source profile version, approval, terms/access review, configuration diff |
| M02 Data Collection | Multi-platform collection | TECH-018, TECH-023, TECH-026, TECH-027, TECH-036, TECH-039 | Allowlist/egress; rate/timeout/retry bounds; provenance and failure state | Approved source ID, run ID, capture metadata, retry/failure log |
| M03 Scheduled Crawling | Deployment and automation | TECH-005, TECH-012, TECH-015, TECH-025, TECH-039, TECH-040 | Idempotency; checkpoint/resume; circuit-break and budget stop | Schedule approval, job history, checkpoint, pause event |
| M04 Data Normalization | Data processing | TECH-018, TECH-023, TECH-027 | Schema, date/URL/language fixtures; malformed input state; provenance | Input/output hashes, parser version, fixture results |
| M05 Deduplication | Data processing | TECH-023, TECH-027 | Exact/near-duplicate fixtures; distinct evidence preserved | Rule version, matched IDs, threshold evaluation |
| M06 News Classification | Data processing | TECH-023, TECH-024, TECH-027 | Versioned taxonomy; low-confidence review; fixed dataset | Taxonomy, model/prompt version if used, evaluation, overrides |
| M07 Market Intelligence | Evidence verification | TECH-001, TECH-024, TECH-028, TECH-029 | Evidence authority; inference/fact separation; conflict/stale states | Claim/evidence IDs, effective date, result, reviewer decision |
| M08 Trend Intelligence | Industry validation | TECH-022, TECH-023, TECH-024, TECH-025 | Coverage caveats; versioned weights; sparse-sample limits | Corpus snapshot, scoring policy, evaluation, approval |
| M09 Claim Extraction | Claim extraction | TECH-018, TECH-023, TECH-026, TECH-027, TECH-028, TECH-030 | Source span/schema; provider-free fixtures; injection isolation | Article version, claim span, schema, provider metadata if used |
| M10 Source Verification | Evidence verification | TECH-001, TECH-023, TECH-025, TECH-028, TECH-029 | Citation existence/relevance; authority/date; high-impact escalation | Result, evidence snapshot, rule version, human review |
| M11 Seller Impact Analysis | Evidence verification | TECH-002, TECH-024, TECH-028 | Inference labels; verified-fact rationale; fixed evaluation | Impact record, supporting claims, provider metadata, review |
| M12 Knowledge Database | Knowledge database | TECH-018, TECH-019, TECH-027, TECH-036 | Constraints/provenance; migration/rollback; access and restore fixture | Schema, migration/rollback evidence, access review, restore result |
| M13 Weekly Digest | News digest | TECH-023, TECH-025, TECH-028, TECH-029 | Eligible verified claims only; citations; explicit empty period | Evidence snapshot, digest hash, validation, approval |
| M14 Content Studio | Content generation | TECH-026, TECH-028, TECH-029, TECH-030, TECH-035 | Channel schema/citations; unsupported-claim rejection; version boundary | Draft versions, evidence links, provider metadata, browser/review evidence |
| M15 SEO Assistant | Content generation | TECH-024, TECH-028, TECH-029 | No invented claims; brand constraints; citation preservation | Template/prompt version, draft, evaluation, review |
| M16 Content Freshness Audit | Content audit | TECH-001, TECH-021, TECH-023, TECH-028, TECH-029 | Corpus permission; effective dates; human review; no auto-edit | Article version, comparison, finding, review candidate |
| M17 Editorial Workflow | Content approval | TECH-004, TECH-013, TECH-025, TECH-029, TECH-038 | Role transitions; hash-bound approval; edit invalidation; audit | Draft hash, actor/role, decision, transition log |
| M18 Conversational Assistant | Multi-agent intelligence | TECH-026, TECH-027, TECH-028, TECH-030, TECH-036 | Permission-filtered retrieval; abstention; injection isolation; citations | Query scope, evidence IDs, response/citations, escalation |
| M19 Notification System | Telegram/notifications | TECH-018, TECH-025, TECH-036, TECH-039, TECH-040 | Consent/target; retry cap; no private text; failure state | Consent, approved template/target, delivery log, stop event |
| M20 Analytics and Evaluation | Industry validation | TECH-022, TECH-023, TECH-024, TECH-025, TECH-040 | Fixed baseline/dataset; success/regression/scope metrics; measured usage only | Benchmark config, raw results, versions, limitations |

The full registry also records recommended skills, candidate tools, responsible role placeholders and techniques that are not currently needed for each module.

## Cross-cutting lifecycle areas

| Area | Recommended techniques | Required evidence | Boundary |
|---|---|---|---|
| Requirements and architecture governance | TECH-001, TECH-002, TECH-003, TECH-031, TECH-032 | Traceability, ADR, target/as-built label | Delivery governance, not a new product module |
| Dashboard and UI/UX | TECH-034, TECH-035, TECH-023 | Browser golden/edge paths, accessibility findings, component/state contracts | No dashboard exists; browser verification is blocked until an approved preview exists |
| Deployment and release | TECH-019, TECH-025, TECH-036, TECH-037, TECH-038, TECH-040 | Release checklist, rollback, security scan, human approval | No production deployment is authorized |
| Team collaboration and parallel development | TECH-005, TECH-013, TECH-014, TECH-015, TECH-038 | Dependency/path analysis, independent review, reconciled checkpoint | Parallelism is opt-in; Jira remains the intended task authority |

## Product-role boundary

Ecomdy product roles PA-01–PA-08 remain defined in [Agent and tool registry](agent-tool-registry.md). DevHarness roles A01–A24 remain development/orchestration roles. A mapping row does not create a long-running agent instance; deterministic services, model calls or human activities may fulfill a role after approval.

## Current blockers

- No Ecomdy runtime, source connector, provider adapter, database, UI, scheduler or deployment exists.
- Jira access and real ownership assignments remain unresolved; role placeholders are intentional.
- Live collection, paid AI calls, Telegram and production actions require separate authorization.
- External tool candidates remain research/approval items until installation, configuration, session availability, smoke testing and integration are independently evidenced.
