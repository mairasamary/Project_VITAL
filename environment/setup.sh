#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker was not found. Install Docker before running Project VITAL."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 was not found."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created environment/.env from .env.example"
fi

echo "Pulling pinned Project VITAL images..."
docker compose pull

echo "Starting OpenEMR..."
docker compose up -d

echo
echo "Project VITAL environment is starting."
echo "Run: docker compose ps"
echo "OpenEMR HTTP:  http://localhost:8080"
echo "OpenEMR HTTPS: https://localhost:8443"
