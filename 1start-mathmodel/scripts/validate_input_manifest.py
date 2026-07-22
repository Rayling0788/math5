#!/usr/bin/env python3
"""Validate that every supplied input is inventoried, profiled, and dispositioned."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


REQUIRED = {
    "input_id",
    "source_path",
    "file_type",
    "sha256",
    "size_bytes",
    "description",
    "questions",
    "profile_path",
    "usage_status",
    "exclusion_reason",
    "status",
}
USAGE = {"used", "reference", "excluded"}
STATUSES = {"inventoried", "inspected", "accepted", "rejected"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--final", action="store_true")
    return parser.parse_args()


def resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    manifest = args.manifest.resolve()
    errors: list[str] = []

    if not manifest.is_file():
        print(f"FAIL: manifest not found: {manifest}", file=sys.stderr)
        return 1

    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            print("FAIL: missing columns: " + ", ".join(missing), file=sys.stderr)
            return 1
        rows = list(reader)

    if not rows:
        print("FAIL: manifest has no rows", file=sys.stderr)
        return 1

    ids: set[str] = set()
    for row_no, row in enumerate(rows, start=2):
        for field in REQUIRED - {"exclusion_reason"}:
            if not (row.get(field) or "").strip():
                errors.append(f"row {row_no}: required field {field} is empty")

        input_id = row["input_id"].strip()
        if input_id in ids:
            errors.append(f"row {row_no}: duplicate input_id {input_id!r}")
        ids.add(input_id)

        usage = row["usage_status"].strip().lower()
        status = row["status"].strip().lower()
        if usage not in USAGE:
            errors.append(f"row {row_no}: invalid usage_status {usage!r}")
        if status not in STATUSES:
            errors.append(f"row {row_no}: invalid status {status!r}")
        if usage == "excluded" and not row["exclusion_reason"].strip():
            errors.append(f"row {row_no}: excluded input requires exclusion_reason")
        if usage != "excluded" and row["exclusion_reason"].strip():
            errors.append(f"row {row_no}: non-excluded input has exclusion_reason")
        if args.final and status != "accepted":
            errors.append(f"row {row_no}: final input is not accepted")

        source = resolve(root, row["source_path"].strip())
        if not source.is_file():
            errors.append(f"row {row_no}: source file missing: {source}")
        else:
            try:
                declared_size = int(row["size_bytes"].strip())
                if declared_size != source.stat().st_size:
                    errors.append(f"row {row_no}: size_bytes does not match source")
            except ValueError:
                errors.append(f"row {row_no}: size_bytes is not an integer")

            declared_hash = row["sha256"].strip()
            if not SHA256_RE.match(declared_hash):
                errors.append(f"row {row_no}: invalid SHA-256 format")
            elif digest(source).lower() != declared_hash.lower():
                errors.append(f"row {row_no}: SHA-256 does not match source")

        profile = resolve(root, row["profile_path"].strip())
        try:
            profile.relative_to(root)
        except ValueError:
            errors.append(f"row {row_no}: profile_path escapes project root")
        if not profile.is_file() or profile.stat().st_size == 0:
            errors.append(f"row {row_no}: profile file missing or empty: {profile}")

    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        print(f"SUMMARY: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1

    print(f"SUMMARY: PASS ({len(rows)} accepted input records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
