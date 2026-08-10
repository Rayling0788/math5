import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "check_academic_prose.py"
SPEC = importlib.util.spec_from_file_location("check_academic_prose", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AcademicProseCheckTests(unittest.TestCase):
    def test_clean_technical_prose_has_no_cluster(self):
        text = "设浮子位移为 z。由静水恢复力与弹簧力平衡可得方程，代入附件参数后求解稳态振幅。"
        summary = MODULE.summarize(MODULE.scan_text(text))
        self.assertFalse(summary["errors"])
        self.assertFalse(summary["clustered"])

    def test_single_formal_transition_is_not_flagged(self):
        text = "在此基础上，进一步计算相邻两个周期的状态差，并判断是否达到收敛阈值。"
        summary = MODULE.summarize(MODULE.scan_text(text))
        self.assertFalse(summary["errors"])
        self.assertFalse(summary["clustered"])

    def test_multiple_soft_patterns_form_warning_cluster(self):
        text = (
            "本模型具有广泛的应用前景，为后续研究奠定坚实基础。"
            "值得注意的是，该结果进一步说明了该模型的优越性。"
        )
        summary = MODULE.summarize(MODULE.scan_text(text))
        self.assertTrue(summary["clustered"])
        self.assertGreaterEqual(len(summary["category_counts"]), 2)

    def test_chat_residue_is_error(self):
        summary = MODULE.summarize(MODULE.scan_text("下面是修改后的内容，希望这对你有帮助。"))
        self.assertTrue(summary["errors"])

    def test_vague_authority_with_citation_is_not_flagged(self):
        text = r"已有研究表明该方法在周期系统中收敛\cite{smith2020}。"
        summary = MODULE.summarize(MODULE.scan_text(text))
        categories = {item.category for item in summary["candidates"]}
        self.assertNotIn("vague_authority", categories)

    def test_code_blocks_are_ignored(self):
        text = "正文给出求解过程。\n```text\n当然可以，下面是修改后的内容\n```"
        summary = MODULE.summarize(MODULE.scan_text(text))
        self.assertFalse(summary["errors"])


if __name__ == "__main__":
    unittest.main()
