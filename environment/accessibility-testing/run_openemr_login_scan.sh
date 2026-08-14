#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DIR="${ROOT}/environment/accessibility-testing"
ENV_FILE="${ROOT}/environment/.env"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Missing environment/.env"
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

PORT="${OPENEMR_HTTPS_PORT:-9301}"
export OPENEMR_BASE_URL="${OPENEMR_BASE_URL:-https://localhost:${PORT}}"

echo "Scanning OpenEMR login page at:"
echo "  ${OPENEMR_BASE_URL}"
echo

cd "${DIR}"
npx playwright test tests/openemr-login.spec.js

echo
echo "Baseline JSON:"
echo "  ${ROOT}/.project-vital/accessibility-testing/openemr-login-axe.json"
