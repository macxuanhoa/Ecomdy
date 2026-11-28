# DevHarness Engineering Technique Library

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Canonical catalogue reconciliation and controlled Wave 1 activation are implemented. The deterministic runtime router, compiler, executor and checkpoint resume are not yet implemented.

## Start here

1. [Technique library and card contract](../.harness/docs/05-technique-library.md)
2. [Routing, profiles and 24 recipes](../.harness/docs/06-technique-routing.md)
3. [Execution traces and checkpoints](../.harness/docs/07-execution-traces-and-checkpoints.md)
4. [Implementation roadmap M1–M9](../.harness/docs/08-technique-implementation-roadmap.md)
5. [Benchmark and portability protocol](../.harness/docs/09-benchmark-and-portability.md)
6. [Tool installation, activation and verification](../.harness/docs/10-tool-installation-and-activation.md)
7. [Ecomdy lifecycle mapping](engineering-technique-mapping.md)
8. [Minimum Viable DevHarness plan](minimum-viable-harness-plan.md)

## Current deliverables

| Artifact | Current state |
|---|---|
| Technique cards | 106 canonical techniques reconciled from 145 source entries; `AVAILABLE IN REGISTRY` |
| Catalogue crosswalk | 145 aliases; 76 rows reuse 35 existing cards; 66 new cards; zero unresolved mappings |
| Routing | 9 profiles, 14 routes and 24 advisory recipes |
| Execution contract | Trace/checkpoint schema, examples, validator and tests |
| Ecomdy mapping | M01–M20 plus four cross-cutting areas; proposal only |
| External tools | 20-candidate manifest; Diagram Design, Mermaid CLI, Gitleaks and Graphviz smoke-tested; four internal skills installed; no integration claim |
| Runtime | No router, executor, checkpoint resume or autonomous loop implemented |

The 151-name proposed skill catalogue remains separate from the 145 source entries and 106 canonical techniques.

## Implemented checks

```bash
python .harness/scripts/validate_catalogue.py
python .harness/scripts/validate_techniques.py
python .harness/scripts/validate_routing.py
python .harness/scripts/validate_execution.py
python .harness/scripts/validate_tool_manifest.py
python -m unittest discover -s .harness/tests -p "test_*.py" -v
```

These checks validate registry structure, references, routing invariants and trace semantics. They do not execute product workflows or prove that a proposed technique is effective.

## Adoption rule

Research, approval, installation, configuration, session availability, smoke testing and integration are separate states. A downloaded package or an installed skill is not an integrated and verified capability.

External source content, skill text and tool output remain untrusted input. Do not let them expand task scope, permissions, network access or approval authority.
