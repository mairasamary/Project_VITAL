#!/usr/bin/env python3
"""
Project VITAL — Assignment 4 data-scale benchmark utility.

Measures:
- synthetic data generation
- intermediate CSV validation
- OpenEMR database load
- post-load OpenEMR validation

Results are written to both CSV and Markdown.

By default the benchmark batch is reset after a successful run.
Use --keep-loaded to leave the benchmark batch in OpenEMR for UI inspection.

Examples:
    python3 environment/data-testing/benchmark.py --size small --seed 42
    python3 environment/data-testing/benchmark.py --size medium --seed 42
    python3 environment/data-testing/benchmark.py --all --seed 42
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

SIZES = ("small", "medium", "high")
EXPECTED_PATIENTS = {"small": 200, "medium": 2000, "high": 20000}


def run_timed(cmd: list[str], *, cwd: Path | None = None, quiet: bool = False):
    start = time.perf_counter()
    if quiet:
        result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    else:
        result = subprocess.run(cmd, cwd=cwd, text=True)
    elapsed = time.perf_counter() - start
    return result, elapsed


def short_batch(size: str, seed: int) -> str:
    # external_id is varchar(20), so keep comfortably below the limit.
    code = {"small": "S", "medium": "M", "high": "H"}[size]
    return f"BENCH-{code}-{seed}-{uuid.uuid4().hex[:5]}"[:20]


def load_manifest(dataset: Path):
    return json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))


def benchmark_one(repo: Path, size: str, seed: int, keep_loaded: bool):
    env = repo / "environment" / "data-testing"
    dataset = repo / ".project-vital" / "data-testing" / "benchmarks" / f"{size}-seed-{seed}"
    batch = short_batch(size, seed)

    generator = env / "generate_data.py"
    validator = env / "validate_data.py"
    loader = env / "load_openemr.py"
    db_validator = env / "validate_openemr_load.py"
    resetter = env / "reset_loaded_data.py"

    print()
    print("=" * 72)
    print(f"PROJECT VITAL BENCHMARK — {size.upper()}")
    print("=" * 72)
    print(f"Seed:  {seed}")
    print(f"Batch: {batch}")
    print()

    gen_cmd = [
        sys.executable, str(generator),
        "--size", size,
        "--seed", str(seed),
        "--output", str(dataset),
    ]
    result, generation_seconds = run_timed(gen_cmd)
    if result.returncode != 0:
        return {
            "size": size, "seed": seed, "batch": batch,
            "status": "generation_failed",
            "generation_seconds": generation_seconds,
        }

    manifest = load_manifest(dataset)

    val_cmd = [sys.executable, str(validator), str(dataset)]
    result, csv_validation_seconds = run_timed(val_cmd)
    if result.returncode != 0:
        return {
            "size": size, "seed": seed, "batch": batch,
            "status": "csv_validation_failed",
            "generation_seconds": generation_seconds,
            "csv_validation_seconds": csv_validation_seconds,
            **manifest["counts"],
        }

    load_cmd = [
        sys.executable, str(loader),
        str(dataset),
        "--batch", batch,
        "--yes",
    ]
    result, db_load_seconds = run_timed(load_cmd)
    if result.returncode != 0:
        return {
            "size": size, "seed": seed, "batch": batch,
            "status": "db_load_failed",
            "generation_seconds": generation_seconds,
            "csv_validation_seconds": csv_validation_seconds,
            "db_load_seconds": db_load_seconds,
            **manifest["counts"],
        }

    db_val_cmd = [
        sys.executable, str(db_validator),
        "--batch", batch,
    ]
    result, db_validation_seconds = run_timed(db_val_cmd)
    status = "valid" if result.returncode == 0 else "db_validation_failed"

    reset_seconds = ""
    if status == "valid" and not keep_loaded:
        reset_cmd = [
            sys.executable, str(resetter),
            "--batch", batch,
            "--yes",
        ]
        reset_result, reset_seconds = run_timed(reset_cmd)
        if reset_result.returncode != 0:
            status = "reset_failed"

    row = {
        "size": size,
        "seed": seed,
        "batch": batch,
        "patients": manifest["counts"]["patients"],
        "encounters": manifest["counts"]["encounters"],
        "vitals": manifest["counts"]["vitals"],
        "generation_seconds": round(generation_seconds, 4),
        "csv_validation_seconds": round(csv_validation_seconds, 4),
        "db_load_seconds": round(db_load_seconds, 4),
        "db_validation_seconds": round(db_validation_seconds, 4),
        "reset_seconds": round(reset_seconds, 4) if isinstance(reset_seconds, float) else reset_seconds,
        "status": status,
        "kept_loaded": bool(keep_loaded and status == "valid"),
    }
    return row


def write_csv_report(path: Path, rows):
    fields = [
        "size", "seed", "batch", "patients", "encounters", "vitals",
        "generation_seconds", "csv_validation_seconds",
        "db_load_seconds", "db_validation_seconds",
        "reset_seconds", "status", "kept_loaded",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def fmt(v):
    if v == "" or v is None:
        return "—"
    if isinstance(v, (int, float)):
        return f"{v:.4f}" if isinstance(v, float) else str(v)
    return str(v)


def write_markdown_report(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project VITAL — Data Testing Benchmark Results",
        "",
        "| Scale | Patients | Encounters | Vitals | Generate (s) | CSV Validate (s) | DB Load (s) | DB Validate (s) | Reset (s) | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('size','')} | {r.get('patients','')} | "
            f"{r.get('encounters','')} | {r.get('vitals','')} | "
            f"{fmt(r.get('generation_seconds',''))} | "
            f"{fmt(r.get('csv_validation_seconds',''))} | "
            f"{fmt(r.get('db_load_seconds',''))} | "
            f"{fmt(r.get('db_validation_seconds',''))} | "
            f"{fmt(r.get('reset_seconds',''))} | {r.get('status','')} |"
        )

    lines += [
        "",
        "## Notes",
        "",
        "- Times are wall-clock measurements from the machine running the benchmark.",
        "- Database timing depends on hardware, Docker resources, existing database size, and other system activity.",
        "- The benchmark measures data-generation and data-loading behavior; it is not a formal performance benchmark.",
        "- By default each benchmark batch is removed after validation so the same scale can be rerun safely.",
        "- Use `--keep-loaded` only when the dataset must remain available for OpenEMR UI inspection.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--size", choices=SIZES)
    group.add_argument("--all", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--keep-loaded", action="store_true")
    ap.add_argument(
        "--results-dir",
        default=".project-vital/data-testing/benchmark-results",
        help="directory for benchmark-results.csv and benchmark-results.md",
    )
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[2]
    sizes = list(SIZES) if args.all else [args.size]

    if args.all and args.keep_loaded:
        print(
            "WARNING: --all --keep-loaded will leave all three benchmark "
            "datasets in OpenEMR.",
            file=sys.stderr,
        )

    rows = []
    for size in sizes:
        row = benchmark_one(repo, size, args.seed, args.keep_loaded)
        rows.append(row)
        if row.get("status") != "valid":
            print(f"\nBenchmark stopped: {size} status={row.get('status')}")
            break

    out = (repo / args.results_dir).resolve()
    csv_path = out / "benchmark-results.csv"
    md_path = out / "benchmark-results.md"

    write_csv_report(csv_path, rows)
    write_markdown_report(md_path, rows)

    print()
    print("=" * 72)
    print("BENCHMARK SUMMARY")
    print("=" * 72)
    for r in rows:
        print(
            f"{r.get('size',''):6} "
            f"patients={r.get('patients','?'):>6} "
            f"generate={fmt(r.get('generation_seconds')):>8}s "
            f"load={fmt(r.get('db_load_seconds')):>8}s "
            f"db-validate={fmt(r.get('db_validation_seconds')):>8}s "
            f"status={r.get('status')}"
        )

    print()
    print("CSV report:     ", csv_path)
    print("Markdown report:", md_path)

    return 0 if rows and all(r.get("status") == "valid" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
