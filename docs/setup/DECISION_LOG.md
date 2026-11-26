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
