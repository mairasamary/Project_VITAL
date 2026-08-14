#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ENV_DIR="${ROOT}/environment"
OUT="${ROOT}/.project-vital/data-testing/schema"
mkdir -p "${OUT}"

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running."
  exit 1
fi

cd "${ENV_DIR}"

if ! docker compose ps --status running | grep -q vital-openemr-db; then
  echo "Project VITAL database container is not running."
  echo "Run: cd environment && docker compose up -d"
  exit 1
fi

# Read root password from environment/.env without printing it.
if [ ! -f .env ]; then
  echo "environment/.env not found."
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

DB_NAME="openemr"

query_to_file () {
  local sql="$1"
  local target="$2"
  docker compose exec -T mysql \
    mariadb -uroot "-p${MYSQL_ROOT_PASSWORD}" "${DB_NAME}" \
    -e "${sql}" > "${OUT}/${target}"
}

query_to_file "SHOW CREATE TABLE patient_data\G" "patient_data.txt"
query_to_file "SHOW CREATE TABLE form_encounter\G" "form_encounter.txt"
query_to_file "SHOW CREATE TABLE form_vitals\G" "form_vitals.txt"
query_to_file "SHOW CREATE TABLE forms\G" "forms.txt"
query_to_file "SELECT
  (SELECT COUNT(*) FROM patient_data) AS patient_data_rows,
  (SELECT COUNT(*) FROM form_encounter) AS form_encounter_rows,
  (SELECT COUNT(*) FROM form_vitals) AS form_vitals_rows,
  (SELECT COUNT(*) FROM forms) AS forms_rows;" "row-counts.txt"

echo "OpenEMR schema captured in:"
echo "  ${OUT}"
echo
ls -1 "${OUT}"
