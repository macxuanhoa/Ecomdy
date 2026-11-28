# Workflow and execution specification

> Target design / v0.1 / 2026-11-26. Not verified as-built.

## Workflow routing
New project: discovery → specification → architecture → plan → approval → execution. Existing project: scan → baseline → gap analysis → plan. Bug: reproduce → isolate root cause → minimal fix → regression. Feature: requirement → impact/reuse → design → implementation → tests. Refactor: characterization tests → scoped change → regression. Security: assess → patch → rescan. Release: build → review → package → human-approved deployment.

## Bounded loops
Ralph-style task iteration; Plan–Execute–Verify; ReAct; Red–Green–Refactor; Evaluator–Optimizer; Critic–Revision; hypothesis–experiment; PDCA; OODA. Every loop has iteration/runtime/cost caps, progress checks, scoped permissions, retries and a BLOCKED exit. Consensus does not prove correctness. Separate agent review from implementation. Do not edit tests to manufacture passing results.

## Context, plan and evidence
Core rules → project summary → task context → relevant documents/symbols → originals. Prefer exact search/AST/SQL before embeddings; incremental indexing, prompt caching where supported, model routing, output budget, scoped retrieval and no secrets. Store provenance, conflicts, ADR, state and rejected proposals. Distinguish as-required, as-designed, as-planned, as-built, as-tested and as-deployed. Preserve baseline commit and actual test evidence.

## Automation
OS scheduler or CI may invoke approved tasks only after execution adapter exists. No automatic merge/deploy, no destructive action. Lock concurrent resources. Record exit codes, checkpoints and structured logs; classify errors, backoff and circuit-break.

## Quality and improvement
Scope, build, lint, type, unit/integration/regression, security and review gates as applicable. Propose improvement separately; benchmark before adoption. Metrics: verified task rate, regression rate, tokens/cost per verified task, latency and human interventions.

## Advisory technique routing

Use the [technique routing guide](06-technique-routing.md) to select a route, profile and recipe without activating the whole library. Record selected, attempted, executed and verified states using the [trace/checkpoint contract](07-execution-traces-and-checkpoints.md). The [M1–M9 roadmap](08-technique-implementation-roadmap.md) keeps runtime enforcement and autonomous orchestration separate from the current advisory design.
