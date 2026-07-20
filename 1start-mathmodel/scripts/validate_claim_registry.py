#!/usr/bin/env python3
"""Validate canonical claims and their source traceability."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


REQUIRED = {
    "claim_id",
    "question_id",
    "scenario_key",
    "candidate_id",
    "metric_id",
    "value_type",
    "value",
    "unit",
    "result_type",
    "source_file",
    "source_key",
    "constraint_status",
    "status",
}
VALUE_TYPES = {"number", "text"}
RESULT_TYPES = {"strict_feasible", "validated_estimate", "scenario_result", "ideal_upper_bound"}
CONSTRAINT_STATUSES = {"pass", "fail", "not_applicable", "unchecked"}
STATUSES = {"planned", "generated", "checked", "accepted", "rejected"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--final", action="store_true")
    return parser.parse_args()


def resolve_source(root: Path, value: str, row_no: int, errors: list[str]) -> None:
    raw = Path(value)
    candidate = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"row {row_no}: source_file escapes project root: {value}")
        return
    if not candidate.is_file() or candidate.stat().st_size == 0:
        errors.append(f"row {row_no}: missing or empty source_file: {value}")


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    registry = args.registry.resolve()
    errors: list[str] = []

    if not registry.is_file():
        print(f"FAIL: registry not found: {registry}", file=sys.stderr)
        return 1

    with registry.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            print("FAIL: missing columns: " + ", ".join(missing), file=sys.stderr)
            return 1
        rows = list(reader)

    if not rows:
        print("FAIL: registry has no rows", file=sys.stderr)
        return 1

    claim_ids: set[str] = set()
    canonical: dict[tuple[str, str, str, str], tuple[str, str, str]] = {}

    for row_no, row in enumerate(rows, start=2):
        for field in REQUIRED:
            if not (row.get(field) or "").strip():
                errors.append(f"row {row_no}: required field {field} is empty")

        claim_id = row["claim_id"].strip()
        if claim_id in claim_ids:
            errors.append(f"row {row_no}: duplicate claim_id {claim_id!r}")
        claim_ids.add(claim_id)

        value_type = row["value_type"].strip().lower()
        result_type = row["result_type"].strip().lower()
        constraint_status = row["constraint_status"].strip().lower()
        status = row["status"].strip().lower()

        if value_type not in VALUE_TYPES:
            errors.append(f"row {row_no}: invalid value_type {value_type!r}")
        if result_type not in RESULT_TYPES:
            errors.append(f"row {row_no}: invalid result_type {result_type!r}")
        if constraint_status not in CONSTRAINT_STATUSES:
            errors.append(f"row {row_no}: invalid constraint_status {constraint_status!r}")
        if status not in STATUSES:
            errors.append(f"row {row_no}: invalid status {status!r}")
        if args.final and status != "accepted":
            errors.append(f"row {row_no}: final claim is not accepted")
        if args.final and constraint_status not in {"pass", "not_applicable"}:
            errors.append(f"row {row_no}: final claim has unresolved constraints")

        value = row["value"].strip()
        if value_type == "number":
            try:
                number = float(value)
                if not math.isfinite(number):
                    raise ValueError
            except ValueError:
                errors.append(f"row {row_no}: numerical value is not finite: {value!r}")
            if not row["unit"].strip():
                errors.append(f"row {row_no}: numerical claim requires a unit or '1'")

        resolve_source(root, row["source_file"].strip(), row_no, errors)

        key = (
            row["question_id"].strip(),
            row["scenario_key"].strip(),
            row["candidate_id"].strip(),
            row["metric_id"].strip(),
        )
        signature = (value_type, value, row["unit"].strip())
        previous = canonical.get(key)
        if previous is not None and previous != signature:
            errors.append(f"row {row_no}: conflicting canonical value for {key}")
        canonical[key] = signature

    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        print(f"SUMMARY: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1

    print(f"SUMMARY: PASS ({len(rows)} canonical claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
