# Contribution protocol

Work from an approved task contract. Jira is the primary delivery tracker after owner-authorized access is available; GitHub remains authoritative for source, branches, commits, pull requests, review, CI/CD and versioned documentation. Until Jira is available, use the existing SET/ECO/REQ IDs and do not invent Jira keys.

Create one short-lived topic branch from current `main` using `<type>/<jira-key>-<short-kebab>` when a real Jira key exists; otherwise use `<type>/<short-kebab>`. Do not create empty branches, force-push or change `main` directly. `main` is the only approved permanent branch; release/environment branches are not established. PR #1 requires Project Owner approval and independent human review before merge. PR #2 is intentionally stacked on PR #1's branch and must be retargeted or rebased only after PR #1 integrates. Follow [team development readiness](docs/team-development-readiness.md) for ownership, contract, migration and integration rules.

Before editing, record requirement/capability IDs, allowed/forbidden paths, dependencies, acceptance criteria, verification commands, budget and stop conditions. Prefer minimal reuse-aware diffs. API/schema changes require a reviewed contract, compatibility tests and rollback before parallel work. Run existing deterministic checks first and record exact results, including skipped checks.

The PR must link its Jira issue when available, list changed paths and risks, update traceability/docs/diagrams and include a handoff checkpoint. Review independently. Require explicit approval for scope expansion, dependency changes, paid services, production deployment, destructive migrations, credentials and publication. Keep local-only originals and secrets out of Git and Jira.

Repository protection/security settings are configured from the setup record but must be re-read with owner authorization before claiming current state. See [Phase 0 acceptance](docs/setup/PHASE_0_ACCEPTANCE.md) and [blockers](docs/setup/BLOCKERS.md).
