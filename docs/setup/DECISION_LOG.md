# Decision Log

| ID | Decision | Basis | State |
|---|---|---|---|
| DEC-001 | Preserve `origin/main` and work on `setup/phase-0-audit`. | Remote `main` already contains commit `560cf0d`; local starter is not based on it. | Applied |
| DEC-002 | Keep original PDFs, workbook, and image out of Git. | Source README directs local-only storage; Git ignore is configured; GitHub repository is public. | Applied |
| DEC-003 | Treat the challenge workbook as the source for mandatory requirements; treat blueprint and image extensions as proposals unless the challenge brief confirms them. | Direct reading of the supplied workbook, PDFs, and image. | Applied |
| DEC-004 | Do not characterize Ecomdy as an implemented product. | The local repository contains documentation and diagrams, no application source/runtime. | Applied |
| DEC-005 | Keep DevHarness OS independent from Ecomdy runtime logic. | Existing Ecomdy instructions and source blueprint define separate responsibilities. | Applied |
| DEC-006 | Protect `main` with PRs, the passing GitHub Actions `validate` check, resolved conversations, no force-push/deletion, and enforced admin rules; require zero approvals until a reviewer group is confirmed. | Verified check-run context and currently unknown contributor/reviewer capacity. | Applied |
| DEC-007 | Enable GitHub secret scanning, push protection, vulnerability alerts, Dependabot security updates, and private vulnerability reporting. | Public repository; owner permissions verified; official GitHub docs describe security features available for public repositories. | Applied |
| DEC-008 | Configure monthly Dependabot version updates for GitHub Actions only. | Current repo has no Ecomdy package manifest; version updates must remain reviewable and limited. | In PR; activates after merge |
| DEC-009 | Bundle the reusable DevHarness starter under `.harness/` in the Ecomdy repository while keeping it isolated from Ecomdy business logic and runtime. | User-supplied repository structure explicitly includes `.harness/`; no separate harness remote was supplied. The packaged CLI remains a bounded advisory starter. | Verified on setup branch; package commit `a08bb16` passed both CI events |
| DEC-010 | Make Jira the primary delivery tracker; retain GitHub for source, branches, commits, PRs, review, CI/CD and versioned documentation. | Phase 0 directive; Jira access is currently unavailable, so setup is blocked rather than fabricated. GitHub Projects permissions are not requested. | Approved direction; implementation blocked on owner authorization |
| DEC-011 | Accept the repository only conditionally as a documentation/setup baseline and advisory harness. | Deterministic checks verify docs/CI/CLI scope; M01–M20 and autonomous harness capabilities are not implemented. | Recorded in `PHASE_0_ACCEPTANCE.md`; owner review pending |
| DEC-012 | Prepare acceptance changes on `docs/phase-0-acceptance` without commit/push/merge. | Preserve PR #1 head and avoid overlapping PRs or unauthorized shared-state changes. | Applied locally |
| DEC-013 | Do not install diagram tools or regenerate valid artifacts in Phase 0. | Read-only acceptance scope; Mermaid CLI metadata is compatible but tool selection, license/security review and pinning are not approved. | Applied; DIAG-01 proposed |
| DEC-014 | Treat current branch-protection/security settings as implemented but unverified. | Phase 0 API revalidation returned HTTP 401; historical setup read-back is not current acceptance evidence. | Open until owner-authenticated read-back |
