# Task Registry

| ID | Task | Status | Evidence / next action |
|---|---|---|---|
| SET-00 | Environment and input audit | Verified | `00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md`; originals are ignored. |
| SET-01 | Requirements traceability | Verified | Requirement IDs, sources, priorities, states, dependencies, and verification evidence are documented. |
| SET-02 | README and documentation portal | Verified | Navigation and command/status claims match current files. |
| SET-03 | Local validation and security review | Verified (local scope) | Root and harness validators, JSON/YAML parse, source hashes, ignore rules, diff whitespace, and harness unit tests passed; diagram rerender unavailable. Current PR CI pending. |
| SET-04 | Commit setup changes | In Progress | Baseline committed on `setup/phase-0-audit`; staged package/docs pass local checks. Create the second scoped commit after final review. |
| SET-05 | Push / pull request | In Progress | Draft [PR #1](https://github.com/macxuanhoa/Ecomdy/pull/1) is open and baseline CI passed. Push the second commit and verify its check run. |
| SET-06 | Repository metadata, security, dependency checks, and main protection | Verified | Authenticated API read-back confirmed settings; monthly Dependabot Actions config is on the PR branch. |
| SET-07 | GitHub Project board | Blocked | Current credential lacks `read:project` required by Projects V2 GraphQL; no project created. Owner can authorize project scope through GitHub integration. |
| SET-08 | Bundle reusable DevHarness and validate its boundaries | In Progress | `.harness/` copied from the supplied sibling starter; 3 unit tests and both validators pass. Independent review found and resolved two doc issues; remote check remains pending. |
