# DockerScan

A lightweight Flask + Trivy web dashboard to scan Docker images for vulnerabilities.

## Features
- Scan local or remote images with Trivy
- Show vulnerability severities and top issues
- JSON report export
- Multi-architecture (x86 / ARM64)
- Auto-built & updated via GitHub Actions

---

## Run via Docker Compose

```bash
docker compose up -d
