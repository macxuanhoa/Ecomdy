# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation and command/status claims match current files. |
| SET-03 | Local validation and security review | Verified (local scope) | Markdown/asset validation, JSON/YAML parse, source hashes, secret-pattern scan, and harness unit tests passed; diagram rerender unavailable. |
| SET-04 | Commit setup changes | In Progress | Stage review, then commit to this branch. |
| SET-05 | Push / pull request | Blocked pending access check | `gh` missing; GitHub write authorization has not been tested. |
| SET-06 | Harness packaging / broader specification | Proposed | Decide repository boundary after baseline setup; harness currently lives in sibling local folder. |
