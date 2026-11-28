# DevHarness Engineering Technique Library

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Initial advisory registry and deterministic routing design. No external candidate is approved, installed or integrated by this document.

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
| Technique cards | 40 initial techniques across categories A–H; `AVAILABLE IN REGISTRY` |
| Missing 145-technique baseline | Explicitly recorded as unavailable; not fabricated |
| Routing | 9 profiles, 14 routes and 24 advisory recipes |
| Execution contract | Trace/checkpoint schema, examples, validator and tests |
| Ecomdy mapping | M01–M20 plus four cross-cutting areas; proposal only |
| External tools | 20-candidate installation/activation manifest; research-only except user-scope Diagram Design |
| Runtime | No router, executor, checkpoint resume or autonomous loop implemented |

The existing 151-name proposed skill catalogue remains separate. It is not the missing 145-technique baseline.

## Implemented checks

```bash
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
