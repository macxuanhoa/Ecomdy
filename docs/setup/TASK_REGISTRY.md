# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation and command/status claims match current files. |
| SET-03 | Local validation and security review | Verified (local scope) | Root and harness validators, JSON/YAML parse, source hashes, ignore rules, diff whitespace, harness unit tests, and independent review passed; Mermaid grammar is not parser-checked locally. Diagram rerender unavailable. |
| SET-04 | Commit setup changes | In Progress | Commits `087c27e` and `728871a` are pushed; the reviewed additional specifications/diagram coverage is ready for a scoped commit. Original inputs remain excluded. |
| SET-05 | Push / pull request | In Progress | Draft [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1) is open; prior commits passed both push and pull-request CI. Push and verify the latest local additions next. |
| SET-06 | Repository metadata, security, dependency checks, and main protection | Verified | Authenticated API read-back confirmed settings; monthly Dependabot Actions config is on the PR branch. |
| SET-07 | GitHub Project board | Blocked | Current credential lacks `read:project` required by Projects V2 GraphQL; no project created. Owner can authorize project scope through GitHub integration. |
| SET-08 | Bundle reusable DevHarness and validate its boundaries | In Progress | Harness bundle/tests, product specification docs, and new detailed diagram sources passed local validation and independent review. Current-branch CI remains pending. |
