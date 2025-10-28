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
```
docker-compose.yml file:
```yml
version: "3.9"
services:
  dockerscan:
    image: ghcr.io/ebarazi/dockerscan:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - "8888:8888"
    restart: unless-stopped  
```
