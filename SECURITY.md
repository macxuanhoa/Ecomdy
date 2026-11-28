# Security Policy

## Project state

This public repository currently contains project documentation and design assets. It does not contain a deployed Ecomdy application or an established security response SLA.

## Reporting a vulnerability

Do not post credentials, private data, or an unpatched vulnerability in a public issue. Use GitHub's private vulnerability reporting for this repository if it is enabled. If private reporting is unavailable, contact the repository owner through a private GitHub channel and include only the information needed to reproduce the issue.

Do not include real secrets or customer data in reports or test fixtures. Historical authenticated setup read-back recorded GitHub secret scanning, push protection, vulnerability alerts, Dependabot security updates, and private vulnerability reporting as enabled. The later unauthenticated recheck returned HTTP 401, so their current state is **unverified**; these features may not detect every secret format. Obtain owner-authorized read-back before relying on them. See the [comprehensive audit](docs/setup/COMPREHENSIVE_AUDIT.md) and [verification report](docs/setup/VERIFICATION_REPORT.md) for current evidence and limits.
