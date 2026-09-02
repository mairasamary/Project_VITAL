#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="${PV_OPENEMR_URL:-https://localhost:8443}"
PATH_TO_CHECK="${PV_OPENEMR_PROTECTED_PATH:-/}"
python3 "$ROOT/unauthenticated_check.py" "${BASE%/}${PATH_TO_CHECK}"
