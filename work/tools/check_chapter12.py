from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("output/csapp-faithful/chapter12")
EXPECTED_MARKDOWN_FILES = 36
EXPECTED_ASSETS = 17
CONTENT_DIRS = [ROOT / f"12.{number}" for number in range(1, 9)] + [
    ROOT / "homework"
]


def count_label(text: str, label: str, number: int) -> int:
    pattern = rf"\*\*{re.escape(label)} 12\.{number}(?!\d)"
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


def required_headings() -> list[str]:
    return [
        "12.1",
        "12.1.1",
        "12.1.2",
        "12.2",
        "12.2.1",
        "12.2.2",
        "12.3",
        *[f"12.3.{number}" for number in range(1, 9)],
        "12.4",
        *[f"12.4.{number}" for number in range(1, 4)],
        "12.5",
        *[f"12.5.{number}" for number in range(1, 6)],
        "12.6",
        "12.7",
        *[f"12.7.{number}" for number in range(1, 6)],
        "12.8",
    ]


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

    if len(files) != EXPECTED_MARKDOWN_FILES:
        issues.append(
            f"markdown files: expected {EXPECTED_MARKDOWN_FILES}, "
            f"found {len(files)}"
        )

    for path in files:
        if path.stat().st_size == 0:
            issues.append(f"{path}: empty markdown file")

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
            "笫 12",
            "对千",
            "关千",
            "源千",
            "基千",
            "变扯",
            "变鼠",
            "捕荻",
            "l/0",
            "1/0",
            "I / 0",
            "P 七 hread",
            "Pthread crea",
            "selec 七",
            "ech o",
            "巳连接",
            "TODO",
            "TBD",
            "\ufffd",
        ]:
            if marker in text:
                issues.append(f"{path}: suspicious marker {marker!r}")

    all_text = "\n".join(all_text_parts)

    for number in range(1, 16):
        count = count_label(all_text, "练习题", number)
        if count != 1:
            issues.append(f"练习题 12.{number}: expected once, found {count}")

    for number in range(16, 40):
        count = count_label(all_text, "家庭作业", number)
        if count != 1:
            issues.append(f"家庭作业 12.{number}: expected once, found {count}")

    for number in range(1, 48):
        caption = rf"^\s*(?:>\s*)?\*\*图 12-{number}\*\*"
        count = len(re.findall(caption, all_text, re.MULTILINE))
        if count != 1:
            issues.append(f"图 12-{number}: expected one caption, found {count}")

    for heading in required_headings():
        if not re.search(
            rf"^# {re.escape(heading)}(?:\s|$)", all_text, re.MULTILINE
        ):
            issues.append(f"heading {heading}: missing")

    if not re.search(r"^# 第 12 章 并发编程(?:\s|$)", all_text, re.MULTILINE):
        issues.append("heading 第 12 章 并发编程: missing")

    if not re.search(r"^# 参考文献说明(?:\s|$)", all_text, re.MULTILINE):
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

    assets: list[Path] = []
    for assets_dir in [directory / "assets" for directory in CONTENT_DIRS]:
        if not assets_dir.exists():
            continue
        for asset in assets_dir.iterdir():
            assets.append(asset)
            if asset.is_file() and asset.resolve() not in referenced_assets:
                issues.append(f"{asset}: unreferenced asset")
            if "contact" in asset.name.lower() or "preview" in asset.name.lower():
                issues.append(f"{asset}: temporary image")

    if len(assets) != EXPECTED_ASSETS:
        issues.append(
            f"assets: expected {EXPECTED_ASSETS}, found {len(assets)}"
        )

    if len(referenced_assets) != EXPECTED_ASSETS:
        issues.append(
            f"referenced assets: expected {EXPECTED_ASSETS}, "
            f"found {len(referenced_assets)}"
        )

    page_images = sorted((ROOT / "pages").glob("page-*.png"))
    if len(page_images) != 46:
        issues.append(f"page images: expected 46, found {len(page_images)}")
    if (ROOT / "source-text").exists():
        issues.append(f"{ROOT / 'source-text'}: temporary OCR directory remains")

    if issues:
        print("\n".join(issues))
        return 1

    print(
        "OK: "
        f"{len(files)} markdown files; "
        "exercises 12.1-12.15; homework 12.16-12.39; figures 12-1-12-47"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
