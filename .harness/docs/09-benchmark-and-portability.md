# Technique Benchmark and Portability Protocol

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Protocol only. No comparative benchmark has been run and no improvement percentage is claimed.

## Objective

Measure whether a technique or recipe improves verified task outcomes without increasing unacceptable scope, security or reproducibility risk.

## Five comparison arms

Run the same approved task against:

1. ordinary coding agent;
2. scoped context only;
3. scoped context plus selected skills;
4. spec workflow;
5. complete recipe with trace/checkpoint discipline.

Do not add all candidates at once. Each arm must be independently reproducible.

## Controlled variables

Hold constant where feasible:

- task contract and acceptance criteria;
- repository baseline commit;
- fixture data and source permissions;
- model/provider/version and decoding settings;
- agent host/version and tool permissions;
- operating system and dependencies;
- retry, runtime and cost ceilings;
- evaluator and evidence rules.

Record every unavoidable difference. Do not compare results from different task scopes and attribute the difference to a technique.

## Metrics

| Dimension | Measures |
|---|---|
| Success | Task completed and accepted by the defined evaluator |
| Acceptance coverage | Passed criteria / total criteria |
| Verification | Tests/checks actually run and evidenced |
| Regression | Existing behavior broken by the change |
| Scope | Out-of-scope, forbidden or unrelated path changes |
| Runtime | Observed wall time |
| Tokens/cost | Provider-reported values only; otherwise `unknown` |
| Retries/interventions | Repeated attempts and human corrections |
| Quality | Review findings, citation/evidence defects, accessibility/security issues as applicable |
| Reproducibility | Same inputs/versions produce compatible result and evidence |

No token estimates may be presented as provider-reported usage. No benchmark result may be inferred from agent confidence or multiple-model agreement.

## Run record

Each run records:

- task/run/trace IDs and baseline commit;
- arm, route, profile, recipe and technique IDs;
- exact tool/skill/model versions;
- context manifest hashes and excluded paths;
- commands, exit codes and evidence artifacts;
- approvals, blockers, retries and stop reasons;
- observed resources with `unknown` fields preserved;
- evaluator identity/role and final disposition.

## Evaluation rules

- Define acceptance before running the task.
- Use deterministic fixtures for parser, schema, validation and migration tasks.
- Use an independent reviewer for implementation acceptance.
- Report failures and excluded runs; do not silently select the best attempt.
- Separate model nondeterminism from harness/tool defects.
- Treat source evidence, not model consensus, as truth.

## Security and cost controls

- No production target, private corpus or paid provider without separate authorization.
- Disable unapproved telemetry, sharing and remote generation.
- Bound concurrency, runtime, retries and spend before execution.
- Do not upload source documents or credentials to evaluation services.
- Red-team only authorized non-production targets.

## Portability acceptance

A technique is portable only when a clean environment can:

1. install or access the pinned artifact through documented steps;
2. configure it without hidden user-scope dependencies;
3. expose it to the intended agent host;
4. pass a bounded smoke test;
5. run the approved workflow;
6. produce equivalent evidence;
7. update, uninstall and recover without losing unrelated work.

User-scope installations are not inherited through Git and must not be documented as repository-provided capabilities.
