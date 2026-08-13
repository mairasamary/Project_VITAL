#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SRC="${ROOT}/.project-vital/openemr-unit"
TEAM_TESTS="${ROOT}/assignment-03/tests"
TARGET_TESTS="${SRC}/tests/Tests/Isolated/ProjectVITAL"
IMAGE="openemr/openemr:flex-3.22-php-8.2"

if ! docker info >/dev/null 2>&1; then
    echo "Docker is not available or the Docker daemon is not running."
    echo "Start Docker Desktop/Engine and run this command again."
    exit 1
fi

if [ ! -d "${SRC}/.git" ]; then
    echo "OpenEMR unit-test checkout was not found."
    echo "Run:"
    echo "  bash environment/unit-testing/setup-unit-tests.sh"
    exit 1
fi

if [ ! -d "${TEAM_TESTS}" ]; then
    echo "No Assignment 3 test directory found:"
    echo "  ${TEAM_TESTS}"
    echo
    echo "Create it and add at least one PHPUnit test."
    exit 1
fi

mkdir -p "${TARGET_TESTS}"
find "${TARGET_TESTS}" -mindepth 1 -maxdepth 1 -type f -name '*.php' -delete

test_count=0
while IFS= read -r -d '' file; do
    cp "${file}" "${TARGET_TESTS}/"
    test_count=$((test_count + 1))
done < <(find "${TEAM_TESTS}" -maxdepth 1 -type f -name '*Test.php' -print0)

if [ "${test_count}" -eq 0 ]; then
    echo "No *Test.php files were found in ${TEAM_TESTS}"
    exit 1
fi

echo "Copied ${test_count} Project VITAL test file(s)."
echo "Using image: ${IMAGE}"

PHPUNIT_TARGET="tests/Tests/Isolated/ProjectVITAL"

if [ "$#" -ge 1 ]; then
    requested="$1"
    if [ ! -f "${TARGET_TESTS}/${requested}" ]; then
        echo "Requested test file not found after copy:"
        echo "  ${requested}"
        exit 1
    fi
    PHPUNIT_TARGET="${PHPUNIT_TARGET}/${requested}"
fi

docker run --rm \
    --entrypoint /bin/sh \
    -v "${SRC}:/workspace" \
    -w /workspace \
    "${IMAGE}" \
    -lc "
        set -e
        echo 'PHP:'
        php --version | head -n 1
        echo 'Composer:'
        composer --version
        if [ ! -f vendor/bin/phpunit ]; then
            echo 'Installing OpenEMR Composer dependencies...'
            composer install --prefer-dist --no-progress
        fi
        echo
        echo 'Running Project VITAL isolated tests...'
        vendor/bin/phpunit -c phpunit-isolated.xml '${PHPUNIT_TARGET}'
    "
