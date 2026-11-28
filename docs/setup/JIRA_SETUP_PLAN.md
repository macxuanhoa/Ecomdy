# Jira-First Delivery Setup Plan

**State:** BLOCKED pending owner authorization. This is a setup plan, not evidence that a Jira project exists.
**Audit date:** 2026-11-27
**Repository:** `macxuanhoa/Ecomdy`

## 1. Availability and authority

Phase 0 found no Jira Cloud site URL, connector, CLI, credential or authorized integration. No tenant, project key, issue, sprint or automation result is assumed.

GitHub remains authoritative for source, branches, commits, pull requests, review, CI/CD and versioned documentation. Jira becomes authoritative for delivery planning, priority, assignment, dependencies, sprint state and acceptance tracking after the owner authorizes it. GitHub Projects V2 is not the primary board and no additional Projects permission is requested.

## 2. Preconditions

Do not create or configure Jira until the owner provides or approves:

1. The Jira Cloud site and an authorized access method; do not paste tokens into chat or Git.
2. Project key, display name, project lead and administrator.
3. Company-managed versus team-managed project type; the recommendation is company-managed Scrum for shared governance.
4. Reviewer/assignee groups and least-privilege permission model.
5. The GitHub repository authorized for integration.
6. Sprint cadence, capacity and acceptance authority.

Record the real values in this document only after verification. Until then, use `TBD` rather than plausible-looking placeholders.

## 3. Proposed project model

| Item | Proposed value | Approval state |
|---|---|---|
| Project type | Company-managed Scrum | Requires owner approval |
| Project key / name | `TBD` / Ecomdy Delivery | Requires owner approval |
| Project lead | `TBD` | Requires owner assignment |
| Board | Ecomdy Delivery board, filtered to the project | Requires owner approval |
| Issue types | Epic, Story, Task, Bug, Spike; Subtask only when useful | Requires owner approval |
| Components | Governance, Sources, Processing, Knowledge, Content, Editorial, Extensions, Evaluation, Harness | Proposed |
| Priority scheme | Use Jira's standard Highest/High/Medium/Low; do not create duplicate P0/P1/P2 fields unless needed for import | Proposed |
| Cadence | `TBD`; no dates or capacity commitments exist | Blocked |

### Epic structure

Create epics only after project approval. These are proposed workstreams, not existing Jira epics.

| Proposed epic | Scope | Capability / task mapping |
|---|---|---|
| Governance and Acceptance | Baseline approval, ownership, Jira/GitHub workflow, acceptance evidence | SET-10, PRGOV-01, COL-01, FND-05/06 |
| Source and Evidence Pipeline | Source policy, connector, normalization, dedup, claims, verification, knowledge contracts | M01–M06, M09–M12; ECO-01/02/05/06/07 |
| Intelligence and Digest | Market/trend evaluation and weekly digest | M07, M08, M13; ECO-08/12 |
| Content and Editorial | Content studio, SEO, freshness and approval workflow | M14–M17; ECO-08/09/10 |
| Validation and Extensions | Interviews, usability, analytics, assistant/notifications and post-MVP extensions | M18–M20; ECO-03/04/11/12 |
| Harness and Engineering Enablement | Diagram validation, context controls, bounded harness hardening | DGM-03/04, CTX-01/03/04, HAR-07/08/11/12/15 |

Product epics do not imply implementation. M01–M20 remain SPECIFICATION ONLY until their acceptance evidence changes.

## 4. Workflow and fields

### Proposed workflow

```text
Backlog -> Ready -> In Progress -> In Review -> Done
                 \-> Blocked -> return to previous active status
```

- `Ready` requires the repository Definition of Ready.
- `In Review` requires a linked PR, actual verification output and updated documentation/traceability.
- `Done` requires the repository Definition of Done and recorded acceptance evidence.
- `Blocked` requires a blocker ID, owner and resolution path.
- Merge, deployment and publication are separate human approvals; no workflow transition grants those permissions automatically.

### Required custom fields or description sections

Use native fields where possible and avoid unnecessary custom-field administration.

| Field | Purpose |
|---|---|
| Requirement IDs | Existing REQ IDs; do not replace them with Jira keys. |
| Capability IDs | M01–M20 or FND/HAR/DGM/CTX/COL IDs from the coverage matrix. |
| Objective / user outcome | Observable result and non-goals. |
| Allowed / forbidden paths | Scope boundary for code and documentation. |
| Dependencies | Linked blocking issues and external approvals. |
| Acceptance criteria | Normal, error, boundary and authorization cases. |
| Verification commands / evidence | Exact commands and real outputs; no planned result presented as actual. |
| Owner / reviewer | Named only after the owner assigns real people. |
| Budget / stop condition | Iteration, runtime, cost and token ceilings where measurable. |
| Source confidentiality | Public, local-only or approval-required input classification. |
| Approval / rollback | Required human approval and recovery path. |

## 5. Initial backlog mapping

The local planning IDs below are not Jira keys. Assign real keys only after the project is authorized and the items are imported/created through an approved method.

| Order | Local planning ID | Work item | Depends on | Exit evidence |
|---|---|---|---|---|
| 1 | SET-10 | Owner review of Phase 0 acceptance package and PR #1 | Owner availability | Recorded approval/rejection and next branch/PR decision. |
| 2 | PM-SETUP | Authorize and configure Jira project/board/integration | Owner Jira authorization | Verified project URL/key, permissions, board and GitHub link. |
| 3 | PRGOV-01 | Adopt branch/PR convention, assign reviewers and module owners | SET-10, owner assignments | Updated CONTRIBUTING/template/CODEOWNERS and protection read-back. |
| 4 | DIAG-01 | Pin and validate Mermaid parser/render toolchain | Owner tool selection, license/security review | Locked version, clean install record and 56-source syntax/render result. |
| 5 | HARD-01 | Enforce approved-task and budget configuration | SET-10, executable task contract | Tests proving disabled automation, stop conditions and config loading. |
| 6 | HARD-02 | Enforce allowed/forbidden paths and dependency checks | HARD-01 | Deterministic tests for scope violation and missing dependency. |
| 7 | HARD-03 | Persist checkpoints and generate structured handoff | HARD-01/02 | Resume test and handoff generated from verified state. |
| 8 | CTX-01 | Pilot scoped context pack on one approved task | HARD-02, telemetry method | Measured file/token/runtime baseline and provenance checks. |
| 9 | COL-02 | Define API/schema contract-change workflow | Module owners, ECO-05 | Compatibility checklist, contract fixture and rollback rule. |
| 10 | COL-03 | Add integration-test policy and fixtures | COL-02, selected vertical slice | CI-backed contract/integration evidence. |

ECO-01–ECO-12 remain in the product task register and should be linked to Jira after owner-approved scope and dependencies are ready. Do not bulk-create speculative issues before the project model is accepted.

The Phase 1 import representation is [JIRA_IMPORT_BACKLOG.csv](JIRA_IMPORT_BACKLOG.csv). It contains proposed epics/tasks, stable internal IDs, dependencies, role placeholders and acceptance criteria. The `Jira Key` column is intentionally empty; no issue has been created. Map the CSV to the approved Jira fields and import method only after project authorization.

## 6. Labels and automation

### Labels

- Requirement/capability: `req-<id>`, `m01`…`m20` where useful.
- Work type: `governance`, `harness`, `diagram`, `context`, `security`, `documentation`, `product`.
- State/risk: `blocked`, `owner-decision`, `local-only-source`, `human-approval`.
- Avoid labels that duplicate Jira status, priority or component fields.

### Proposed automation rules

1. When an issue enters `Blocked`, require a blocker link/description and notify only the assigned owner/reviewer.
2. When a linked PR opens, add a PR-link comment and move the issue to `In Review` only if the PR author requests it; do not auto-approve.
3. When CI fails, add a verification comment; do not silently return the issue to `In Progress` or close it.
4. When an issue is inactive for an owner-approved interval, flag it for review; do not auto-close.
5. When an issue becomes `Done`, require acceptance evidence and linked PR/commit; do not trigger merge, deployment or publication.
6. Never place credentials, local-only source text or generated secrets in Jira comments or automation payloads.

All rules require owner review of actors, conditions, actions, failure behavior and audit logs before activation.

## 7. GitHub integration

After authorization:

1. Install/configure the approved Jira Cloud–GitHub integration for `macxuanhoa/Ecomdy`.
2. Verify repository read access and issue/PR linking with one owner-approved real task.
3. Adopt branch names containing the real Jira key once available: `<type>/<jira-key>-<short-kebab>`.
4. Require the Jira issue link in the PR template; keep requirement IDs and capability IDs in the PR body.
5. Do not enable smart-commit actions that change status or assign work unless explicitly approved.
6. Keep GitHub as source/review/CI authority; do not mirror branch state into Jira with competing automation.

## 8. Permissions and security

- Project administrator: owner-designated person only.
- Developers: create/edit assigned work and link PRs; no project administration.
- Reviewers: comment, transition review states and verify evidence within assigned scope.
- Automation actor: least privilege; no repository write, merge, deploy, secret or permission-management rights.
- External contributors: no access by default.
- Store no PAT, API token, private source content or personal data in Jira or Git.

## 9. Acceptance checklist

Jira setup is complete only when all applicable items are evidenced:

- [ ] Owner authorization and real site/project identifiers recorded.
- [ ] Project type, workflow, board filter, components and issue types verified.
- [ ] Permission groups and automation actor reviewed.
- [ ] One approved real issue traverses the intended workflow with evidence.
- [ ] GitHub repository connection and PR/branch linking verified.
- [ ] No GitHub Projects permission expansion requested or required.
- [ ] Existing SET/ECO/REQ/capability IDs are linked, not replaced.
- [ ] `SET-07`, `BLOCKERS.md`, `DECISION_LOG.md` and `HANDOFF.md` updated with actual results.

Until this checklist is complete, PM-01 and PM-02 remain BLOCKED.
