#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
BASE="${ROOT}/.project-vital/privacy-testing/stage2"
SRC="${BASE}/source"
SECRET="LOCAL-STAGE2-VALIDATION-ONLY"

rm -rf "${BASE}"
mkdir -p "${BASE}"

echo "== 1. Generate source dataset =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small --seed 42 --output "${SRC}" >/dev/null

echo "== 2. Baseline privacy strategy =="
python3 "${ROOT}/environment/privacy-testing/privacy_transform.py" \
  "${SRC}" --output "${BASE}/baseline" --secret "${SECRET}" \
  --age-band 10 --geo postal3 --time month >/dev/null

set +e
python3 "${ROOT}/environment/privacy-testing/k_anonymity_report.py" \
  "${BASE}/baseline/patients.csv" \
  --fields age_band sex geography --threshold 3
BASE_RC=$?
set -e
echo "Baseline k>=3 exit code: ${BASE_RC} (failure is expected if unique/small classes remain)"

echo
echo "== 3. Stronger generalization strategy =="
python3 "${ROOT}/environment/privacy-testing/privacy_transform.py" \
  "${SRC}" --output "${BASE}/stronger" --secret "${SECRET}" \
  --age-band 20 --geo state --time year --suppress-sex >/dev/null

python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${BASE}/stronger" --qi age_band geography --min-k 3

echo
echo "== 4. Utility comparison =="
python3 "${ROOT}/environment/privacy-testing/utility_report.py" \
  "${SRC}" "${BASE}/stronger"

echo
echo "== 5. Direct identifier leakage must be detected =="
cp -R "${BASE}/stronger" "${BASE}/leaked"
python3 "${ROOT}/environment/privacy-testing/privacy_corrupt.py" \
  "${BASE}/leaked" --defect leak-email
set +e
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${BASE}/leaked" --qi age_band geography --min-k 3
LEAK_RC=$?
set -e
if [ "${LEAK_RC}" -eq 0 ]; then
  echo "ERROR: leaked identifier was not detected"
  exit 1
fi
echo "Direct identifier leak correctly rejected."

echo
echo "== 6. Broken pseudonymous relationship must be detected =="
cp -R "${BASE}/stronger" "${BASE}/broken"
python3 "${ROOT}/environment/privacy-testing/privacy_corrupt.py" \
  "${BASE}/broken" --defect break-encounter-subject
set +e
python3 "${ROOT}/environment/privacy-testing/validate_privacy_export_v2.py" \
  "${BASE}/broken" --qi age_band geography --min-k 3
REL_RC=$?
set -e
if [ "${REL_RC}" -eq 0 ]; then
  echo "ERROR: broken relationship was not detected"
  exit 1
fi
echo "Broken pseudonymous relationship correctly rejected."

echo
echo "STAGE 2 PRIVACY VALIDATION PASSED"
