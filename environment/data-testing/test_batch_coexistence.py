#!/usr/bin/env python3
"""
Load two different five-patient Project VITAL batches simultaneously and verify
that both remain valid. Then remove only the second batch and verify that the
first is still valid.
"""
import subprocess
import sys
from pathlib import Path

BATCH_A = "COEXIST-A"
BATCH_B = "COEXIST-B"


def run(cmd, expected=0):
    print("+", " ".join(map(str, cmd)))
    r = subprocess.run(cmd)
    if r.returncode != expected:
        raise SystemExit(
            f"Unexpected exit code {r.returncode}; expected {expected}"
        )
    return r


def main():
    repo = Path(__file__).resolve().parents[2]
    py = sys.executable
    env = repo / "environment" / "data-testing"
    dataset = repo / ".project-vital" / "data-testing" / "coexist-five"

    run([
        py, str(env / "generate_data.py"),
        "--size", "small", "--patients", "5", "--seed", "123",
        "--output", str(dataset)
    ])

    # Cleanup from prior attempts. Validator/reset semantics make repeat runs safe.
    for batch in (BATCH_A, BATCH_B):
        subprocess.run([
            py, str(env / "reset_loaded_data.py"),
            "--batch", batch, "--yes"
        ], stdout=subprocess.DEVNULL)

    run([
        py, str(env / "load_openemr.py"),
        str(dataset), "--batch", BATCH_A, "--yes"
    ])
    run([
        py, str(env / "validate_openemr_load.py"),
        "--batch", BATCH_A
    ])

    run([
        py, str(env / "load_openemr.py"),
        str(dataset), "--batch", BATCH_B, "--yes"
    ])
    run([
        py, str(env / "validate_openemr_load.py"),
        "--batch", BATCH_B
    ])

    # A must still be valid after B is loaded.
    run([
        py, str(env / "validate_openemr_load.py"),
        "--batch", BATCH_A
    ])

    # Remove only B.
    run([
        py, str(env / "reset_loaded_data.py"),
        "--batch", BATCH_B, "--yes"
    ])

    # B should now be absent; exit code 4 is expected.
    run([
        py, str(env / "validate_openemr_load.py"),
        "--batch", BATCH_B
    ], expected=4)

    # A must remain valid.
    run([
        py, str(env / "validate_openemr_load.py"),
        "--batch", BATCH_A
    ])

    print("\nBATCH COEXISTENCE TEST PASSED")
    print(f"Batch {BATCH_A} intentionally remains loaded for inspection.")
    print(
        "Remove it when finished with:\n"
        f"  python3 environment/data-testing/reset_loaded_data.py "
        f"--batch {BATCH_A}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
