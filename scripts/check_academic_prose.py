#!/usr/bin/env python3
"""Detect high-signal templated prose in mathematical modeling papers.

The checker is intentionally conservative. Chat/editing residue is an error. Other
patterns become a warning only when they form a cluster, because ordinary academic
Chinese legitimately uses formal transitions and repeated technical terms.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    category: str
    phrase: str
    severity: str
    start: int


CHAT_PATTERNS = (
    r"当然可以",
    r"下面是(?:修改|润色|重写|整理)后的(?:内容|版本|文本)",
    r"希望(?:这|以上内容).{0,12}(?:帮助|有用)",
    r"如有需要.{0,10}(?:继续|补充|调整|修改)",
    r"如果你(?:还)?需要",
    r"让我们(?:来)?(?:看|分析|讨论|开始)",
    r"以下是我(?:为你)?",
)

SOFT_PATTERNS = {
    "unsupported_elevation": (
        r"具有(?:十分|非常|重要|重大|深远|广泛)的(?:理论|现实|实践|工程|应用|推广)?意义",
        r"具有广泛的(?:应用|推广)前景",
        r"为.{0,24}奠定(?:了)?(?:坚实|良好|重要)?基础",
        r"标志着.{0,24}(?:重大|重要|关键)突破",
    ),
    "decorative_analysis": (
        r"(?:从而|进而)?(?:充分)?(?:彰显|凸显|体现)(?:了)?.{0,28}(?:价值|优势|意义|重要性)",
        r"为.{0,24}提供(?:了)?(?:强有力|有力|重要)支撑",
        r"进一步说明了该模型的(?:有效性|优越性|先进性)",
    ),
    "vague_authority": (
        r"(?:已有|相关|大量|多项)?研究(?:普遍)?(?:表明|指出|认为)",
        r"(?:有关|业内|行业)?专家(?:普遍)?(?:认为|指出|表示)",
        r"业内普遍认为",
        r"众所周知",
    ),
    "empty_signposting": (
        r"下面(?:将|我们将)(?:对)?.{0,24}(?:进行|展开)(?:详细|深入)?(?:分析|讨论|介绍)",
        r"接下来(?:我们)?(?:将|来)(?:对)?.{0,24}(?:分析|讨论|介绍)",
        r"本文将从.{0,30}(?:三个|三大|多种)方面",
    ),
    "generic_conclusion": (
        r"未来(?:发展)?前景(?:十分|非常)?广阔",
        r"具有(?:较高|很高|重要|广泛)的(?:参考|推广|应用)价值",
        r"为后续(?:研究|工作).{0,16}(?:基础|支撑)",
        r"相信.{0,20}(?:发挥|产生).{0,12}(?:作用|影响)",
    ),
    "promotional_language": (
        r"(?:国际|国内|行业)?领先(?:水平|地位|优势)?",
        r"(?:革命性|颠覆性|里程碑式|划时代)的",
        r"完美(?:地)?解决",
        r"卓越的(?:性能|表现|效果)",
    ),
    "filler_hedge": (
        r"值得注意的是",
        r"需要指出的是",
        r"不难发现",
        r"显而易见",
        r"不言而喻",
        r"从某种意义上说",
        r"在一定程度上可以认为",
    ),
}

ABSTRACT_NOUNS = (
    "协同",
    "闭环",
    "赋能",
    "体系",
    "范式",
    "生态",
    "抓手",
    "格局",
    "价值",
    "机制",
    "路径",
    "维度",
)


def strip_non_prose(text: str) -> str:
    """Remove code and comments while preserving offsets approximately."""

    def blank(match: re.Match[str]) -> str:
        return " " * (match.end() - match.start())

    patterns = (
        r"```.*?```",
        r"\\begin\{(?:lstlisting|verbatim|Verbatim|minted)\}.*?\\end\{(?:lstlisting|verbatim|Verbatim|minted)\}",
        r"(?m)(?<!\\)%.*$",
    )
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, blank, cleaned, flags=re.S)
    return cleaned


def _has_adjacent_citation(text: str, start: int, end: int, radius: int = 120) -> bool:
    context = text[max(0, start - radius) : min(len(text), end + radius)]
    return bool(re.search(r"\\cite\w*\{[^}]+\}|#cite\s*\(|@[A-Za-z0-9_:-]+|\[[0-9]{1,3}\]", context))


def _iter_sentences(text: str) -> Iterable[tuple[int, str]]:
    start = 0
    for match in re.finditer(r"[。！？!?；;\n]", text):
        sentence = text[start : match.end()]
        if sentence.strip():
            yield start, sentence
        start = match.end()
    if text[start:].strip():
        yield start, text[start:]


def scan_text(text: str) -> list[Finding]:
    cleaned = strip_non_prose(text)
    findings: list[Finding] = []

    for pattern in CHAT_PATTERNS:
        for match in re.finditer(pattern, cleaned):
            findings.append(Finding("chat_or_editing_residue", match.group(0), "error", match.start()))

    for category, patterns in SOFT_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, cleaned):
                if category == "vague_authority" and _has_adjacent_citation(cleaned, match.start(), match.end()):
                    continue
                findings.append(Finding(category, match.group(0), "candidate", match.start()))

    for sentence_start, sentence in _iter_sentences(cleaned):
        hits = [word for word in ABSTRACT_NOUNS if word in sentence]
        if len(hits) >= 4:
            excerpt = re.sub(r"\s+", "", sentence)[:80]
            findings.append(Finding("abstract_noun_chain", excerpt, "candidate", sentence_start))

    return sorted(findings, key=lambda item: (item.start, item.category))


def summarize(findings: Iterable[Finding]) -> dict[str, object]:
    items = list(findings)
    errors = [item for item in items if item.severity == "error"]
    candidates = [item for item in items if item.severity == "candidate"]
    category_counts: dict[str, int] = {}
    for item in candidates:
        category_counts[item.category] = category_counts.get(item.category, 0) + 1
    clustered = len(category_counts) >= 2 or sum(category_counts.values()) >= 3
    return {
        "errors": errors,
        "candidates": candidates,
        "category_counts": category_counts,
        "clustered": clustered,
    }


def scan_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    result = summarize(scan_text(text))
    result["path"] = str(path)
    return result


def _serializable(result: dict[str, object]) -> dict[str, object]:
    return {
        key: [asdict(item) for item in value] if key in {"errors", "candidates"} else value
        for key, value in result.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    exit_code = 0
    results = []
    for path in args.files:
        if not path.exists() or not path.is_file():
            continue
        result = scan_file(path)
        results.append(result)
        errors = result["errors"]
        if errors:
            exit_code = 1
            phrases = ", ".join(sorted({item.phrase for item in errors}))
            print(f"FAIL: chatbot/editing residue in {path}: {phrases}")
        if result["clustered"]:
            counts = result["category_counts"]
            details = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
            examples = ", ".join(sorted({item.phrase for item in result["candidates"]})[:5])
            print(f"WARN: templated-prose cluster in {path}: {details}; examples: {examples}")

    if args.as_json:
        print(json.dumps([_serializable(result) for result in results], ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
