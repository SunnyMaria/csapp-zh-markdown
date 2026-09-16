from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("output/csapp-faithful/chapter1")
EXPECTED_MARKDOWN_FILES = 21
EXPECTED_ASSETS = 16
CONTENT_DIRS = [ROOT / f"1.{number}" for number in range(1, 11)]


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
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.4.1",
        "1.4.2",
        "1.5",
        "1.6",
        "1.7",
        "1.7.1",
        "1.7.2",
        "1.7.3",
        "1.7.4",
        "1.8",
        "1.9",
        "1.9.1",
        "1.9.2",
        "1.9.3",
        "1.10",
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
        text = path.read_text(encoding="utf-8")
        all_text_parts.append(text)
        lines = text.splitlines()
        if not text.strip():
            issues.append(f"{path}: empty markdown file")

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
            "笫 1",
            "对千",
            "关千",
            "源千",
            "基千",
            "深人",
            "变扯",
            "I / 0",
            "l/0",
            "井发",
            "存贮",
            "TODO",
            "TBD",
            "\ufffd",
        ]:
            if marker in text:
                issues.append(f"{path}: suspicious marker {marker!r}")

    all_text = "\n".join(all_text_parts)

    for number in range(1, 3):
        pattern = rf"\*\*练习题 1\.{number}(?!\d)"
        count = len(re.findall(pattern, all_text))
        if count != 1:
            issues.append(f"练习题 1.{number}: expected once, found {count}")

    for number in range(1, 19):
        caption = rf"^\s*(?:>\s*)?\*\*图 1-{number}\*\*"
        count = len(re.findall(caption, all_text, re.MULTILINE))
        if count != 1:
            issues.append(f"图 1-{number}: expected one caption, found {count}")

    for heading in required_headings():
        if not re.search(
            rf"^# {re.escape(heading)}(?:\s|$)", all_text, re.MULTILINE
        ):
            issues.append(f"heading {heading}: missing")

    if not re.search(
        r"^# 第 1 章 计算机系统漫游(?:\s|$)", all_text, re.MULTILINE
    ):
        issues.append("heading 第 1 章 计算机系统漫游: missing")
    if not re.search(r"^# 参考文献说明(?:\s|$)", all_text, re.MULTILINE):
        issues.append("heading 参考文献说明: missing")
    if "练习题答案" in all_text:
        issues.append("exercise-answer section must not be included")
    if "家庭作业" in all_text:
        issues.append("chapter 1 has no homework section")

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
    if len(page_images) != 20:
        issues.append(f"page images: expected 20, found {len(page_images)}")
    for path in (ROOT / "pages").glob("*.png"):
        if "preview" in path.name.lower() or "contact" in path.name.lower():
            issues.append(f"{path}: temporary image")

    if issues:
        print("\n".join(issues))
        return 1

    print(
        "OK: 21 markdown files; exercises 1.1-1.2; "
        f"figures 1-1-1-18; {EXPECTED_ASSETS} retained assets"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
