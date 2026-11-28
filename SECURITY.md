# Security Policy

## Project state

This public repository currently contains project documentation and design assets. It does not contain a deployed Ecomdy application or an established security response SLA.

## Reporting a vulnerability

Do not post credentials, private data, or an unpatched vulnerability in a public issue. Use GitHub's private vulnerability reporting for this repository if it is enabled. If private reporting is unavailable, contact the repository owner through a private GitHub channel and include only the information needed to reproduce the issue.

Do not include real secrets or customer data in reports or test fixtures. Authenticated read-back on 2026-11-28 verified GitHub secret scanning/push protection, vulnerability alerts, Dependabot security updates and private vulnerability reporting as enabled; these features may not detect every secret format. The same read-back verified strict `validate` protection on `main`, PR-only and resolved-conversation requirements, admin enforcement, no force-pushes/deletions and no repository rulesets. See the [verification report](docs/setup/VERIFICATION_REPORT.md) for current evidence and limits.
