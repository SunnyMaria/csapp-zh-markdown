"""Build continuous chapter files from the standalone section Markdown."""

import os
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
LINK = re.compile(r"(!?\[[^\]\n]*\]\()(<[^>]+>|[^)\n]+)(\))")


def outside_fences(text, transform):
    result = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = FENCE.match(line)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            result.append(line)
        else:
            result.append(line if fence else transform(line))
    if fence is not None:
        raise ValueError("unclosed code fence")
    return "".join(result)


def heading_slug(title):
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"[`*_~]", "", title).strip().lower()
    chars = []
    for char in title:
        category = unicodedata.category(char)
        if char in (" ", "-") or category[0] in ("L", "N") or char == "_":
            chars.append(char)
    return "".join(chars).replace(" ", "-")


def section_links(index_text):
    match = re.search(
        r"^## 小节目录\s*$\n(?P<body>.*?)(?=^##\s|\Z)",
        index_text,
        flags=re.M | re.S,
    )
    if not match:
        raise ValueError("README.md has no section directory")
    return re.findall(r"^- \[[^\]]+\]\(([^)]+)\)", match.group("body"), re.M)


def section_level(title):
    number = re.match(r"(\d+(?:\.\d+)+)", title)
    return min(6, len(number.group(1).split(".")) + 1) if number else 2


def shift_headings(text, amount):
    def transform(line):
        match = re.match(r"^(#{1,6})(\s+)", line)
        if not match:
            return line
        level = min(6, max(1, len(match.group(1)) + amount))
        return "#" * level + line[len(match.group(1)) :]

    return outside_fences(text, transform)


def build_chapter(chapter):
    index_path = chapter / "README.md"
    index_text = index_path.read_text(encoding="utf-8-sig")
    title_match = re.match(r"^#\s+(.+)$", index_text, re.M)
    if not title_match:
        raise ValueError(f"missing chapter title: {index_path}")

    refs = section_links(index_text)
    sections = [(chapter / unquote(urlsplit(ref).path)).resolve() for ref in refs]
    metadata = []
    slug_counts = {}
    for path in sections:
        text = path.read_text(encoding="utf-8-sig").strip()
        heading = re.match(r"^(#{1,6})\s+(.+)$", text, re.M)
        if not heading:
            raise ValueError(f"missing section heading: {path}")
        section_title = heading.group(2).strip()
        base_slug = heading_slug(section_title)
        count = slug_counts.get(base_slug, 0)
        slug_counts[base_slug] = count + 1
        slug = f"{base_slug}-{count}" if count else base_slug
        metadata.append((path, text, heading.group(1), section_title, section_level(section_title), slug))

    anchors = {path: slug for path, _, _, _, _, slug in metadata}
    output_path = chapter / "chapter.md"

    def rebase(text, source):
        def replace(match):
            raw = match.group(2).strip("<>")
            parsed = urlsplit(raw)
            if parsed.scheme or raw.startswith(("#", "mailto:")):
                return match.group(0)
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if target in anchors:
                url = "#" + (parsed.fragment or anchors[target])
            else:
                url = os.path.relpath(target, chapter).replace("\\", "/")
                if parsed.fragment:
                    url += "#" + parsed.fragment
            return match.group(1) + url + match.group(3)

        return outside_fences(text, lambda line: LINK.sub(replace, line))

    nav_match = re.search(r"^\[[^\n]+(?: · \[[^\n]+)*$", index_text, re.M)
    navigation = nav_match.group(0) if nav_match else "[返回总目录](../README.md)"
    navigation = re.sub(r"\[整章阅读\]\(chapter\.md\)", "[按小节阅读](README.md)", navigation)
    if "[按小节阅读](README.md)" not in navigation:
        navigation += " · [按小节阅读](README.md)"

    toc = []
    chunks = []
    for path, text, original_marks, section_title, level, slug in metadata:
        toc.append("  " * (level - 2) + f"- [{section_title}](#{slug})")
        rebased = rebase(text, path)
        chunks.append(shift_headings(rebased, level - len(original_marks)))

    return (
        f"# {title_match.group(1)}\n\n"
        f"{navigation}\n\n"
        "## 本章目录\n\n"
        + "\n".join(toc)
        + "\n\n"
        + "\n\n".join(chunks)
        + f"\n\n---\n\n{navigation}\n"
    )


def main():
    built = 0
    for chapter in sorted(path for path in ROOT.iterdir() if path.is_dir()):
        index = chapter / "README.md"
        if not index.is_file() or "## 小节目录" not in index.read_text(encoding="utf-8-sig"):
            continue
        (chapter / "chapter.md").write_text(build_chapter(chapter), encoding="utf-8")
        built += 1
    print(f"OK: rebuilt {built} continuous chapter files")


if __name__ == "__main__":
    main()
