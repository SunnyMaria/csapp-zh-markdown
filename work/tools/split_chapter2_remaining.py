from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "output" / "CSAPP-3th-ZH-OCR-chapter2-readable.md"
OUT_ROOT = ROOT / "output" / "csapp-faithful" / "chapter2"


SLUGS = {
    "2.2": "integer-representations",
    "2.2.1": "integer-data-types",
    "2.2.2": "unsigned-encodings",
    "2.2.3": "twos-complement-encodings",
    "2.2.4": "conversions-between-signed-and-unsigned",
    "2.2.5": "signed-versus-unsigned-in-c",
    "2.2.6": "expanding-bit-representations",
    "2.2.7": "truncating-numbers",
    "2.2.8": "advice-on-signed-versus-unsigned",
    "2.3": "integer-arithmetic",
    "2.3.1": "unsigned-addition",
    "2.3.2": "twos-complement-addition",
    "2.3.3": "twos-complement-negation",
    "2.3.4": "unsigned-multiplication",
    "2.3.5": "twos-complement-multiplication",
    "2.3.6": "multiplying-by-constants",
    "2.3.7": "dividing-by-powers-of-two",
    "2.3.8": "final-thoughts-on-integer-arithmetic",
    "2.4": "floating-point",
    "2.4.1": "binary-fractions",
    "2.4.2": "ieee-floating-point-representation",
    "2.4.3": "numeric-examples",
    "2.4.4": "rounding",
    "2.4.5": "floating-point-operations",
    "2.4.6": "floating-point-in-c",
    "2.5": "summary",
}


COMMON_REPLACEMENTS = [
    ("Ox", "0x"),
    ("Oxl", "0x1"),
    ("Oll", "011"),
    ("OO", "00"),
    (" Cll", " C11"),
    ("Cll", "C11"),
    ("I SO", "ISO"),
    ("I SO", "ISO"),
    ("ANS I", "ANSI"),
    ("C+ ＋", "C++"),
    ("C + ＋", "C++"),
    ("次幕", "次幂"),
    ("于 4 位", "于 4 位"),
    ("少千", "少于"),
    ("涌洞", "漏洞"),
    ("范酣", "范围"),
]


def clean(text: str) -> str:
    for old, new in COMMON_REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def title_to_filename(section: str, title: str) -> str:
    slug = SLUGS.get(section, re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"))
    return f"{section}-{slug}.md"


def split_sections(markdown: str) -> list[tuple[str, str, str]]:
    heading = re.compile(r"^(##|###) (2\.(?:[2-5](?:\.\d+)?)?) (.+)$", re.M)
    matches = list(heading.finditer(markdown))
    result: list[tuple[str, str, str]] = []
    for i, match in enumerate(matches):
        section = match.group(2)
        if not (section == "2.5" or section.startswith(("2.2", "2.3", "2.4"))):
            continue
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        # Stop before end-of-chapter reference/homework material when splitting 2.5.
        body = markdown[start:end]
        if section == "2.5":
            cut = re.search(r"\n参考文献说明|\n家庭作业", body)
            if cut:
                body = body[: cut.start()]
        title = match.group(3).strip()
        result.append((section, title, clean(body)))
    return result


def main() -> None:
    markdown = SRC.read_text(encoding="utf-8")
    for section, title, body in split_sections(markdown):
        top = ".".join(section.split(".")[:2])
        out_dir = OUT_ROOT / top
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / title_to_filename(section, title)
        out.write_text(body, encoding="utf-8")
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
