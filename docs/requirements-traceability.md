# Requirements Traceability Matrix

All implementation references below are **planned**. This repository currently contains no Ecomdy application code.

| Requirement | Candidate capability / module | Verification evidence needed | Current state |
|---|---|---|---|
| REQ-01, REQ-05 | Source registry, compliant connectors, source policy | Approved allowlist; connector tests against permitted fixtures; terms review | Proposed |
| REQ-02, REQ-06 | Article/event store, claim/citation model, digest generator | Every digest item traces to source; sampled claim/source comparison | Proposed |
| REQ-03, REQ-06, REQ-07 | Content drafting and editorial workflow | Per-format drafts preserve citations; state-transition and approval-version tests | Proposed |
| REQ-04 | Published-content freshness audit | Controlled old/new source fixtures; findings reviewed by a person | Proposed |
| REQ-08 | Demo assembly | Running demo, generated digest, one-week content sample, recorded checks | Proposed |
| REQ-09 | Seller discovery | Dated, consent-aware records for at least five real seller interviews | Outstanding |
| REQ-10 | Content strategy and calendar | Prioritization rationale, calendar, acquisition proposal reviewed by owner | Outstanding |
| REQ-11 | Normalize, deduplicate, summarize | Duplicate/outdated fixtures; source-agreement sample; error report | Proposed |
| REQ-12 | Content templates and editorial UI | Usability session, review/edit/approve evidence, team feedback | Proposed |

## Evidence policy

Status moves to `Verified` only after concrete evidence is recorded (command, result, sample, and date). Proposed modules, diagrams, and tests on a roadmap do not count as implementation or acceptance evidence.
