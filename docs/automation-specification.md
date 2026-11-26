# Automation Specification

**State:** Target specification. The Ecomdy project profile sets `runtime_automation: false`; no product scheduler, worker, or automated content publication is implemented.

## Candidate jobs

| Job | Candidate trigger | Required inputs | Output / check |
|---|---|---|---|
| Source collection | Per-source interval or manual request | Approved source and terms profile | Fetch record, versions, error/health state. |
| Processing | New fetched version | Normalization/dedup/classification rules | Event, claim, evidence and review states. |
| Trend snapshots | Scheduled aggregation after source coverage is approved | Timestamped signal data and market taxonomy | Candidate trend snapshot with coverage caveats. Extension only. |
| Weekly digest | Weekly owner-configured schedule | Eligible event window, audience, citations | Draft digest and source/evidence links. |
| Freshness audit | Owner-configured schedule or manual run | Authorized published article set and current evidence | Findings for human review. |
| Source health | Per-source check after collection attempts | Connector status history | Health state and alert; no false “complete coverage” claim. |

The 30–60 minute interval in supporting notes is a proposal, not an approved schedule. Select schedules from source terms, rate limits, freshness need, operating budget, and measured lag.

## Execution controls

- `enabled` defaults false until source access, host, cost, retention, and owner are approved.
- Every job has a stable ID, idempotency key, timeout, retry cap, concurrency limit, and cancellation state.
- Retry only transient failures; use backoff and a circuit breaker for repeated failures.
- Persist checkpoints and status; never report success if a required downstream step failed.
- AI calls have explicit per-run token/cost/time budgets, schema validation, and failure escalation.
- No scheduled job can approve content, merge code, change permissions, delete source history, or deploy to production.
- All generated content remains draft-only until a person approves its exact version.

## Stop conditions and monitoring

Stop or pause on scope violation, source terms change, authentication failure, budget exhaustion, repeated connector error, unsupported high-impact claim, stale/ambiguous evidence, or required human approval. Record the observed error, retry count, last successful time, checkpoint, and recovery action. Alerts should not include secrets or unnecessary source text.
