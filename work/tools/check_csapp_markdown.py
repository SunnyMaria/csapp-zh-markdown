from __future__ import annotations

import argparse
import re
from pathlib import Path


OCR_HAZARDS = [
    "七",
    "曰",
    "芦",
    "豆日",
    "尸",
    "兀",
    "队",
    "叽",
    "少千",
    "涌洞",
    "范酣",
    "Cll",
    "DSE",
    "shor 七",
    "prin 七",
    "宇符",
    "巨m",
    "汒",
]

LATEX_HAZARDS = [
    r"\cdot",
    r"\sim",
    r"_{",
    r"^{",
]

MATHY_CODE_RE = re.compile(
    r"(```(?P<fence>.*?)```)|(`(?P<inline>[^`\n]*(?:\^|Σ|UMax|TMin|TMax|B2U|B2T|U2B|T2B|U2T|T2U|->|\{0)[^`\n]*)`)",
    re.S,
)


def image_refs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    for hazard in OCR_HAZARDS:
        for match in re.finditer(re.escape(hazard), text):
            line_no = text.count("\n", 0, match.start()) + 1
            issues.append(f"{path}:{line_no}: OCR hazard {hazard!r}")

    for hazard in LATEX_HAZARDS:
        for match in re.finditer(re.escape(hazard), text):
            line_no = text.count("\n", 0, match.start()) + 1
            issues.append(f"{path}:{line_no}: raw LaTeX marker {hazard!r}")

    for match in MATHY_CODE_RE.finditer(text):
        snippet = match.group("fence") or match.group("inline") or ""
        if "```" in match.group(0) and not any(token in snippet for token in ["Σ", "^", "UMax", "B2U", "TMin", "TMax", "->", "{0"]):
            continue
        line_no = text.count("\n", 0, match.start()) + 1
        shown = " ".join(snippet.strip().split())[:80]
        issues.append(f"{path}:{line_no}: math-like code formatting {shown!r}")

    for ref in image_refs(text):
        if not (path.parent / ref).exists():
            issues.append(f"{path}: missing image {ref}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    md_files: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            md_files.extend(sorted(path.glob("*.md")))
        else:
            md_files.append(path)

    issues: list[str] = []
    for path in md_files:
        issues.extend(check_file(path))

    if issues:
        print("\n".join(issues))
        return 1
    print(f"OK: checked {len(md_files)} markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
