# Definition of Ready and Done

## Definition of Ready

A feature/task can start when:

- It references approved requirement IDs and has an observable user outcome.
- Scope, allowed paths, dependencies, constraints, assumptions, risks, and non-goals are explicit.
- Relevant source documents and repository areas are identified; originals remain local-only unless publication is approved.
- Acceptance criteria describe normal, error, boundary, and authorization behavior where relevant.
- Source access, brand, data, identity, and cost dependencies are resolved or the task is explicitly limited to a safe stub/specification.
- Verification commands or evidence collection are specified and available.
- Human approval requirements and a safe stop/rollback path are defined.

## Definition of Done

A task is `Verified` only when applicable checks have been run and evidence is recorded:

- The change satisfies approved acceptance criteria and stays within allowed paths.
- Tests/checks pass with exact commands and exit codes; skipped checks are explained.
- Security, privacy, source terms, citations, temporal data, and access-control impacts are reviewed.
- UI changes are reviewed at supported sizes and accessible interactions are checked.
- Requirements traceability, diagrams, API/schema docs, and user/developer guidance are reconciled.
- Independent review findings are resolved or tracked; no blocker is silently waived.
- Git diff, staged file list, secrets, and original-source exclusions are reviewed.
- Current branch has an evidence-backed commit; CI status is verified where configured.
- Product deployment and content publication remain separate, human-approved steps.

## Status rules

`Implemented` means code/config exists. `Verified` means a named check or evidence artifact supports its acceptance criteria. `Completed` means all required verification and approval gates are satisfied. A proposal, generated file, or successful documentation check alone does not mark product behavior implemented or verified.
