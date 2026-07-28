import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_paper_structure.py"
SPEC = importlib.util.spec_from_file_location("validate_paper_structure", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AssumptionCountTests(unittest.TestCase):
    def test_validator_does_not_require_fixed_model_summary_heading(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn('"模型汇总"', source)

    def test_counts_latex_enumerate_items(self):
        body = "\\begin{enumerate}\n" + "\n".join(
            f"  \\item assumption {index}" for index in range(1, 6)
        ) + "\n\\end{enumerate}"
        self.assertEqual(MODULE.count_assumption_items(body, "latex"), 5)

    def test_detects_six_latex_items(self):
        body = "\n".join(f"\\item assumption {index}" for index in range(1, 7))
        self.assertEqual(MODULE.count_assumption_items(body, "latex"), 6)

    def test_counts_typst_enum_items(self):
        self.assertEqual(MODULE.count_assumption_items("+ first\n+ second", "typst"), 2)

    def test_counts_named_assumptions_without_list_markup(self):
        body = "假设一及其依据。\n假设二：另一项前提。"
        self.assertEqual(MODULE.count_assumption_items(body, "latex"), 2)


if __name__ == "__main__":
    unittest.main()
