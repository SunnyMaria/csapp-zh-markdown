"""One-time assembly of the v1 reading folder from the archived workspace."""

import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote

from check_release import references, check


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "work"
DEST = ROOT / "docs"


def natural(path):
    return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", path.as_posix())]


def copy_document(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    for ref in references(source.read_text(encoding="utf-8")):
        if ref.startswith(("http://", "https://", "#", "mailto:")):
            continue
        relative = unquote(urlsplit(ref).path)
        asset = (source.parent / relative).resolve()
        target = (destination.parent / relative).resolve()
        if not asset.is_relative_to(WORK) or not target.is_relative_to(DEST):
            raise ValueError(f"Unexpected dependency: {source}: {ref}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, target)


def index(folder, title, files, preserve_order=False):
    lines = [f"# {title}", ""]
    ordered = files if preserve_order else sorted(files, key=lambda p: natural(p.relative_to(folder)))
    for path in ordered:
        text = path.read_text(encoding="utf-8-sig")
        heading = re.search(r"^#{1,6}\s+(.+)$", text, re.M)
        label = heading.group(1) if heading else path.stem
        label = label.replace("[", "\\[").replace("]", "\\]")
        lines.append(f"- [{label}]({quote(path.relative_to(folder).as_posix())})")
    (folder / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if DEST.exists():
        raise SystemExit("docs already exists; edit it directly. Refusing to overwrite.")
    book = WORK / "output/csapp-faithful"
    groups = ["preface"] + [f"chapter{n}" for n in range(1, 13)]
    for group in groups:
        files = []
        for source in (book / group).rglob("*.md"):
            if {"drafts", "pages", "source-text"} & set(source.relative_to(book).parts):
                continue
            destination = DEST / "book" / source.relative_to(book)
            copy_document(source, destination)
            files.append(destination)
        index(DEST / "book" / group, "序章" if group == "preface" else f"第 {group[7:]} 章", files)
    index(DEST / "book", "正文目录", [DEST / "book" / g / "README.md" for g in groups], preserve_order=True)
    labs = []
    for name in ["attacklab-zh", "archlab-zh", "cachelab-zh"]:
        for source in (WORK / "output" / name).glob("*.md"):
            destination = DEST / "labs" / name / source.name
            copy_document(source, destination)
            labs.append(destination)
    index(DEST / "labs", "实验资料", labs)
    (DEST / "README.md").write_text(
        "# CSAPP 1.0 阅读目录\n\n"
        "- [序章与第 1—12 章](book/README.md)\n"
        "- [实验资料](labs/README.md)\n\n"
        "本目录可整体复制或下载，图片和附件均在目录内。请使用 Markdown 阅读器打开，并保留内部文件结构。\n",
        encoding="utf-8",
    )
    check(DEST)


if __name__ == "__main__":
    main()
