from __future__ import annotations

import re
import struct
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "archlab-zh"


EXPECTED = {
    "simguide-zh.md": {
        "headings": [
            "## 1 安装",
            "## 2 实用程序",
            "## 3 处理器模拟器",
            "### 3.1 模拟器命令行选项",
            "### 3.2 SEQ 模拟器的 GUI 版本",
            "### 3.3 PIPE 模拟器",
            "## 4 一些建议",
        ],
        "tokens": [
            "linux> ./ssim+ -t < ../y86-code/asum.yo",
            "linux> ./ssim -g ../y86-code/asum.yo &",
            "0x0FFF",
            "0xd000d000d",
            "0x020",
            "0x03",
            "0x01f0",
            "0x01f8",
            "R[d_srcA]",
            "R[d_srcB]",
            "D_valP",
            "e_valE",
            "M_valE",
            "m_valM",
            "W_valE",
            "W_valM",
            "BUB",
            "PIP",
        ],
        "images": [
            "simguide-assets/pipeline-overview.png",
            "simguide-assets/figure-2-seq-control-panel.png",
            "simguide-assets/figure-3-seq-code-window.png",
            "simguide-assets/figure-4-seq-memory-window.png",
            "simguide-assets/figure-5-pipe-control-panel.png",
            "simguide-assets/figure-6-pipeline-register.png",
            "simguide-assets/figure-7-pipe-code-window.png",
        ],
    },
    "archlab-zh.md": {
        "headings": [
            "## 1 引言",
            "## 2 实验安排",
            "## 3 实验材料说明",
            "## 4 Part A",
            "## 5 Part B",
            "## 6 Part C",
            "## 7 评分",
            "## 8 提交说明",
            "## 9 提示",
        ],
        "tokens": [
            "result ^= val;",
            "unix> make VERSION=full",
            "unix> ./ssim -t ../y86-code/asumi.yo",
            "unix> (cd ../ptest; make SIM=../seq/ssim TFLAGS=-i)",
            "unix> ./check-len.pl < ncopy.yo",
            "irmovq $1, %r10",
            "irmovq $8, %r10",
            "unix> ./gen-driver.pl -f ncopy.ys -n K -rc > driver.ys",
            "0xaaaa",
            "0xbbbb",
            "0xcccc",
            "0xdddd",
            "0xeeee",
            "897/63 = 14.24",
            "29.00",
            "14.27",
            "15.18",
            "7.48",
            "20 * (10.5 - c)",
            "unix> make handin-partX TEAM=teamname VERSION=2",
        ],
        "images": [],
    },
}


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])


def check_document(name: str, expected: dict[str, list[str]]) -> list[str]:
    path = OUTPUT / name
    issues: list[str] = []
    if not path.exists():
        return [f"missing document: {path}"]

    text = path.read_text(encoding="utf-8")
    if "\ufffd" in text:
        issues.append(f"{name}: replacement character found")
    bad_controls = sorted(
        {
            f"U+{ord(char):04X}"
            for char in text
            if unicodedata.category(char).startswith("C") and char not in "\n\r\t"
        }
    )
    if bad_controls:
        issues.append(f"{name}: unexpected Unicode controls {bad_controls!r}")
    if "PDF PAGE" in text:
        issues.append(f"{name}: raw extraction page marker found")
    if text.count("```") % 2:
        issues.append(f"{name}: unbalanced fenced code blocks")

    for heading in expected["headings"]:
        if heading not in text:
            issues.append(f"{name}: missing heading {heading!r}")
    for token in expected["tokens"]:
        if token not in text:
            issues.append(f"{name}: missing technical token {token!r}")

    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    if refs != expected["images"]:
        issues.append(f"{name}: image reference order/count differs: {refs!r}")
    for ref in refs:
        image_path = path.parent / ref
        if not image_path.exists():
            issues.append(f"{name}: missing image {ref}")
            continue
        try:
            width, height = png_dimensions(image_path)
        except ValueError as exc:
            issues.append(f"{name}: invalid image {ref}: {exc}")
            continue
        if width < 500 or height < 300:
            issues.append(f"{name}: suspiciously small crop {ref}: {width}x{height}")

    return issues


def main() -> int:
    issues: list[str] = []
    for name, expected in EXPECTED.items():
        issues.extend(check_document(name, expected))

    if issues:
        print("\n".join(issues))
        return 1
    print("OK: checked 2 translated Markdown documents and 7 image assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
