# Execution Traces and Checkpoints

**As of:** 2026-11-28 (Asia/Saigon)
**Status:** Task-contract validation, Git scope inspection, controlled verification, evidence capture and trace schema/validator implemented. Checkpoint generation, handoff and resume are not implemented.

## Purpose

An execution trace records what was selected, attempted, executed and verified without turning a plan into evidence. A checkpoint records where authorized work can resume and what prevents continuation.

## Sources of truth

| Artifact | Purpose |
|---|---|
| [`.harness/schemas/execution.schema.json`](../schemas/execution.schema.json) | JSON Schema Draft 2020-12 for trace and checkpoint documents |
| [`.harness/schemas/task-contract.schema.json`](../schemas/task-contract.schema.json) | Controlled verification task-contract contract |
| [`.harness/templates/task-contract.example.json`](../templates/task-contract.example.json) | Example contract; approvals are intentionally empty and verification is blocked until reviewed |
| [`.harness/templates/execution-trace.example.json`](../templates/execution-trace.example.json) | Example trace; explicitly not run evidence |
| [`.harness/templates/checkpoint.example.json`](../templates/checkpoint.example.json) | Example blocked checkpoint |
| [`.harness/scripts/task_contract.py`](../scripts/task_contract.py) | Fail-closed task, route, scope, command and budget validation |
| [`.harness/scripts/scope_checker.py`](../scripts/scope_checker.py) | Read-only Git state and changed-path scope inspection |
| [`.harness/scripts/verification_runner.py`](../scripts/verification_runner.py) | Allowlisted argv execution, bounded output, evidence capture and observed trace generation |
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

## Controlled task contract

A verification contract binds the task, route/profile/recipe, one verification technique, acceptance criteria, allowed paths, exact command argv, command criteria, timeouts, output caps, budgets, approval references and an evidence directory under `.harness/state/`.

Validation rejects unknown fields, malformed IDs, uncovered acceptance criteria, shell executables, inline Python code, unapproved Python modules, non-reviewed executables, paid-call budgets, retries, multiple iterations and secret scans without Gitleaks `--redact`. Built-in protected paths remain denied even when a contract supplies an empty additional deny list.

`verify` refuses to start when `approvals` is empty. Approval strings are recorded references, not proof that a human approved the exact content; reviewers must bind the recorded task-contract SHA-256 to their decision.

## Repository scope inspection

`scope` reads Git with structured argv and porcelain `-z` output. It records branch, HEAD, optional ancestor-checked base commit, staged paths, unstaged paths, untracked paths, rename/copy origin and destination, statuses and working-tree byte sizes.

A scope PASS means every observed changed path matches the allowlist, avoids protected/denied paths, stays within file/byte limits and contains no unsafe symlink or non-regular path. Gitignored paths are not reported as untracked by this status-based inspection. Missing Git state, invalid base commits, non-UTF-8 paths and malformed status records fail closed. The runner checks scope before execution and again afterward so a command cannot turn a PASS into an accepted out-of-scope side effect.

This is change detection, not prevention. An independent agent with terminal access can still edit files; only the controlled runner refuses to continue after detecting a violation.

## Verification and evidence

`verify` executes only the exact allowlisted argv entries after contract, approval and scope checks. Executables are limited to the current Python interpreter, pytest and Gitleaks; Python `-c` and unapproved `-m` modules are rejected. Absolute, parent-traversal and URL arguments are rejected. Python script/start-directory paths and Gitleaks source/config/baseline/ignore paths must resolve inside the project and explicit symlinks are rejected. Gitleaks report-file options are disallowed so redacted stdout remains the bounded evidence channel.

Each command records actual resolved argv, cwd, status, exit code, timestamps, bounded output excerpt, truncation flag, observed output bytes and evidence path. stdout and stderr are combined without a shell. A timeout terminates the direct child; an output-cap overflow terminates it and records FAIL. Later commands are blocked after the first non-PASS command.

Logs use heuristic redaction for common credential/private-key patterns, and Gitleaks scans require `--redact`. Redaction is best effort, not a confidentiality guarantee. Evidence includes pre/post scope reports, command logs, an observed trace, a verification record and a hash manifest. Token usage and cost remain null/unknown; local runtime is observed.

## Command records

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

Routing profile budgets remain advisory. A controlled verification contract enforces one iteration, zero retries/cost, total command-timeout bounds and per-command output caps; the trace schema still records budget enforcement as `advisory` because it does not provide token/spend controls or process-tree/network isolation.

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

Run scope inspection and controlled verification against a reviewed contract:

```bash
python .harness/harness.py scope --task PATH/TO/TASK.json --project .
python .harness/harness.py verify --task PATH/TO/TASK.json --project .
```

`scope` exits `0` for PASS, `3` for a scope block and `2` for input/inspection errors. `verify` exits `0` for PASS, `1` for FAIL, `3` for BLOCKED and `2` for input/output/internal errors. Add `--output PATH/TO/RESULT.json` to persist the JSON result.

The bundled task-contract example is intentionally blocked by empty approvals. Do not fabricate an approval to make the example pass; use a reviewed approval reference tied to the exact contract content in an authorized task.

## Runtime boundary

The current runner detects repository changes, refuses unsafe command input, executes a narrow allowlist, enforces command time/output limits, rechecks post-command scope and records evidence. It does not enforce OS/container filesystem permissions, isolate network access, guarantee termination of every descendant process, or prevent an independent agent from editing outside the contract. Redaction and path checks reduce risk but are not a sandbox.

Trace/checkpoint schemas still accept example and manually assembled documents; semantic validation cannot prove a command ran or that evidence is truthful. Checkpoint generation, handoff generation and resume execution remain unimplemented.
