# Deployment Strategy

**State:** Proposed gates only. No deployment platform, cloud account, infrastructure, environment, or runtime is present or approved.

## Candidate progression

1. **Local development:** deterministic fixtures, no external collection by default, fake credentials, isolated test database.
2. **Shared test environment:** only after source access, authentication, retention, backup, logs, and cost limits are reviewed; use non-sensitive or approved data.
3. **Demonstration environment:** run the functional demo with a bounded source set, record coverage/freshness, keep generated content in draft, and provide a human approval path.
4. **Production:** separate approval after security review, restore test, monitoring, on-call owner, cost budget, rollback plan, and user acceptance evidence.

## Infrastructure decisions still open

Hosting region and provider; container/VM strategy; database and backup service; object storage; worker/scheduler runtime; identity provider; secrets service; network egress policy; observability; retention; deployment cadence; and operating budget. Do not choose a provider from the candidate stack without comparing constraints and current pricing.

## Release and recovery gates

- Build and test artifacts are traceable to a commit and environment configuration.
- Migrations are reviewed, reversible where practical, and tested against a backup/restore path.
- Secrets are supplied through an approved secret manager and are never committed or included in prompts/logs.
- Rollback and incident contacts are known before a production release.
- Deployment automation stays manual or approval-gated until operational controls are tested.
- No production deployment or automatic publishing is authorized by the current repository setup.
