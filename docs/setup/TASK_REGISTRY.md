# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation and command/status claims match current files. |
| SET-03 | Local validation and security review | Verified (local scope) | Root and harness validators, JSON/YAML parse, source hashes, ignore rules, diff whitespace, and harness unit tests passed; setup commit CI passed. Diagram rerender unavailable. |
| SET-04 | Commit setup changes | Verified | Commit `087c27e` adds the reviewed harness/docs package; no original source files were included. |
| SET-05 | Push / pull request | Verified | Draft [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1) is open; setup commit `087c27e` was pushed and both push and pull-request CI runs passed. |
| SET-06 | Repository metadata, security, dependency checks, and main protection | Verified | Authenticated API read-back confirmed settings; monthly Dependabot Actions config is on the PR branch. |
| SET-07 | GitHub Project board | Blocked | Current credential lacks `read:project` required by Projects V2 GraphQL; no project created. Owner can authorize project scope through GitHub integration. |
| SET-08 | Bundle reusable DevHarness and validate its boundaries | Verified | `.harness/` copied from the supplied sibling starter; 3 unit tests, both validators, independent review, and both current-commit CI runs passed. |
