# Project Owner Execution Guide

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Audience:** Project Owner and delegated decision makers.<br>
**Purpose:** Turn the audit into authorized, evidence-backed decisions without inventing assignments, integrations or product progress.

## 1. Owner decision summary

The project has a conditionally accepted documentation/setup baseline and a prepared fixture-first vertical-slice plan. It does not have a running product, authorized Jira, approved source/provider policies, real reviewer assignments or verified current GitHub governance settings.

The owner's next job is not to request more architecture documents. It is to make the baseline integrable, assign accountability, authorize the delivery system and approve or reject the first-slice gates.

## 2. Decision order

| Order | Decision | Required evidence | Stop condition |
|---:|---|---|---|
| 1 | PR #1 disposition | Reviewed diff, acceptance package, CI, authenticated protection/security read-back | Do not merge with unresolved blockers or missing human approval |
| 2 | Reviewer and module ownership | Real people/teams, review count, escalation path, `CODEOWNERS` decision | Do not invent handles or require unavailable reviewers |
| 3 | Jira authorization | Approved tenant/project model, least-privilege access, import mapping | Do not create a duplicate GitHub Projects backlog |
| 4 | First market/platform/source profile | Approved URLs/methods, terms, frequency, retention and attribution | No live collection without approval |
| 5 | Data and verification policy | Raw/reference retention, deletion, authority, contradiction and human-review rules | No live storage or verification claims without policy |
| 6 | AI provider and budget | Data-handling terms, evaluation set, budget, latency/quality thresholds | No paid call or non-public context before approval |
| 7 | Stack and contracts | ADR, DB/API contracts, migration ownership, team skills and operating cost | No substantive product code before contract approval |
| 8 | Vertical-slice start | `VS01-G1`–`VS01-G6` decision record | Fixture approval does not authorize live/production actions |
| 9 | Demo and expansion | Acceptance evidence, interviews, feedback, measured suitability/time | No MVP or extension claim from a fixture demo alone |

## 3. Authorization matrix

| Action | Current authorization | Required future approval/evidence |
|---|---|---|
| Edit documentation on the existing work branch | Allowed within scope | Normal diff review and deterministic checks |
| Commit/push documentation | Not performed by this audit | Explicit owner request and repository access verification |
| Merge PR #1 or PR #2 | Not authorized | Human approval, required checks, resolved conversations, governance read-back |
| Change branch protection, security settings or permissions | Not authorized | Explicit owner/security approval and rollback record |
| Create/import Jira data | Blocked | Authorized tenant/project and approved import plan |
| Assign real reviewers or `CODEOWNERS` | Not authorized | Owner-approved role-to-person mapping |
| Run fixture-only product implementation | Planned, not started | `VS01-G1`–`VS01-G6` |
| Fetch live external sources | Not authorized | Source terms/access/rate/retention approval |
| Store non-public source content | Not authorized | Retention, access, encryption and provider policy |
| Call a paid model | Not authorized | Provider terms, budget, evaluation and escalation approval |
| Run migrations or deploy | Not authorized | Reviewed migration/rollback and deployment approval |
| Publish generated content | Not authorized | Exact-version human approval and publication approval |

## 4. PR #1 and PR #2 review checklist

### PR #1 — baseline setup

- [ ] Confirm base `main` and head `setup/phase-0-audit` at `4bddc925…`.
- [ ] Review the full diff, not only the latest commit.
- [ ] Confirm `Validate repository` is successful and required by current protection.
- [ ] Confirm no local originals, credentials or sensitive files are included.
- [x] Authenticated governance/security read-back completed on 2026-11-28: strict `validate` protection, PR-only/resolved-conversation requirements, admin enforcement, no force-pushes/deletions, no rulesets, read-only default workflow permissions, and enabled secret scanning/push protection, Dependabot security updates, vulnerability alerts and private vulnerability reporting.
- [ ] Decide: approve, request changes or reject; record the decision.
- [ ] Merge only through the protected process after approval.

### PR #2 — acceptance and Phase 1 package

- [ ] Confirm it remains stacked on PR #1 and includes no duplicate baseline changes.
- [ ] Review requirements/architecture deltas, 39-row Jira CSV, vertical-slice plan and team readiness.
- [ ] Confirm capability IDs and diagrams are preserved.
- [ ] After PR #1 merges, retarget/rebase through the normal reviewed process; do not force-push.
- [ ] Do not treat Phase 1 planning as product implementation approval.

## 5. Jira activation checklist

1. Approve the Jira site/project model in [JIRA_SETUP_PLAN.md](setup/JIRA_SETUP_PLAN.md).
2. Authorize a named human administrator and least-privilege integration access.
3. Decide project key, issue types, workflow states, labels, components and epic mapping.
4. Review the 39 CSV rows; remove or defer unapproved scope before import.
5. Preserve every stable internal ID and map it to the real Jira key.
6. Import/create only approved records; verify counts, dependencies and permissions.
7. Connect the approved GitHub repository and test one branch/PR link.
8. Confirm automation cannot merge, deploy, publish, change permissions or expose private data.
9. Record the real Jira identifiers and read-back evidence in the handoff.

Do not request GitHub Projects V2 access for this Jira-first model.

## 6. Vertical-slice gate checklist

| Gate | Owner question | Acceptable evidence |
|---|---|---|
| VS01-G1 | Exactly which platform, market and source profile are approved? Is mode fixture-only or live? | Decision record with source identity, terms review and explicit mode |
| VS01-G2 | What raw text/reference may be stored, for how long, and who can access/delete it? | Approved retention/access/deletion policy |
| VS01-G3 | Are DB/API/event/claim/evidence contracts and migration ownership approved? | Reviewed contracts, fixtures and ADR |
| VS01-G4 | Which provider/data policy/budget/evaluation applies before live model use? | Provider decision, evaluation set, budget and escalation policy |
| VS01-G5 | Who reviews independently and who owns each contract? | Real reviewer mapping and capacity confirmation |
| VS01-G6 | Is substantive product implementation authorized? | Explicit owner approval referencing the accepted plan |
| VS01-G7 | Does the fixture demo satisfy acceptance without hidden gaps? | Recorded demo, exact checks, review findings and residual gaps |

Fixture-only approval never authorizes live collection, paid AI, production migration, deployment or publication. Use the [VS01 owner approval pack](vs01-owner-approval-pack.md) for plain-language decision cards, recommendations, consequences and the approval record template.

## 7. Diagram decision checklist

- Preserve all 56 sources and 26 static sets unless a task-specific change is approved.
- Treat the installed Diagram Design Plugin as an authoring/import skill, not a CI renderer.
- Record parser-only results accurately: 56/56 extracted after a one-line quoted-label compatibility fix; 482 nodes, 499 edges and zero dangling edges; no Mermaid render.
- Select and pin an independent parser/renderer only after license, dependency, sandbox/security and CI compatibility review. See [diagram tooling](setup/DIAGRAM_TOOLING.md) for the installed manifest, commands and smoke-test limits.
- Inspect changed SVG/PNG at full size before visual acceptance.
- Compare Mermaid/DOT semantic parity after source changes; do not infer parity from filenames.
- Keep all target diagrams labelled as target until as-built evidence exists.
- Do not redraw all diagrams solely for style.

## 8. Harness investment decision

Choose explicitly among:

1. **Keep advisory:** use `init`, `ingest`, `doctor`, validators and manual review; no automation claims.
2. **Harden selectively:** implement task-scope validation, budget stop conditions and durable checkpoints with tests.
3. **Defer:** document that budgets/configuration are non-enforcing and avoid autonomous execution.

Do not enable automation because a config flag exists. The CLI currently does not read or enforce the budget/automation file. CTX-01 repository/context indexing should be prototyped only after measuring a real task and defining provenance.

## 9. Reusable owner prompts

### Baseline integration review

```text
Act as an independent release reviewer. Inspect PR #1 from its actual base and full diff.
Verify branch/head SHA, CI, required checks, changed paths, secret/original-source exclusion,
and authenticated protection/security read-back. Report PASS/BLOCKED for each gate.
Do not merge, push, change settings or infer unverified configuration.
```

### Jira authorization and import

```text
Prepare Jira import execution from docs/setup/JIRA_SETUP_PLAN.md and JIRA_IMPORT_BACKLOG.csv.
Wait for explicit tenant/project authorization. Preserve internal IDs, leave unknown keys empty,
validate dependencies, and produce a dry-run mapping plus rollback plan. Do not mutate Jira yet.
```

### First-slice approval

```text
Review VS01-G1 through VS01-G6 against current evidence. For each gate, state APPROVED,
BLOCKED or REJECTED with the exact missing artifact, owner role and stop condition.
Do not start product code or live/paid actions. Identify which decisions can be made in parallel.
```

### Architecture review

```text
Review the target modular-monolith architecture and Phase 1 delta. Check source permission,
raw/processed separation, temporal provenance, deterministic-first processing, evidence states,
exact-version approval, retry/checkpoint boundaries and deployment simplicity.
Report only task-critical changes; do not rewrite valid design or propose microservices without evidence.
```

### Diagram change review

```text
Review the proposed diagram source and affected artifacts. Verify ID/version/state metadata,
gallery registration, source parity, parser result, full-size visual inspection and target/as-built label.
Do not regenerate unrelated diagrams or claim rendering that was not performed.
```

### Demo acceptance

```text
Evaluate the fixture-only Vertical Slice 01 demo against every acceptance criterion.
Record exact command/exit code/artifact for each claim, including supported, contradicted, stale,
malformed, timeout, hallucinated-citation, idempotency and approval-invalidation cases.
Separate demonstrated behavior from remaining MVP/full-product gaps. Do not invent metrics.
```

### Safe handoff

```text
Create a handoff from observed state only: repository, branch, HEAD, clean/dirty status,
PR/base/head/review/CI, changed files, stable task IDs, exact checks, skipped/blocked checks,
source/security/diagram impacts, open decisions, next task and stop/rollback conditions.
Do not change code, commit, push or resolve blockers without authorization.
```

## 10. Owner reporting template

```text
Decision date:
Decision owner:
Scope / stable IDs:
Current branch and HEAD:
Evidence reviewed:
Decision: APPROVED / BLOCKED / REJECTED / DEFERRED
Conditions:
Required follow-up owner role:
Acceptance evidence:
Stop / rollback condition:
Next review point:
```

## 11. Current owner actions

1. Review Ready PR #1; authenticated governance read-back is complete.
2. Assign real reviewers and approve review policy.
3. Authorize Jira or explicitly approve the temporary internal-ID workflow.
4. Resolve VS01-G1–VS01-G4 decisions.
5. Approve contracts and `VS01-G6` only when evidence is complete.
6. Keep all live, paid, production and publication actions behind separate approval gates.

See [COMPREHENSIVE_AUDIT.md](setup/COMPREHENSIVE_AUDIT.md) for the full evidence baseline and [BLOCKERS.md](setup/BLOCKERS.md) for active blockers.
