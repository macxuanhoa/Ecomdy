# Engineering Technique Library

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** `AVAILABLE IN REGISTRY`; advisory design. No runtime router, installer, provider adapter or autonomous executor is implemented.

## Authority and boundary

The machine-readable source of truth is [`.harness/registry/techniques.json`](../registry/techniques.json), validated against [`.harness/schemas/technique.schema.json`](../schemas/technique.schema.json).

The supplied directive refers to a 145-technique catalogue. That catalogue was not present in the repository, attachment or inspected workspace. The registry therefore contains an explicitly labelled initial set of **40 techniques**, five in each category A–H. It does not fabricate the missing 145 entries and does not substitute the separate 151-name proposed skill catalogue in [Agent, skill and tool registry](02-registries.md).

DevHarness techniques are development methods and controls. They do not change Ecomdy product requirements, module status, architecture, Jira backlog or runtime scope.

## Taxonomy

`category` describes where a technique is used. `kind` describes what it is. These are independent fields.

| Category | Area | Initial techniques |
|---|---|---|
| A | Requirements, specification and planning | TECH-001–TECH-005 |
| B | Context engineering and token optimization | TECH-006–TECH-010 |
| C | Agent engineering and orchestration | TECH-011–TECH-015 |
| D | Coding and software engineering | TECH-016–TECH-020 |
| E | Testing, debugging and evaluation | TECH-021–TECH-025 |
| F | AI product engineering | TECH-026–TECH-030 |
| G | Architecture, diagram and UI/UX | TECH-031–TECH-035 |
| H | Collaboration, security and automation | TECH-036–TECH-040 |

Allowed kinds are `methodology`, `design_pattern`, `agent_pattern`, `skill`, `tool`, `mcp_server`, `framework`, `script`, `workflow` and `policy`.

A non-executable technique has `invocation: null`. An invocation may be recorded only with an observed `SMOKE TESTED` or `VERIFIED` status. Research or installation alone is not invocation evidence.

## Technique card contract

Every card includes:

- stable ID, name, category and kind;
- description, purpose and problem solved;
- when to use and when not to use it;
- triggers, prerequisites, inputs and outputs;
- supporting skills/tools and compatible DevHarness agent roles;
- workflow, example prompt and actual invocation when available;
- an Ecomdy example;
- acceptance criteria and verification method;
- security controls;
- resources and source references;
- conflicts, alternatives and fallback;
- implementation and lifecycle status.

The validator rejects unknown fields, duplicate IDs, empty required values, invalid roles, unknown references, unverified invocations and fabricated resource measurements.

## Lifecycle status

A technique may advance only when the corresponding evidence exists:

| Status | Meaning |
|---|---|
| `AVAILABLE IN REGISTRY` | Card exists and validates; no adoption claim |
| `RESEARCHED` | Canonical capabilities and constraints were investigated |
| `APPROVED` | An authorized owner approved the defined use |
| `INSTALLED` | The pinned artifact is present in the target environment |
| `CONFIGURED` | Required configuration exists without claiming usability |
| `AVAILABLE IN SESSION` | The active host exposes the capability |
| `SMOKE TESTED` | A bounded representative invocation produced evidence |
| `INTEGRATED` | The capability is used in an approved workflow with regression evidence |
| `DEFERRED` | Not adopted now; revisit conditions are recorded |
| `REJECTED` | Evaluated and not adopted; reason is recorded |
| `BLOCKED` | Required permission, dependency or control is missing |

Do not skip from `RESEARCHED` or `INSTALLED` to `INTEGRATED`.

## Current resource claims

All 40 cards use `measurement_status: "not_measured"`. Qualitative token/runtime implications are planning notes, not measured usage. Provider token or cost fields remain `unknown` unless the provider exposes them.

## Supported checks

These commands are implemented read-only validators:

```bash
python .harness/scripts/validate_techniques.py
python -m unittest discover -s .harness/tests -p "test_technique_registry.py" -v
```

The registry has no command that automatically loads all 40 cards into an agent prompt. Use the [routing guide](06-technique-routing.md) to select a small task-relevant subset.

## Related documents

- [Technique routing, profiles and recipes](06-technique-routing.md)
- [Execution traces and checkpoints](07-execution-traces-and-checkpoints.md)
- [Tool installation, activation and verification](10-tool-installation-and-activation.md)
- [Ecomdy engineering technique mapping](../../docs/engineering-technique-mapping.md)
- [Minimum Viable DevHarness plan](../../docs/minimum-viable-harness-plan.md)
