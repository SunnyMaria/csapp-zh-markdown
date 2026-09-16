from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("output/csapp-faithful/preface")
SECTIONS = ROOT / "sections"

EXPECTED_FILES = [
    "01-出版者的话.md",
    "02-中文版序一.md",
    "03-中文版序二.md",
    "04-译者序.md",
    "05-前言.md",
    "06-如何阅读此书.md",
    "07-本书概述.md",
    "08-本版新增内容.md",
    "09-本书的起源.md",
    "10-写给指导教师们-可以基于本书的课程.md",
    "11-写给指导教师们-经过课堂验证的实验练习.md",
    "12-第3版的致谢.md",
    "13-第2版的致谢.md",
    "14-第1版的致谢.md",
    "15-关于作者.md",
]

EXPECTED_HEADINGS = [
    "# 出版者的话",
    "# 中文版序一",
    "# 中文版序二",
    "# 译者序",
    "# 前言",
    "# 如何阅读此书",
    "# 本书概述",
    "# 本版新增内容",
    "# 本书的起源",
    "# 写给指导教师们：可以基于本书的课程",
    "# 写给指导教师们：经过课堂验证的实验练习",
    "# 第3版的致谢",
    "# 第2版的致谢",
    "# 第1版的致谢",
    "# 关于作者",
]

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    issues: list[str] = []
    md_files = sorted(SECTIONS.glob("*.md"))
    names = [path.name for path in md_files]

    if names != EXPECTED_FILES:
        issues.append(f"markdown files differ: {names}")

    combined = ""
    referenced_assets: set[Path] = set()
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text

        if text.count("```") % 2:
            issues.append(f"{path}: unbalanced code fences")

        for match in IMAGE_RE.finditer(text):
            target = (path.parent / match.group(1)).resolve()
            referenced_assets.add(target)
            if not target.is_file():
                issues.append(f"{path}: missing image {match.group(1)}")

    for heading in EXPECTED_HEADINGS:
        if combined.count(heading) != 1:
            issues.append(
                f"heading {heading!r}: expected once, found {combined.count(heading)}"
            )

    for marker in [
        "\\begin{",
        "\\end{",
        "卡内基斗",
        "OGR",
        "I / 0",
        "1 / 0",
        "JCS",
        "15-2I3",
        "练习题答案",
    ]:
        if marker in combined:
            issues.append(f"suspicious marker {marker!r}")

    required_fragments = [
        "**图 1** 一个典型的代码示例",
        "**图 2** 五类基于本书的课程",
        "| 12 | 并发编程 |",
        "```c",
        "preface-mei-hong.jpg",
        "preface-zang-binyu.jpg",
    ]
    for fragment in required_fragments:
        if fragment not in combined:
            issues.append(f"missing required fragment {fragment!r}")

    assets = sorted(path.resolve() for path in (ROOT / "assets").glob("*"))
    if len(assets) != 2:
        issues.append(f"assets: expected 2, found {len(assets)}")
    if set(assets) != referenced_assets:
        issues.append(
            "asset references differ: "
            f"assets={len(assets)}, referenced={len(referenced_assets)}"
        )

    page_images = sorted((ROOT / "pages").glob("page-*.png"))
    expected_pages = [f"page-{number:03d}.png" for number in range(5, 30)]
    if [path.name for path in page_images] != expected_pages:
        issues.append("page images must cover PDF pages 5-29 exactly")

    for path in ROOT.rglob("*"):
        if path.is_file() and any(
            marker in path.name.lower() for marker in ("preview", "contact", "tmp")
        ):
            issues.append(f"temporary file in output: {path}")

    if issues:
        print("\n".join(issues))
        return 1

    print(
        "OK: 15 markdown files; figures 1-2; "
        "2 retained photo assets; PDF pages 5-29"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
