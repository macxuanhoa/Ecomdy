# Technique Library Implementation Roadmap

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Bounded proposal. Only the explicitly marked artifacts are implemented.

## Milestones

| ID | Outcome | Current state | Exit evidence |
|---|---|---|---|
| M1 | Inventory techniques and repository baseline | Implemented for the inspected baseline | 40-card registry; missing 145-technique baseline explicitly recorded |
| M2 | Technique cards and compatibility research | Partial | Cards validate; 20 external candidates have version/license/security research, but no candidate is approved or compatibility-proven in the target workflow |
| M3 | Installation and activation manifests | Manifest design implemented; no installation | Versioned schema, 20-candidate inventory, required/optional/missing baseline, lifecycle procedures, validator/tests and human guide exist; owner approval remains pending |
| M4 | Advisory router and recipe compiler | Partial | 9 profiles, 14 routes, 24 recipes and validator exist; no executable compiler |
| M5 | Runtime context, verification and file-scope controls | Not implemented | Bounded context loader; allowlisted runner; timeout/output caps; scope report; adversarial tests |
| M6 | Skill and tool integration | Not implemented | Per-tool approval, pinned installation, session availability, smoke test and workflow integration evidence |
| M7 | Checkpoints, traces and resource controls | Partial | Trace/checkpoint schema, examples, validator and tests exist; no automatic capture, process limits or resume |
| M8 | Advanced orchestration | Blocked | Independent-task analysis, bounded parallel loops, reconciliation and stop controls verified; AUTONOMOUS remains blocked |
| M9 | Benchmark and portability | Plan only | Same-task comparison across five arms; clean-environment reproduction; measured results with limitations |

## Dependency order

1. Complete M2 research and approve M3 security/compatibility scope.
2. Keep M4 advisory until M5 supplies enforceable path, command and resource boundaries.
3. Integrate individual skills/tools in M6 only after their own smoke tests.
4. Use M7 to record selected, attempted, executed and verified states.
5. Do not start M8 autonomous or multi-agent loops by default.
6. Run M9 before making effectiveness, cost or productivity claims.

## Per-milestone gates

Every implemented milestone must include:

- stable IDs and versioned schemas/registries;
- deterministic tests, including negative cases;
- security and permission review;
- exact working commands and observed output;
- documentation and navigation updates;
- rollback/uninstall/recovery procedure where applicable;
- handoff with blockers and limitations;
- independent review before integration.

No milestone may mark itself implemented from this roadmap alone.

## Verification snapshot

Local verification on 2026-11-28, branch `devharness/technique-library`:

| Check | Observed result |
|---|---|
| `python scripts/validate.py` | PASS |
| `python .harness/scripts/validate.py` | PASS |
| Technique registry validator | PASS: 40 techniques, categories A–H |
| Routing registry validator | PASS: 9 profiles, 14 routes, 24 recipes; advisory only |
| Execution contract validator | PASS: 2 templates; not run evidence |
| Tool manifest validator | PASS: 20 candidates; proposed commands `NOT_RUN` |
| Full harness unit suite | PASS: 50 tests |
| JSON Schema conformance | PASS: 4 schemas checked, 7 documents validated with local `jsonschema` 4.26.0 |
| Workflow YAML parse | PASS: 7 run steps |
| Python compile and `git diff --check` | PASS |
| `python .harness/harness.py doctor` | Python 3.11.9; Git present; Graphviz and GitHub CLI absent; advisory mode |

These are local results, not remote CI evidence. No external candidate was installed by this work, no proposed command was executed, no benchmark was run and no commit/push was performed.

## Explicit non-goals

- full Ecomdy product runtime;
- live crawling or paid model services;
- production deployment or automatic publication;
- unreviewed remote scripts;
- general model routing;
- unbounded autonomy;
- replacing Jira or GitHub protection with a second task/protection system.
