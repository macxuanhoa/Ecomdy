# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation and command/status claims match current files. |
| SET-03 | Local validation and security review | Verified (local scope) | Root and harness validators, JSON/YAML parse, source hashes, ignore rules, diff whitespace, harness unit tests, and independent review passed; Mermaid grammar is not parser-checked locally. Diagram rerender unavailable. |
| SET-04 | Commit setup changes | Verified | Commit `a08bb16` containing the reviewed specifications and diagram coverage is pushed; the remote branch matches. Original inputs remain excluded. |
| SET-05 | Push / pull request | Verified (draft PR open) | [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1) points to `a08bb16`; push and pull-request CI passed. Owner review/merge remains pending. |
| SET-06 | Repository metadata, security, dependency checks, and main protection | Verified | Authenticated API read-back confirmed settings; monthly Dependabot Actions config is on the PR branch. |
| SET-07 | GitHub Project board | Blocked | Current credential lacks `read:project` required by Projects V2 GraphQL; no project created. Owner can authorize project scope through GitHub integration. |
| SET-08 | Bundle reusable DevHarness and validate its boundaries | Verified (starter scope) | Harness bundle/tests, product specification docs, and new detailed diagram sources passed local validation and independent review; push and pull-request CI passed. |
| SET-09 | Reconcile status and handoff | Verified | Execution status, task registry, verification report, environment audit, and handoff point to the pushed setup package commit and its CI evidence. |
