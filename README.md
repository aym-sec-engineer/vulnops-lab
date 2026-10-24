# VulnOps Lab

**DevSecOps | Python | Vulnerability Management | GitHub Actions**

A reproducible DevSecOps laboratory focused on vulnerability detection, risk prioritization, automated testing, and remediation simulation.

## Context

This project was inspired by the critical PHP vulnerabilities CVE-2026-109618 and CVE-2026-109619, disclosed in October 2026.

The objective is to demonstrate how security teams can transform a vulnerability advisory into actionable, auditable results.

**Disclaimer:** This is a fictional laboratory. No real DGFiP systems were scanned, audited or modified.

## Architecture

```text
Application inventory (JSON)
          |
          v
PHP version classification
          |
          v
Business risk prioritization
          |
          v
Security reporting (JSON / Markdown)
          |
          v
Remediation simulation
          |
          v
Post-remediation verification

GitHub Actions:
Ruff -> Pytest -> Reports -> Artifacts
```

## Features

- PHP upstream version classification
- Context-based risk prioritization
- Detection of unsupported branches
- Review-required classification for unknown branches
- Automated tests using Pytest
- Static code quality checks using Ruff
- JSON and Markdown security reports
- Reproducible remediation simulation
- GitHub Actions continuous integration

## Quick start

Python 3.12 recommended.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest tests/ -v
python -m src.report
python -m src.simulate_remediation
python -m src.report --inventory data/inventory-remediated.json --output-dir reports/after
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

## Example results

Initial fictional inventory:

- 5 applications analyzed
- 2 potentially vulnerable upstream versions
- 1 unsupported PHP branch
- 2 upstream patched versions

After simulated remediation:

- 5 applications with versions meeting upstream correction thresholds
- 0 actual production deployments performed

## Security limitations

This tool is a proof of concept, not a production vulnerability scanner.

- It uses fictional, manually supplied inventory data.
- It does not verify installed distribution packages.
- Vendor backported fixes require manual verification.
- CVE exposure is not confirmed through exploitation.
- Risk scoring is illustrative and is not CVSS.
- No live remediation, SOAR integration or production deployment is performed.
- More input validation and security tests would be required for production use.

## Further improvements

- Vendor-aware security advisory verification
- SBOM and dependency inventory ingestion
- Real asset discovery through authorized integrations
- Ticket creation and SOAR playbook integration
- Human approval gates for remediation
- Patch validation and rollback evidence

## References

- CERT-FR: https://cert.cyber.gouv.fr/alerte/CERTFR-2026-ALE-014
- PHP: https://www.php.net/
- GitHub Actions: https://docs.github.com/en/actions

## Author

aym-sec-engineer

Personal DevSecOps learning and demonstration project.