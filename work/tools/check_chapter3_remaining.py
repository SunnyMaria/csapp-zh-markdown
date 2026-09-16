from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("output/csapp-faithful/chapter3")
SECTION_DIRS = [
    ROOT / "3.6",
    ROOT / "3.7",
    ROOT / "3.8",
    ROOT / "3.9",
    ROOT / "3.10",
    ROOT / "3.11",
    ROOT / "3.12",
    ROOT / "homework",
]


def count_label(text: str, label: str, number: int) -> int:
    pattern = rf"\*\*{re.escape(label)} 3\.{number}(?!\d)"
    return len(re.findall(pattern, text))


def markdown_table_issues(path: Path, lines: list[str]) -> list[str]:
    issues: list[str] = []
    in_table = False
    expected_cells = 0

    for line_no, line in enumerate(lines, start=1):
        if re.match(r"^\s*(?:>\s*)?\|.*\|\s*$", line):
            cells = len(re.findall(r"(?<!\\)\|", line)) - 1
            if not in_table:
                in_table = True
                expected_cells = cells
            elif cells != expected_cells:
                issues.append(
                    f"{path}:{line_no}: table has {cells} cells, "
                    f"expected {expected_cells}"
                )
        else:
            in_table = False
            expected_cells = 0

    return issues


def main() -> int:
    files = sorted(
        path
        for directory in SECTION_DIRS
        if directory.exists()
        for path in directory.rglob("*.md")
    )
    issues: list[str] = []
    all_text_parts: list[str] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        all_text_parts.append(text)

        fence_count = sum(
            1 for line in lines if re.match(r"^\s*(?:>\s*)?```", line)
        )
        if fence_count % 2:
            issues.append(f"{path}: unbalanced code fences ({fence_count})")

        issues.extend(markdown_table_issues(path, lines))

        for ref in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
            if not (path.parent / ref).exists():
                issues.append(f"{path}: missing image {ref}")

        for marker in ["�", "锟", "烫", r"\cdot", r"\sim", "$$"]:
            if marker in text:
                issues.append(f"{path}: suspicious marker {marker!r}")

    all_text = "\n".join(all_text_parts)

    for number in range(13, 58):
        count = count_label(all_text, "练习题", number)
        if count != 1:
            issues.append(f"练习题 3.{number}: expected once, found {count}")

    for number in range(58, 76):
        count = count_label(all_text, "家庭作业", number)
        if count != 1:
            issues.append(f"家庭作业 3.{number}: expected once, found {count}")

    for number in range(13, 55):
        if not re.search(rf"图 3-{number}(?!\d)", all_text):
            issues.append(f"图 3-{number}: missing")

    if re.search(r"^#.*练习题答案", all_text, flags=re.MULTILINE):
        issues.append("exercise-answer section must not be included")

    for tag in ["sub", "sup"]:
        opens = all_text.count(f"<{tag}>")
        closes = all_text.count(f"</{tag}>")
        if opens != closes:
            issues.append(
                f"<{tag}> tags are unbalanced: {opens} opening, {closes} closing"
            )

    if issues:
        print("\n".join(issues))
        return 1

    print(
        "OK: "
        f"{len(files)} markdown files; "
        "exercises 3.13-3.57; homework 3.58-3.75; figures 3-13-3-54"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
