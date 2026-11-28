# Setup Plan

## Execution order

| ID | Work | Gate |
|---|---|---|
| SET-00 | Audit repository, tools, permissions, and source documents | Evidence recorded; originals remain local-only |
| SET-01 | Reconcile official requirements and target proposals | Every requirement has ID, source, priority, and state |
| SET-02 | Publish repository navigation, onboarding, and governance docs | Commands and status claims match files that exist |
| SET-03 | Review diagrams, scripts, CI, and security boundaries | Syntax / smoke checks recorded; no secrets staged |
| SET-04 | Stage and inspect diff; commit to working branch | No original documents or unreviewed sensitive files |
| SET-05 | Push branch and open PR if authenticated access permits | Remote branch/PR verified; otherwise report exact blocker |
| SET-06 | Configure repository metadata, security, dependency checks, and main protection | Read back settings and verify required CI context |
| SET-07 | Configure Jira-first delivery after owner authorization | Real Jira project/board/permissions and GitHub integration verified; no GitHub Projects permission expansion required |
| SET-08 | Package DevHarness and verify reuse boundary | Harness included under `.harness/`; tests, validators, ignore rules, and CI updated |
| SET-09 | Reconcile result and prepare next implementation task | Only verified work marked complete; PR and blockers linked |

The plan is limited to the evidence and access available. Product implementation, production deployment, external source collection, paid automation, and publishing are not enabled by this setup.
