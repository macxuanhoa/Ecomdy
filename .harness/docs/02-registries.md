# Agent, skill and tool registry

> Target design / v0.1 / 2026-11-26. Not verified as-built.

## Roles
| ID | Capability | Status |
|---|---|---|
| A01 | Master Orchestrator | Proposed |
| A02 | Product Manager | Proposed |
| A03 | Business Analyst | Proposed |
| A04 | Requirements Auditor | Proposed |
| A05 | Solution Architect | Proposed |
| A06 | Technical Planner | Proposed |
| A07 | Research Agent | Proposed |
| A08 | Repository Analyst | Proposed |
| A09 | Frontend Engineer | Proposed |
| A10 | Backend Engineer | Proposed |
| A11 | Database Engineer | Proposed |
| A12 | UI/UX Designer | Proposed |
| A13 | Integration Engineer | Proposed |
| A14 | Refactoring Engineer | Proposed |
| A15 | Debugging Engineer | Proposed |
| A16 | QA Engineer | Proposed |
| A17 | Independent Code Reviewer | Proposed |
| A18 | Security Engineer | Proposed |
| A19 | Performance Engineer | Proposed |
| A20 | Accessibility Auditor | Proposed |
| A21 | DevOps Engineer | Proposed |
| A22 | Documentation Engineer | Proposed |
| A23 | Context Curator | Proposed |
| A24 | Harness Engineer | Proposed |

## Proposed skill catalogue

The catalogue below is proposed; it is not automatically installed or loaded. Three physical instruction files exist under `.harness/skills/` (`scoped-task`, `debug`, `diagram`) and can be read manually. They are guidance documents, not executable skills or a role router. The user-level Diagram Design Plugin is external to this harness and is not required for a repository clone.

- **discovery**: project-discovery, requirements-extraction, rubric-analysis, document-analysis, evidence-validation, gap-analysis
- **management**: scope-management, wbs-generation, roadmap-planning, sprint-planning, dependency-management, risk-management, gantt-generation, change-management
- **architecture**: system-design, architecture-review, design-pattern-selection, clean-architecture, modular-monolith, microservices-design, api-contract-design, adr
- **code**: repository-mapping, ast-analysis, symbol-search, dependency-analysis, call-graph-analysis, change-impact-analysis, code-reuse-discovery, duplicate-detection, safe-refactoring
- **frontend**: component-design, responsive-layout, design-tokens, state-management, routing, form-validation, error-state-design, accessibility
- **backend**: rest-api, authentication, authorization, service-layer, request-validation, rate-limiting, pagination, idempotency, concurrency-control
- **database**: erd, normalization, schema-validation, migration-planning, query-optimization, transaction-management, offline-sync, conflict-resolution
- **mobile**: android, react-native, flutter, offline-first, device-permissions, emulator-testing
- **ux**: persona, journey-map, information-architecture, user-flow, wireframe, design-system-audit, usability-testing, figma-integration
- **testing**: unit-testing, integration-testing, e2e, contract-testing, smoke, regression, property-based, mutation, fuzz, visual-regression, coverage, flaky-test-detection
- **debugging**: bug-reproduction, root-cause-analysis, stack-trace-analysis, log-analysis, git-bisect, network-debugging
- **security**: threat-modeling, owasp, static-analysis, secret-detection, dependency-scan, least-privilege, prompt-injection-defense, mcp-security, sbom
- **devops**: environment-bootstrap, dockerization, ci, cd, infrastructure-as-code, rollback, release-management, health-check
- **agent**: context-engineering, prompt-compilation, context-compression, model-routing, skill-selection, ralph-loop, plan-and-execute, evaluator-optimizer, multi-agent-review, checkpoint-recovery, budget-management
- **documentation**: readme-generation, api-documentation, architecture-documentation, changelog, adr, knowledge-validation, documentation-reconciliation, session-handoff
- **academic**: coursework-brief-analysis, marking-rubric-mapping, requirement-traceability, implementation-evidence, demo-script, viva-preparation, submission-audit
- **diagrams**: c4-context, c4-container, c4-component, uml-class, uml-sequence, uml-activity, uml-state-machine, uml-use-case, erd, data-flow, workflow, sitemap, deployment, network-topology, dependency-graph, event-flow, ci-cd, gantt, threat-model, agent-orchestration

## Tool registry candidates
Codex CLI, Claude Code, Gemini CLI, OpenCode, Aider, Spec Kit or OpenSpec, ripgrep, Tree-sitter/LSP, SQLite FTS5, Git worktree, Playwright, pytest, Vitest, JUnit, Semgrep, Gitleaks, Trivy, Docker, GitHub Actions, OpenTelemetry, Graphviz, Mermaid. Pin versions and validate permissions before installation. No provider assumed installed.

## Engineering technique registry

The separate [technique library](05-technique-library.md) contains 40 stable technique cards across categories A–H with explicit kinds, lifecycle states, verification and security metadata. It is not the proposed skill catalogue above and does not claim that the missing 145-technique baseline was recovered. Use the [routing guide](06-technique-routing.md) for task-scoped selection.

## External candidate tool manifest

The [installation manifest](../registry/installation/tool-manifest.json) records 20 stable `TOOL-*` candidates with canonical sources, pinned versions, licenses, compatibility, permissions, credentials, telemetry/privacy, conflicts, reproducibility and lifecycle procedures. The [installation and activation guide](10-tool-installation-and-activation.md) explains required/optional/missing tools and approval boundaries. No proposed command is execution evidence; no external candidate is integrated. Diagram Design is installed only at user scope and is not inherited by clones or CI.
