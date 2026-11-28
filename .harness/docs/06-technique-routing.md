# Technique Routing, Profiles and Recipes

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Advisory design. No routing CLI, task executor or model router is implemented.

## Sources of truth

| Registry | Purpose |
|---|---|
| [`.harness/registry/routing/profiles.json`](../registry/routing/profiles.json) | Nine execution profiles and limits |
| [`.harness/registry/routing/manifests.json`](../registry/routing/manifests.json) | Fourteen deterministic task routes |
| [`.harness/registry/routing/recipes.json`](../registry/routing/recipes.json) | Twenty-four reusable workflow recipes |
| [`.harness/schemas/routing.schema.json`](../schemas/routing.schema.json) | JSON Schema Draft 2020-12 contract |
| [`.harness/scripts/validate_routing.py`](../scripts/validate_routing.py) | Standard-library reference and invariant checks |

## Deterministic selection procedure

A human or future adapter should apply this order:

1. Read the approved task contract: objective, task type, allowed paths, acceptance checks, dependencies, budget and stop conditions.
2. Reject or block the task if authority, scope or required inputs are missing.
3. Match explicit task-type and activation rules against a route manifest. Do not infer a route from vague keywords alone.
4. Use the route's profile and required techniques. Optional techniques require a stated reason.
5. Remove incompatible techniques and stop if a required technique is incompatible.
6. Compile the ordered steps, context scope, verification gates, approvals, stop conditions and fallback into an explainable advisory recipe.
7. Record the selection before execution. A selection is not an attempt, an execution or verification.

If no route matches, return `NO_MATCH` with guidance. Do not guess a framework or activate the whole technique library.

## Profiles

| Profile | Intended use | Agent default |
|---|---|---|
| QUICK | Small, bounded, low-risk change | 1 |
| STANDARD | Normal reviewed implementation/documentation | 1 |
| DEEP | Multi-file or high-uncertainty analysis | 1 |
| PARALLEL | Independent tasks with explicit merge/reconciliation plan | Up to 3; opt-in only |
| AUTONOMOUS | Future bounded runtime design | 1; `BLOCKED` |
| DEBUG | Reproduction-first failure analysis | 1 |
| DESIGN | Architecture, diagram or UI design work | 1 |
| SECURITY | Authorized defensive security review | 1 |
| AUDIT | Evidence and traceability review | 1 |

Only `PARALLEL` may default to more than one agent. `AUTONOMOUS` remains `BLOCKED` until runtime controls are approved and verified.

## Routes and recipes

The 14 routes cover quick documentation, documentation, feature, bug, refactor, exploration, requirements, architecture, API, data, security, diagram, audit and parallel research.

The 24 recipes cover feature, bug, refactor, exploration, requirements, architecture, API, database/migrations, data collection, data processing, AI workflow, RAG, LLM evaluation, UI, browser testing, security review, performance, diagram, documentation, PR review, release, handoff, interrupted recovery and parallel development.

A recipe is reusable guidance, not proof that its workflow ran.

## Context policy

- Start with repository rules and a task-scoped context manifest.
- Prefer exact search, symbol/AST/SQL retrieval and relevant excerpts over whole-repository ingestion.
- Exclude `docs/00-original/**` and `.harness/docs/00-original/**` by default.
- Record path, hash, authority and reason for every loaded file.
- Deduplicate overlapping excerpts and preserve provenance.
- Apply progressive disclosure: load detail only when the current step needs it.
- Context byte/file limits are advisory until an approved loader enforces them.

## Enforcement layers

| Layer | Can enforce | Cannot establish alone |
|---|---|---|
| Prompt/instruction | Desired behavior and stop rules | Host-independent enforcement |
| Agent-host hook | Host event interception within its documented scope | Control over every terminal/tool path |
| Local script | Deterministic validation and bounded child execution | Prevention of unrelated direct shell use |
| Git hook | Repository event checks when installed and not bypassed | Server-side review or protected-branch policy |
| CI | Remote checks on submitted changes | Local pre-merge behavior or unreviewed runtime actions |
| OS/process sandbox | Process, filesystem, network and resource boundaries | Product correctness |
| Repository protection | Merge/push/review rules | Content truth or test quality |

Do not claim that a Python script or prompt blocks every action available to an agent with independent terminal access.

## Explainability record

For each selection record:

- task ID and input hashes;
- matched route/profile/recipe IDs;
- selected, optional, excluded and incompatible technique IDs;
- reason for each inclusion/exclusion;
- context scope and limits;
- verification gates, approvals and stop conditions;
- fallback if execution is unavailable.

Use the [execution trace contract](07-execution-traces-and-checkpoints.md) to distinguish selection from later runtime states.

## Supported checks

```bash
python .harness/scripts/validate_routing.py
python -m unittest discover -s .harness/tests -p "test_routing.py" -v
```

There is no `harness.py route`, `recipe compile` or autonomous execution command. Such names in planning documents remain proposed until implemented and tested.
