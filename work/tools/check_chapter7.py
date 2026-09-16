from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("output/csapp-faithful/chapter7")
CONTENT_DIRS = [ROOT / f"7.{number}" for number in range(1, 16)] + [
    ROOT / "homework"
]


def count_label(text: str, label: str, number: int) -> int:
    pattern = rf"\*\*{re.escape(label)} 7\.{number}(?!\d)"
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
        for directory in CONTENT_DIRS
        if directory.exists()
        for path in directory.rglob("*.md")
    )
    issues: list[str] = []
    all_text_parts: list[str] = []
    referenced_assets: set[Path] = set()

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
            asset = (path.parent / ref).resolve()
            referenced_assets.add(asset)
            if not asset.exists():
                issues.append(f"{path}: missing image {ref}")

        for marker in [
            "锟",
            "閿",
            "鐑",
            r"\cdot",
            r"\sim",
            r"\frac",
            r"\mathrm",
            "$$",
            "笫 7 章",
            "对千",
            "关千",
            "源千",
            "Ox0",
            "Ox4",
            ".te 江",
            ".te江",
            "dl sym",
            "变最",
        ]:
            if marker in text:
                issues.append(f"{path}: suspicious marker {marker!r}")

    all_text = "\n".join(all_text_parts)

    for number in range(1, 6):
        count = count_label(all_text, "练习题", number)
        if count != 1:
            issues.append(f"练习题 7.{number}: expected once, found {count}")

    for number in range(6, 14):
        count = count_label(all_text, "家庭作业", number)
        if count != 1:
            issues.append(f"家庭作业 7.{number}: expected once, found {count}")

    for number in range(1, 23):
        caption = rf"^\s*(?:>\s*)?\*\*图 7-{number}\*\*"
        count = len(re.findall(caption, all_text, re.MULTILINE))
        if count != 1:
            issues.append(f"图 7-{number}: expected one caption, found {count}")

    required_headings = [
        "7.1",
        "7.2",
        "7.3",
        "7.4",
        "7.5",
        "7.6",
        "7.6.1",
        "7.6.2",
        "7.6.3",
        "7.7",
        "7.7.1",
        "7.7.2",
        "7.8",
        "7.9",
        "7.10",
        "7.11",
        "7.12",
        "7.13",
        "7.13.1",
        "7.13.2",
        "7.13.3",
        "7.14",
        "7.15",
    ]
    for heading in required_headings:
        if not re.search(
            rf"^# {re.escape(heading)}(?:\s|$)", all_text, re.MULTILINE
        ):
            issues.append(f"heading {heading}: missing")

    if not re.search(r"^# 参考文献说明", all_text, re.MULTILINE):
        issues.append("heading 参考文献说明: missing")

    if re.search(r"练习题答案", all_text):
        issues.append("exercise-answer section must not be included")

    for tag in ["sub", "sup"]:
        opens = all_text.count(f"<{tag}>")
        closes = all_text.count(f"</{tag}>")
        if opens != closes:
            issues.append(
                f"<{tag}> tags are unbalanced: {opens} opening, {closes} closing"
            )

    for assets_dir in [directory / "assets" for directory in CONTENT_DIRS]:
        if not assets_dir.exists():
            continue
        for asset in assets_dir.iterdir():
            if asset.is_file() and asset.resolve() not in referenced_assets:
                issues.append(f"{asset}: unreferenced asset")
            if "contact" in asset.name.lower():
                issues.append(f"{asset}: temporary contact sheet")

    if issues:
        print("\n".join(issues))
        return 1

    print(
        "OK: "
        f"{len(files)} markdown files; "
        "exercises 7.1-7.5; homework 7.6-7.13; figures 7-1-7-22"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
