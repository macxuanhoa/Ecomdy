# Execution Traces and Checkpoints

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Schema, examples and read-only validator implemented. Trace capture and checkpoint resume are not implemented.

## Purpose

An execution trace records what was selected, attempted, executed and verified without turning a plan into evidence. A checkpoint records where authorized work can resume and what prevents continuation.

## Sources of truth

| Artifact | Purpose |
|---|---|
| [`.harness/schemas/execution.schema.json`](../schemas/execution.schema.json) | JSON Schema Draft 2020-12 for trace and checkpoint documents |
| [`.harness/templates/execution-trace.example.json`](../templates/execution-trace.example.json) | Example trace; explicitly not run evidence |
| [`.harness/templates/checkpoint.example.json`](../templates/checkpoint.example.json) | Example blocked checkpoint |
| [`.harness/scripts/validate_execution.py`](../scripts/validate_execution.py) | Standard-library semantic validator |

## Step states

| State | Required meaning | Must not imply |
|---|---|---|
| `SELECTED` | Technique/step chosen by the route | Any work was attempted |
| `ATTEMPTED` | Work started but no completed result is claimed | Execution completed |
| `EXECUTED` | A result or command completed | Result was independently verified |
| `VERIFIED` | Evidence satisfies the stated verification requirement | Broader product correctness than the evidence supports |
| `SKIPPED` | Step intentionally omitted with a recorded reason | Step passed |
| `BLOCKED` | Required authority, input or dependency is missing | Step failed technically |
| `FAILED` | Attempt ran and did not meet its expected result | Retry may continue without a new bound |

Timestamp fields enforce these transitions. A `VERIFIED` step requires output or PASS-command evidence. A `COMPLETED` trace requires every step to be `VERIFIED` or `SKIPPED`, PASS results for all acceptance checks and no blockers.

## Commands and evidence

Commands are structured `argv` arrays with a working directory. They are not shell strings, and shell-wrapped forms such as `bash -c` are rejected. Each command records status, exit code, start/end timestamps, a bounded output excerpt, an explicit truncation flag, byte count and an optional evidence path.

A `PASS` command requires exit code 0. A `FAIL` command requires a non-zero exit code. `NOT_RUN`, `BLOCKED` and `TIMEOUT` have distinct semantics. Do not convert an unrun or blocked command into PASS.

Artifacts record path, SHA-256, byte size and kind. Approvals must identify the exact version/content they authorize. Editing approved content invalidates the approval.

## Resource accounting

Resource fields separate observed values from unknown values:

- `runtime_seconds`, `token_usage` and `cost_usd` are nullable;
- `measurement_status` is `unknown`, `partial` or `measured`;
- `unknown` cannot contain runtime, token or cost values;
- provider-reported usage is not estimated from prompt length;
- missing cost remains `null`/unknown even if runtime was measured.

Current profile and task budgets are advisory. The schema records limits and observations but does not enforce process termination, token caps or spend.

## Checkpoint states

| State | Meaning |
|---|---|
| `READY_TO_RESUME` | No blockers; pending steps and explicit resume conditions exist |
| `BLOCKED` | At least one unresolved blocker exists |
| `COMPLETE` | No pending steps or blockers; completed steps are recorded |

Completed and pending step IDs must be disjoint. A checkpoint does not authorize retrying external side effects. Resume must re-check input hashes, repository state, approvals and permission scope.

## Example usage

Validate the bundled examples:

```bash
python .harness/scripts/validate_execution.py
python -m unittest discover -s .harness/tests -p "test_execution_contract.py" -v
```

The examples deliberately include a fake command result to demonstrate state validation. Their limitations field states that no command ran. They must not be cited as execution evidence.

Validate a real proposed trace or checkpoint only after replacing all example values with observed state:

```bash
python .harness/scripts/validate_execution.py PATH/TO/DOCUMENT.json
```

## Runtime boundary

This validator reads JSON and checks invariants. It does not:

- execute commands;
- create traces automatically;
- terminate processes;
- enforce file scope or budgets;
- resume tasks;
- approve changes;
- prove that referenced evidence exists or is truthful.

A future executor must separately implement path resolution, allowlisted commands, timeouts, output caps, process isolation, evidence capture and human approval gates.
