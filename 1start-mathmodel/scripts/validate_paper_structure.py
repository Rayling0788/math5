#!/usr/bin/env python3
"""Validate per-question analysis, segmented Chinese abstract, and assumptions."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CN_DIGITS = "零一二三四五六七八九"


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    path: Path
    line: int


def chinese_number(value: int) -> str:
    if value < 10:
        return CN_DIGITS[value]
    if value == 10:
        return "十"
    if value < 20:
        return "十" + CN_DIGITS[value - 10]
    if value < 100:
        tens, ones = divmod(value, 10)
        return CN_DIGITS[tens] + "十" + (CN_DIGITS[ones] if ones else "")
    return str(value)


def question_number(question_id: str, fallback: int) -> int:
    match = re.search(r"\d+", question_id)
    return int(match.group()) if match else fallback


def strip_tex_comments(text: str) -> str:
    clean_lines = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        clean_lines.append(line[: match.start()] if match else line)
    return "\n".join(clean_lines)


def strip_typst_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?m)//.*$", "", text)


def read_sources(paper_dir: Path, engine: str) -> list[tuple[Path, str]]:
    suffix = ".tex" if engine == "latex" else ".typ"
    sources = []
    for path in sorted(paper_dir.rglob(f"*{suffix}")):
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        text = strip_tex_comments(text) if engine == "latex" else strip_typst_comments(text)
        sources.append((path, text))
    return sources


def detect_engine(paper_dir: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    if (paper_dir / "main.tex").exists() or any(paper_dir.rglob("*.tex")):
        return "latex"
    if (paper_dir / "main.typ").exists() or any(paper_dir.rglob("*.typ")):
        return "typst"
    raise ValueError("no .tex or .typ source found")


def extract_headings(path: Path, text: str, engine: str) -> list[Heading]:
    headings: list[Heading] = []
    if engine == "latex":
        pattern = re.compile(
            r"\\(section|subsection|subsubsection)\*?\s*\{([^{}]+)\}"
        )
        levels = {"section": 1, "subsection": 2, "subsubsection": 3}
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            headings.append(Heading(levels[match.group(1)], match.group(2).strip(), path, line))
    else:
        for line_no, line in enumerate(text.splitlines(), 1):
            match = re.match(r"^\s*(=+)\s+(.+?)\s*$", line)
            if match:
                headings.append(Heading(len(match.group(1)), match.group(2).strip(), path, line_no))
    return headings


def normalized_title(title: str) -> str:
    title = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?", "", title)
    title = re.sub(r"[#*_`~{}\[\]（）()：:\s]", "", title)
    return title


def is_analysis_title(title: str) -> bool:
    title = normalized_title(title)
    return "问题分析" in title or "题目分析" in title


def is_assumptions_title(title: str) -> bool:
    title = normalized_title(title)
    return title in {"模型假设", "基本假设", "问题假设", "模型的假设"}


def question_tokens(number: int, raw_id: str) -> tuple[str, ...]:
    cn = chinese_number(number)
    return (f"问题{cn}", f"第{cn}问", f"问题{number}", f"Q{number}", raw_id)


def headings_inside_section(headings: list[Heading], index: int) -> list[Heading]:
    section = headings[index]
    result = []
    for heading in headings[index + 1 :]:
        if heading.level <= section.level:
            break
        result.append(heading)
    return result


def extract_latex_abstract(text: str) -> list[str]:
    blocks = []
    env = re.compile(
        r"\\begin\{(?:abstract|cnabstract|zhabstract)\}(.*?)"
        r"\\end\{(?:abstract|cnabstract|zhabstract)\}",
        re.S | re.I,
    )
    blocks.extend(match.group(1) for match in env.finditer(text))

    # Covers contest templates that put a literal abstract in a front-page macro.
    for marker in re.finditer(r"摘要\s*\}?", text):
        tail = text[marker.end() :]
        end = re.search(r"(?:关键词|关\s*键\s*词|\\newpage|\\clearpage)", tail)
        if end:
            candidate = tail[: end.start()]
            if len(re.sub(r"\\\w+|[{}\s]", "", candidate)) >= 40:
                blocks.append(candidate)
    return blocks


def extract_typst_abstract(text: str) -> list[str]:
    blocks = []
    for pattern in (
        r"(?s)#let\s+(?:abstract|summary)\s*=\s*\[(.*?)\]\s*\n",
        r"(?s)^=\s*摘要\s*$\n(.*?)(?=^=\s+|\Z)",
    ):
        blocks.extend(match.group(1) for match in re.finditer(pattern, text, re.M))
    return blocks


def clean_abstract(text: str, engine: str) -> str:
    if engine == "latex":
        text = re.sub(r"\\(?:begin|end)\{[^}]+\}", "\n", text)
        text = re.sub(r"\\(?:vspace|hspace)\*?\{[^}]*\}", "", text)
        text = re.sub(r"\\(?:noindent|par|centering|bfseries|heiti|songti)\b", "", text)
        text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?\{([^{}]*)\}", r"\1", text)
        text = text.replace("\\\\", "\n")
        text = text.replace("{", "").replace("}", "")
    else:
        text = re.sub(r"#\w+(?:\([^)]*\))?", "", text)
        text = text.replace("[", "").replace("]", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def paragraphs(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-dir", required=True, type=Path)
    parser.add_argument("--questions", nargs="+", required=True)
    parser.add_argument("--language", choices=("zh", "en"), default="zh")
    parser.add_argument("--engine", choices=("auto", "latex", "typst"), default="auto")
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    findings: list[tuple[str, str]] = []

    def report(level: str, message: str) -> None:
        findings.append((level, message))

    if not paper_dir.is_dir():
        report("FAIL", f"paper directory does not exist: {paper_dir}")
        engine = args.engine
        sources = []
    else:
        try:
            engine = detect_engine(paper_dir, args.engine)
        except ValueError as exc:
            report("FAIL", str(exc))
            engine = args.engine
            sources = []
        else:
            sources = read_sources(paper_dir, engine)
            if not sources:
                report("FAIL", f"no {engine} source files found")

    headings_by_file = {
        path: extract_headings(path, text, engine) for path, text in sources
    }
    all_headings = [heading for items in headings_by_file.values() for heading in items]

    analysis_sections = [h for h in all_headings if h.level == 1 and is_analysis_title(h.title)]
    if len(analysis_sections) != 1:
        report("FAIL", f"expected exactly one top-level problem-analysis section; found {len(analysis_sections)}")
    else:
        section = analysis_sections[0]
        file_headings = headings_by_file[section.path]
        index = file_headings.index(section)
        child_headings = headings_inside_section(file_headings, index)
        for fallback, raw_id in enumerate(args.questions, 1):
            number = question_number(raw_id, fallback)
            tokens = question_tokens(number, raw_id)
            matches = [
                h for h in child_headings
                if h.level >= 2
                and any(token.lower() in normalized_title(h.title).lower() for token in tokens)
                and "分析" in normalized_title(h.title)
            ]
            if matches:
                report("PASS", f"{raw_id}: independent analysis subsection found")
            else:
                report("FAIL", f"{raw_id}: missing independent analysis subsection under '{section.title}'")

    assumption_sections = [h for h in all_headings if h.level == 1 and is_assumptions_title(h.title)]
    if len(assumption_sections) == 1:
        report("PASS", "exactly one top-level model-assumptions section found")
    else:
        report("FAIL", f"expected exactly one top-level model-assumptions section; found {len(assumption_sections)}")

    scattered = [
        h for h in all_headings
        if h.level == 1 and "假设" in normalized_title(h.title) and not is_assumptions_title(h.title)
    ]
    if scattered:
        names = ", ".join(f"{h.title} ({h.path.name}:{h.line})" for h in scattered)
        report("FAIL", f"scattered top-level assumption sections found: {names}")

    if args.language == "zh":
        abstract_blocks: list[tuple[Path, str]] = []
        for path, text in sources:
            blocks = extract_latex_abstract(text) if engine == "latex" else extract_typst_abstract(text)
            if not blocks and "abstract" in path.stem.lower():
                blocks = [text]
            abstract_blocks.extend((path, block) for block in blocks)

        if not abstract_blocks:
            report("FAIL", "Chinese abstract source not found")
        else:
            path, block = max(abstract_blocks, key=lambda item: len(item[1]))
            abstract_paragraphs = paragraphs(clean_abstract(block, engine))
            assigned: dict[int, int] = {}
            for fallback, raw_id in enumerate(args.questions, 1):
                number = question_number(raw_id, fallback)
                tokens = question_tokens(number, raw_id)
                indexes = [
                    index for index, paragraph in enumerate(abstract_paragraphs)
                    if any(token.lower() in paragraph.lower() for token in tokens)
                ]
                if not indexes:
                    report("FAIL", f"{raw_id}: abstract paragraph not found")
                else:
                    assigned[number] = indexes[0]
            duplicate_paragraphs = {
                index for index in assigned.values() if list(assigned.values()).count(index) > 1
            }
            if duplicate_paragraphs:
                report("FAIL", "multiple questions are compressed into the same abstract paragraph")
            elif len(assigned) == len(args.questions):
                report("PASS", f"Chinese abstract has one distinct question paragraph per question ({path.name})")
            if len(abstract_paragraphs) < len(args.questions) + 1:
                report("FAIL", "Chinese abstract lacks a separate opening overview plus per-question paragraphs")

    for level, message in findings:
        print(f"[{level}] {message}")
    failures = sum(level == "FAIL" for level, _ in findings)
    warnings = sum(level == "WARN" for level, _ in findings)
    print(f"SUMMARY: engine={engine}, pass={sum(level == 'PASS' for level, _ in findings)}, warn={warnings}, fail={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
