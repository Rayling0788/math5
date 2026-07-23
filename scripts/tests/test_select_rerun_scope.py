from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from select_rerun_scope import read_edges, select_scope


class SelectRerunScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.edges_path = Path(self.temp.name) / "workflow_edges.csv"
        with self.edges_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["source_task", "target_task", "kind", "exported_fields"])
            writer.writerows(
                [
                    ["q1_fast", "q2_model", "blocking", "temperature,flux"],
                    ["q2_model", "q3_model", "blocking", "score"],
                    ["q1_cert", "q1_fast", "advisory", "cert_error"],
                    ["q1_cert", "q4_model", "advisory", "cert_error"],
                    ["q1_fast", "q4_model", "advisory", "temperature"],
                ]
            )
        self.edges = read_edges(self.edges_path)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_local_certification_failure_stays_local(self) -> None:
        self.assertEqual(
            select_scope(self.edges, "local_failure", "q1_cert"), ["q1_cert"]
        )

    def test_figure_artifact_change_stays_local(self) -> None:
        self.assertEqual(
            select_scope(self.edges, "artifact_change", "fig_q1_font"),
            ["fig_q1_font"],
        )

    def test_shared_contract_change_follows_blocking_descendants(self) -> None:
        self.assertEqual(
            select_scope(self.edges, "shared_contract_change", "q1_fast"),
            ["q1_fast", "q2_model", "q3_model"],
        )

    def test_changed_field_filters_first_blocking_edge(self) -> None:
        self.assertEqual(
            select_scope(
                self.edges,
                "accepted_output_change",
                "q1_fast",
                {"unused_field"},
            ),
            ["q1_fast"],
        )


if __name__ == "__main__":
    unittest.main()
