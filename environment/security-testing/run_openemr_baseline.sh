#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
URL="${PV_OPENEMR_URL:-https://localhost:8443/}"
OUT=".project-vital/security-testing/openemr-security-baseline.json"
mkdir -p "$(dirname "$OUT")"
python3 "$ROOT/security_baseline.py" "$URL" --output "$OUT"
echo "Baseline written to: $OUT"
