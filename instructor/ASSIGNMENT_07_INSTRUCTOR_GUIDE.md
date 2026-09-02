# Assignment 7 — Instructor Validation Guide

Before releasing to students:

1. Run `bash environment/security-testing/run_stage1_validation.sh`.
2. Start OpenEMR and run `bash environment/security-testing/run_openemr_baseline.sh`.
3. Run `bash environment/security-testing/run_unauthenticated_check.sh` and validate the protected path for the semester image.
4. Push and confirm **Project VITAL Security Tests** is GREEN.
5. Remove only `X-Content-Type-Options: nosniff` from the controlled fixture and confirm local/GitHub RED.
6. Restore it and confirm GREEN.

Expected sequence: **GREEN → RED → GREEN**.

Do not expand this into brute force, credential stuffing, DoS, high-volume fuzzing, destructive testing, or testing public/BC production systems. Students should distinguish observed evidence from proof of exploitability or overall security.
