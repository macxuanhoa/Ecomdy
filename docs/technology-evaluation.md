# Technology and Harness Evaluation

**As of:** 2026-11-26. **Decision:** no new framework or product stack selected. This repository has no application code, and team skills, deployment environment, source permissions, timeline, and budget are unknown.

## Selection criteria

1. Fit the approved requirements and team workflow.
2. Preserve requirement/evidence provenance and support reviewable, recoverable changes.
3. Keep permissions, dependencies, and operational burden as small as practical.
4. Provide testable behavior with an exit path; avoid overlap between tools.
5. Compare task-level quality, maintainability, latency, cost, and security before adoption.

## Development process and harness options

| Option | Verified capability from primary documentation | Trade-off / unresolved question | Current decision |
|---|---|---|---|
| Repository-native Markdown, Git branches, CI, task/requirement registers | Already present and runnable in this repository; no new runtime dependency needed for documentation work. | Manual linking/traceability and no automatic task-state enforcement. | Use for setup baseline and keep records portable. |
| GitHub Spec Kit | Official docs describe specification-driven workflows through specify, plan, task, implementation, and convergence activities. Its docs also note teams must decide how specs change as requirements evolve. | Adds conventions/tooling; fit with the current standalone harness and agents must be tested; generated artifacts still need owner review. | Candidate for a bounded brownfield pilot, not installed. [Official docs](https://github.github.com/spec-kit/) |
| OpenSpec | Official project describes spec-driven development for AI coding assistants and change-oriented specification artifacts. | Requires comparing its change lifecycle and CLI/runtime dependencies with repository-native docs and Spec Kit. No Ecomdy pilot exists. | Candidate, not installed. [Official repository](https://github.com/Fission-AI/OpenSpec) |
| DevHarness OS starter | Bundled in `.harness/`; Python CLI preserves existing files, inventories/hashes local documents, protects generated outputs from unapproved overwrite, provides prompts and local validation. Three unit tests pass locally, in fresh clones and in CI. | It does not extract documents, call models, run implementation tasks, enforce permissions/budgets, checkpoint/resume, or schedule work. No independent harness release or remote is established. | Bundle as an advisory, reusable component; do not describe it as a full orchestrator. See [Phase 0 acceptance](setup/PHASE_0_ACCEPTANCE.md). |
| Custom bounded workflow | Existing simple scripts and GitHub Actions can cover today's documentation checks. | Building a durable agent state machine, approval UI, or scheduler now would be unvalidated new work. | Keep custom implementation limited to demonstrated gaps. |

Spec Kit and OpenSpec should not be installed together by default. If either is trialed, define the same feature task, compare artifacts, setup friction, agent compatibility, and requirement drift, then decide from observed results.

## Agent execution / durability options

| Option | Primary documentation evidence | Trade-off / decision |
|---|---|---|
| Explicit application state machine and database records | Can make Ecomdy workflow states and audit history visible in product data. No implementation exists. | Lower initial framework dependency, but checkpoint/retry semantics need implementation and tests. Candidate for simple product/editorial flows. |
| LangGraph checkpointers | Official LangGraph docs describe saving graph state at steps to support persistence, human-in-the-loop, and fault-tolerant execution. [Checkpointer docs](https://docs.langchain.com/oss/python/langgraph/persistence) | Adds framework and persistence integrations; not justified until the workflow requires graph branching, pause/resume, or replay beyond a simple state machine. Must review dependency security and state privacy. |

No benchmark shows that a framework or model improves Ecomdy accuracy, Vietnamese quality, latency, cost, or recovery. These must be evaluated on representative, permissioned fixtures before adoption.

## Product stack evaluation status

The blueprint lists React/Next.js, Python/FastAPI, PostgreSQL, workers, and optional vector search as candidates. There is no codebase to preserve or team/deployment profile to compare against. Record these as candidates only; defer stack decision until constraints are known. A later ADR should compare at least one viable alternative per layer and include version, support lifecycle, security update process, deployment fit, skills, and total operating cost.

## Research scope and sources

Reviewed official documentation for [GitHub Spec Kit](https://github.github.com/spec-kit/), [Spec Kit's SDD guide](https://github.com/github/spec-kit/blob/main/docs/how-to/sdd.md), [OpenSpec](https://github.com/Fission-AI/OpenSpec), and [LangGraph persistence/checkpointers](https://docs.langchain.com/oss/python/langgraph/persistence). This is a capability review, not an effectiveness benchmark or recommendation to install.
