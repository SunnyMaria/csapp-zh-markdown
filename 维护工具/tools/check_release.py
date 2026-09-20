"""Check a standalone Markdown release using only the standard library."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def anchors(text):
    text = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text, flags=re.M | re.S)
    found = set(re.findall(r'<a\b[^>]*\bid=["\']([^"\']+)', text))
    counts = {}
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(f"{slug}-{count}" if count else slug)
    return found


def references(text):
    # Ignore examples in fenced blocks before examining actual document links.
    text = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text, flags=re.M | re.S)
    for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)", text):
        yield match.group(1).strip().strip("<>")
    for match in re.finditer(r'^\[(?!\^)[^\]]+\]:\s*(\S+)', text, re.M):
        yield match.group(1).strip("<>")
    for match in re.finditer(r'<(?:img|a)\b[^>]*?\b(?:src|href)=["\']([^"\']+)', text, re.I):
        yield match.group(1)


def check(root):
    root = root.resolve()
    issues = []
    files = list(root.rglob("*.md"))
    local_links = 0
    targets = set()
    anchor_cache = {}
    for path in files:
        for ref in references(path.read_text(encoding="utf-8")):
            if ref.startswith(("https://", "http://", "mailto:")):
                continue
            if "\\" in ref or ref.startswith("/") or re.match(r"^[A-Za-z][\w+.-]*:", ref):
                issues.append(f"{path}: non-portable path {ref}")
                continue
            parsed = urlsplit(ref)
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not target.is_relative_to(root):
                issues.append(f"{path}: dependency outside reading root: {ref}")
                continue
            local_links += 1
            targets.add(target)
            if not target.is_file():
                issues.append(f"{path}: missing file {ref}")
                continue
            if parsed.fragment and target.suffix == ".md":
                if target not in anchor_cache:
                    anchor_cache[target] = anchors(target.read_text(encoding="utf-8-sig"))
                if unquote(parsed.fragment) not in anchor_cache[target]:
                    issues.append(f"{path}: missing anchor {ref}")
            # Windows accepts wrong case; check every component for Linux hosts.
            current = root
            for part in target.relative_to(root).parts:
                if part not in {item.name for item in current.iterdir()}:
                    issues.append(f"{path}: incorrect path case: {ref}")
                    break
                current /= part
    if not files or not (root / "README.md").is_file():
        issues.append("Missing release README or Markdown content")
    for path in files:
        if path.name != "README.md" and path.resolve() not in targets:
            issues.append(f"Not linked from reading index: {path}")
    if issues:
        raise SystemExit("\n".join(issues))
    print(f"OK: {len(files)} Markdown files, {local_links} local links; paths, case and anchors checked")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    check(parser.parse_args().directory)
