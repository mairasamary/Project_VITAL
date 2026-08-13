#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
docker compose ps
echo
echo "Recent OpenEMR logs:"
docker compose logs --tail=30 openemr
