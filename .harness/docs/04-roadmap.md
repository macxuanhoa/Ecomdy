# Master development roadmap

> Target design / v0.1 / 2026-11-26. Not verified as-built.

| Phase | Output | Acceptance |
|---|---|---|
| V0.1 | Bootstrap, configuration, source inventory | repeatable non-clobbering initialization; existing files preserved, missing ignore rules appended; tests |
| V0.2 | Extraction, indexes and context compiler | grounded source pointers; retrieval benchmark |
| V0.3 | Requirements, DAG, task contracts, approval | reject invalid or unapproved plans |
| V0.4 | Agent adapter, scoped execution, gates | deny out-of-scope changes; verify actual tests |
| V0.5 | Loop, checkpoint, scheduler | stop on budget, resume without duplicate work |
| V0.6 | Skills, MCP, model routing | adapter capability and permission tests |
| V0.7 | Architecture engine, dashboard | semantic validation, UI accessibility |
| V1.0 | Packaging, benchmark, upgrade | clean-machine install, recovery and security audit |

Each phase requires owner approval and detailed task contracts. Do not confuse roadmap with implemented capabilities.

## Technique-library milestones

The separate [M1–M9 technique roadmap](08-technique-implementation-roadmap.md) tracks inventory, cards/compatibility, installation manifests, advisory routing, runtime controls, integration, traces/resources, orchestration and benchmarking. The [tool installation guide](10-tool-installation-and-activation.md) records the current research-only activation boundary. It does not replace the phase roadmap above or authorize product implementation.
