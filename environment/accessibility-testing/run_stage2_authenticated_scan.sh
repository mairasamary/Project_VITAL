#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ENV_FILE="${ROOT}/environment/.env"
IMAGE="mcr.microsoft.com/playwright:v1.62.0-noble"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Missing environment/.env"
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running."
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

PORT="${OPENEMR_HTTPS_PORT:-8443}"
export OPENEMR_BASE_URL="https://host.docker.internal:${PORT}"

if [ -z "${OPENEMR_ADMIN_USER:-}" ] || [ -z "${OPENEMR_ADMIN_PASSWORD:-}" ]; then
  echo "Missing OPENEMR_ADMIN_USER or OPENEMR_ADMIN_PASSWORD in environment/.env"
  exit 1
fi

echo "Authenticated accessibility baseline"
echo "OpenEMR: ${OPENEMR_BASE_URL}"
echo "Credentials: loaded from environment/.env (not printed)"
echo

docker run --rm --ipc=host \
  -e OPENEMR_BASE_URL="${OPENEMR_BASE_URL}" \
  -e OPENEMR_ADMIN_USER="${OPENEMR_ADMIN_USER}" \
  -e OPENEMR_ADMIN_PASSWORD="${OPENEMR_ADMIN_PASSWORD}" \
  -e ACCESSIBILITY_PATIENT_FINDER_PATH="${ACCESSIBILITY_PATIENT_FINDER_PATH:-}" \
  -v "${ROOT}:/work" \
  -w /work/environment/accessibility-testing \
  "${IMAGE}" \
  /bin/bash -lc "npm install >/dev/null && npx playwright test tests/openemr-authenticated.spec.js"

echo
echo "Reports written under:"
echo "  ${ROOT}/.project-vital/accessibility-testing/authenticated/"
