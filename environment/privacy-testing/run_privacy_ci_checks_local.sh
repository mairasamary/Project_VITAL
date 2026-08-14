#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
BASE="${ROOT}/.project-vital/privacy-testing/local-ci"
SRC="${BASE}/source"
OUT="${BASE}/export"
SECRET="LOCAL-CI-TEACHING-SECRET-ONLY"

rm -rf "${BASE}"
mkdir -p "${BASE}"

echo "== 1. Generate deterministic synthetic source =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small \
  --patients 200 \
  --seed 42 \
  --output "${SRC}"

echo
echo "== 2. Create privacy-preserving export =="
python3 "${ROOT}/environment/privacy-testing/privacy_transform.py" \
  "${SRC}" \
  --output "${OUT}" \
  --secret "${SECRET}" \
  --age-band 20 \
  --geo state \
  --time year \
  --suppress-sex

echo
echo "== 3. Validate privacy export =="
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${OUT}" \
  --qi age_band geography \
  --min-k 3

echo
echo "== 4. Verify utility preservation =="
python3 "${ROOT}/environment/privacy-testing/utility_report.py" \
  "${SRC}" "${OUT}"

echo
echo "== 5. Prove direct-identifier leakage is rejected =="
cp -R "${OUT}" "${BASE}/leaked"
python3 "${ROOT}/environment/privacy-testing/privacy_corrupt.py" \
  "${BASE}/leaked" --defect leak-email

set +e
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${BASE}/leaked" --qi age_band geography --min-k 3
LEAK_RC=$?
set -e
if [ "${LEAK_RC}" -eq 0 ]; then
  echo "ERROR: privacy validator unexpectedly accepted leaked data."
  exit 1
fi
echo "Direct identifier leakage correctly rejected."

echo
echo "== 6. Prove broken pseudonymous relationship is rejected =="
cp -R "${OUT}" "${BASE}/broken"
python3 "${ROOT}/environment/privacy-testing/privacy_corrupt.py" \
  "${BASE}/broken" --defect break-encounter-subject

set +e
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${BASE}/broken" --qi age_band geography --min-k 3
REL_RC=$?
set -e
if [ "${REL_RC}" -eq 0 ]; then
  echo "ERROR: privacy validator unexpectedly accepted broken relationship."
  exit 1
fi
echo "Broken pseudonymous relationship correctly rejected."

echo
echo "LOCAL PRIVACY CI CHECKS PASSED"
