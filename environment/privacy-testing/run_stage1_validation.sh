#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
SRC="${ROOT}/.project-vital/privacy-testing/source"
OUT="${ROOT}/.project-vital/privacy-testing/pseudonymized"

rm -rf "${ROOT}/.project-vital/privacy-testing"
mkdir -p "${ROOT}/.project-vital/privacy-testing"

echo "== 1. Generate 200 synthetic source patients =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small --seed 42 --output "${SRC}"

echo
echo "== 2. Create pseudonymized research export =="
python3 "${ROOT}/environment/privacy-testing/pseudonymize_data.py" \
  "${SRC}" --output "${OUT}" --secret "LOCAL-STAGE1-VALIDATION-ONLY"

echo
echo "== 3. Validate removal of direct identifiers and referential integrity =="
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export.py" \
  "${OUT}" --min-k 1

echo
echo "== 4. Measure quasi-identifier re-identification risk =="
python3 "${ROOT}/environment/privacy-testing/reidentification_probe.py" \
  "${OUT}/patients.csv"

echo
echo "== 5. Verify pseudonymization is deterministic =="
OUT2="${ROOT}/.project-vital/privacy-testing/pseudonymized-repeat"
python3 "${ROOT}/environment/privacy-testing/pseudonymize_data.py" \
  "${SRC}" --output "${OUT2}" --secret "LOCAL-STAGE1-VALIDATION-ONLY" >/dev/null

diff -q "${OUT}/patients.csv" "${OUT2}/patients.csv"
diff -q "${OUT}/encounters.csv" "${OUT2}/encounters.csv"
diff -q "${OUT}/vitals.csv" "${OUT2}/vitals.csv"

echo
echo "STAGE 1 PRIVACY VALIDATION PASSED"
