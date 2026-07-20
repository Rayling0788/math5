#!/usr/bin/env python3
"""Validate traceability and visual-evidence coverage in figure_manifest.csv."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


REQUIRED_COLUMNS = {
    "figure_id",
    "panel_id",
    "question_id",
    "scenario_key",
    "regime_id",
    "model_level",
    "claim_id",
    "claim_text",
    "evidence_role",
    "figure_type",
    "generator",
    "script_path",
    "data_path",
    "pdf_path",
    "png_path",
    "paper_section",
    "status",
}

ROLES = {
    "overview",
    "architecture",
    "mechanism",
    "geometry",
    "material",
    "boundary",
    "discretization",
    "input",
    "result",
    "comparison",
    "tradeoff",
    "validation",
    "sensitivity",
    "diagnostic",
}
GENERATORS = {"matlab", "drawio", "latex", "other"}
STATUSES = {"planned", "generated", "checked", "accepted", "rejected"}
MODEL_LEVELS = {
    "conceptual",
    "analytical",
    "reduced",
    "numerical",
    "high_fidelity",
    "experimental",
}
DATA_ROLES = {"result", "comparison", "tradeoff", "validation", "sensitivity", "diagnostic"}
COVERAGE = {
    "mechanism/input": {
        "mechanism",
        "geometry",
        "material",
        "boundary",
        "discretization",
        "input",
        "architecture",
    },
    "primary result": {"result", "comparison", "tradeoff"},
    "validation": {"validation", "sensitivity", "diagnostic"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--questions", nargs="*", default=[])
    parser.add_argument("--min-core", type=int, default=0)
    parser.add_argument("--min-matlab", type=int, default=0)
    parser.add_argument("--final", action="store_true", help="Require accepted status")
    return parser.parse_args()


def project_file(root: Path, value: str, field: str, row_no: int, errors: list[str]) -> Path | None:
    value = value.strip()
    if not value:
        errors.append(f"row {row_no}: {field} is empty")
        return None
    raw = Path(value)
    candidate = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"row {row_no}: {field} escapes project root: {value}")
        return None
    if not candidate.is_file() or candidate.stat().st_size == 0:
        errors.append(f"row {row_no}: missing or empty {field}: {value}")
    return candidate


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    manifest = args.manifest.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not manifest.is_file():
        print(f"FAIL: manifest not found: {manifest}", file=sys.stderr)
        return 1

    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - fields)
        if missing:
            print("FAIL: missing columns: " + ", ".join(missing), file=sys.stderr)
            return 1
        rows = list(reader)

    if not rows:
        print("FAIL: manifest has no rows", file=sys.stderr)
        return 1

    seen: set[tuple[str, str]] = set()
    roles_by_question: dict[str, set[str]] = defaultdict(set)
    generator_counts: Counter[str] = Counter()

    for row_no, row in enumerate(rows, start=2):
        for field in REQUIRED_COLUMNS:
            if not (row.get(field) or "").strip():
                errors.append(f"row {row_no}: required field {field} is empty")

        key = (row["figure_id"].strip(), row["panel_id"].strip())
        if key in seen:
            errors.append(f"row {row_no}: duplicate figure_id/panel_id {key[0]}/{key[1]}")
        seen.add(key)

        question = row["question_id"].strip()
        role = row["evidence_role"].strip().lower()
        generator = row["generator"].strip().lower()
        status = row["status"].strip().lower()
        model_level = row["model_level"].strip().lower()

        if not (question == "Q0" or (question.startswith("Q") and question[1:].isdigit())):
            errors.append(f"row {row_no}: invalid question_id {question!r}")
        if role not in ROLES:
            errors.append(f"row {row_no}: invalid evidence_role {role!r}")
        if generator not in GENERATORS:
            errors.append(f"row {row_no}: invalid generator {generator!r}")
        if status not in STATUSES:
            errors.append(f"row {row_no}: invalid status {status!r}")
        if model_level not in MODEL_LEVELS:
            errors.append(f"row {row_no}: invalid model_level {model_level!r}")
        if args.final and status != "accepted":
            errors.append(f"row {row_no}: final manifest row is not accepted")

        roles_by_question[question].add(role)
        generator_counts[generator] += 1

        pdf_file = project_file(root, row["pdf_path"], "pdf_path", row_no, errors)
        png_file = project_file(root, row["png_path"], "png_path", row_no, errors)
        if pdf_file and pdf_file.suffix.lower() != ".pdf":
            errors.append(f"row {row_no}: pdf_path must end in .pdf")
        if png_file and png_file.suffix.lower() != ".png":
            errors.append(f"row {row_no}: png_path must end in .png")

        needs_data = role in DATA_ROLES or generator == "matlab"
        if needs_data:
            project_file(root, row["data_path"], "data_path", row_no, errors)
        elif row["data_path"].strip():
            project_file(root, row["data_path"], "data_path", row_no, errors)

        script_value = row["script_path"].strip()
        if generator == "matlab":
            script_file = project_file(root, script_value, "script_path", row_no, errors)
            if script_file and script_file.suffix.lower() != ".m":
                errors.append(f"row {row_no}: MATLAB generator must be a .m file")
        elif script_value:
            project_file(root, script_value, "script_path", row_no, errors)

        if len(row["claim_text"].strip()) < 8:
            warnings.append(f"row {row_no}: claim_text may be too vague")

    questions = args.questions or sorted(q for q in roles_by_question if q != "Q0")
    for question in questions:
        found = roles_by_question.get(question, set())
        for label, accepted_roles in COVERAGE.items():
            if not (found & accepted_roles):
                errors.append(f"{question}: missing {label} evidence role")

    if len(rows) < args.min_core:
        errors.append(f"core evidence units {len(rows)} < required {args.min_core}")
    if generator_counts["matlab"] < args.min_matlab:
        errors.append(
            f"MATLAB evidence units {generator_counts['matlab']} < required {args.min_matlab}"
        )

    for warning in warnings:
        print("WARN: " + warning)
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        print(f"SUMMARY: FAIL ({len(errors)} errors, {len(warnings)} warnings)", file=sys.stderr)
        return 1

    print(
        "SUMMARY: PASS "
        f"({len(rows)} evidence units, {generator_counts['matlab']} MATLAB, "
        f"{len(questions)} checked questions, {len(warnings)} warnings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
