# Technique Routing, Profiles and Recipes

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Advisory routing and capability inspection implemented and tested. No task executor, model router or autonomous runtime is implemented.

## Sources of truth

| Registry | Purpose |
|---|---|
| [`.harness/registry/routing/profiles.json`](../registry/routing/profiles.json) | Nine execution profiles and limits |
| [`.harness/registry/routing/manifests.json`](../registry/routing/manifests.json) | Fourteen deterministic task routes |
| [`.harness/registry/routing/recipes.json`](../registry/routing/recipes.json) | Twenty-four reusable workflow recipes |
| [`.harness/schemas/routing.schema.json`](../schemas/routing.schema.json) | JSON Schema Draft 2020-12 contract |
| [`.harness/scripts/validate_routing.py`](../scripts/validate_routing.py) | Standard-library reference and invariant checks |
| [`.harness/scripts/technique_router.py`](../scripts/technique_router.py) | Deterministic advisory route selection and explainability record |
| [`.harness/scripts/capability_doctor.py`](../scripts/capability_doctor.py) | Local capability lifecycle inspection |
| [`.harness/harness.py`](../harness.py) | `route` and `capabilities` CLI entry points |

## Deterministic selection procedure

The implemented router applies this order:

1. Validate the routing facts and reject malformed task input.
2. Block `execution_mode: AUTONOMOUS` before registry evaluation.
3. Evaluate every explicit activation rule. Missing fields do not match; keywords are not used to infer a route.
4. Select the unique matching route with the most activation rules. Equally specific matches require an explicit matching `route_id`.
5. Return `NO_MATCH` when no route matches; never silently choose a framework.
6. Select required techniques, block required conflicts or route incompatibilities, and accept optional techniques only when the route allows them and a non-empty reason is supplied.
7. Return the ordered sequence, context scope, limits, gates, approvals, stop conditions, fallback and compatible recipe IDs with every route decision.
8. Record the selection as `RECOMMENDED` and `NOT_EXECUTED`.

A requested `route_id` narrows the matching candidates but does not override activation rules. Optional techniques that conflict with selected techniques are excluded with a reason rather than treated as execution evidence.

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

## Supported commands

Run from the repository root. The router accepts a JSON object on stdin by default, or a file through `--task`. The minimum routing facts for the quick-documentation route are shown below; other routes require the activation facts in their manifests.

```json
{
  "task_id": "TASK-ROUTE-001",
  "task_type": "documentation",
  "risk": "low",
  "complexity": "low",
  "changed_file_count": 2,
  "mutation_required": true
}
```

```bash
python .harness/harness.py route --task task.json --output route.json
python .harness/scripts/technique_router.py task.json
python .harness/harness.py capabilities
python .harness/scripts/capability_doctor.py --session-skill TOOL-013
python .harness/scripts/capability_doctor.py --strict
python .harness/scripts/validate_routing.py
python -m unittest discover -s .harness/tests -p "test_technique_router.py" -v
python -m unittest discover -s .harness/tests -p "test_capability_doctor.py" -v
python -m unittest discover -s .harness/tests -p "test_harness.py" -v
```

Route exit codes are `0` for `RECOMMENDED`, `2` for `NO_MATCH`, `3` for `BLOCKED`, and `1` for input errors. These codes describe selection only. They do not report task execution.

Capability exit codes are `0` for a valid inspection, `1` for inspection/registry failure, and `2` for `--strict` when a registered tool is `BLOCKED`.

## Capability lifecycle inspection

Capability Doctor reports `registered`, `installed`, `configured`, `available_in_session`, `smoke_tested`, `integrated` and `verified` independently. Each value is `true`, `false` or `null`; `null` means unknown, not failed.

- Internal skills are discovered under `.harness/skills`. Project copies under `.qoder/skills` must match the canonical `SKILL.md` and a matching local `skills-lock.json` source record before configuration is reported.
- CLI artifacts are detected from recorded activation paths or known commands on `PATH`. Diagram Design is detected only at its recorded or pinned plugin version.
- Current-session availability is `true` only for a capability explicitly observed through `--session-skill`; absence from that optional observation remains unknown.
- A smoke-test record does not imply integration. Verification is not reported for a tool whose recorded artifact is missing and has no detected fallback.
- The inspection is not an OS sandbox, a complete host catalog or proof that another contributor inherited user-scope installations.

## Implementation boundary

The routing and capability commands are local advisory tools. They do not execute tasks, invoke agents, enforce filesystem/process boundaries, compile recipes or provide model routing. `harness.py recipe compile` and autonomous execution remain unimplemented. Context and runtime limits remain advisory until R05–R07 add reviewed enforcement and evidence contracts.
