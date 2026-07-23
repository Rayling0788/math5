#!/usr/bin/env python3
"""Select the smallest rerun scope from a workflow dependency graph."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict, deque
from pathlib import Path


REQUIRED = {"source_task", "target_task", "kind", "exported_fields"}
LOCAL_EVENTS = {"local_failure", "artifact_change"}
PROPAGATING_EVENTS = {"accepted_output_change", "shared_contract_change"}
EVENTS = LOCAL_EVENTS | PROPAGATING_EVENTS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edges", type=Path, help="workflow_edges.csv")
    parser.add_argument("--event", choices=sorted(EVENTS), required=True)
    parser.add_argument("--task", required=True, help="owner/source task ID")
    parser.add_argument(
        "--changed-fields",
        nargs="*",
        default=[],
        help="optional exported fields changed by accepted_output_change",
    )
    return parser.parse_args()


def split_fields(raw: str) -> set[str]:
    normalized = raw.replace(";", ",").replace("|", ",")
    return {item.strip() for item in normalized.split(",") if item.strip()}


def read_edges(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        raise ValueError(f"edge file not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            raise ValueError("missing columns: " + ", ".join(missing))
        rows: list[dict[str, object]] = []
        for row_no, row in enumerate(reader, start=2):
            source = (row.get("source_task") or "").strip()
            target = (row.get("target_task") or "").strip()
            kind = (row.get("kind") or "").strip().lower()
            if not source or not target:
                raise ValueError(f"row {row_no}: source_task and target_task are required")
            if kind not in {"blocking", "advisory"}:
                raise ValueError(f"row {row_no}: kind must be blocking or advisory")
            rows.append(
                {
                    "source": source,
                    "target": target,
                    "kind": kind,
                    "fields": split_fields(row.get("exported_fields") or ""),
                }
            )
    return rows


def select_scope(
    edges: list[dict[str, object]],
    event: str,
    task: str,
    changed_fields: set[str] | None = None,
) -> list[str]:
    if event not in EVENTS:
        raise ValueError(f"unsupported event: {event}")
    if event in LOCAL_EVENTS:
        return [task]

    graph: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)
    for edge in edges:
        if edge["kind"] == "blocking":
            graph[str(edge["source"])].append(
                (str(edge["target"]), set(edge["fields"]))
            )

    changed = changed_fields or set()
    queue: deque[str] = deque([task])
    seen = {task}
    while queue:
        source = queue.popleft()
        for target, exported in sorted(graph.get(source, [])):
            if (
                event == "accepted_output_change"
                and source == task
                and changed
                and exported
                and changed.isdisjoint(exported)
            ):
                continue
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return [task] + sorted(seen - {task})


def main() -> int:
    args = parse_args()
    try:
        edges = read_edges(args.edges)
        scope = select_scope(edges, args.event, args.task, set(args.changed_fields))
    except ValueError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "event": args.event,
                "root_task": args.task,
                "rerun": scope,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
