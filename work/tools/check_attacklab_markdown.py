from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageStat


EXPECTED_HEADINGS = [
    "## 1 引言",
    "## 2 实验安排",
    "### 2.1 获取文件",
    "### 2.2 重要事项",
    "## 3 目标程序",
    "## 4 第一部分：代码注入攻击",
    "### 4.1 第 1 级",
    "### 4.2 第 2 级",
    "### 4.3 第 3 级",
    "## 5 第二部分：面向返回编程",
    "### 5.1 第 2 级",
    "### 5.2 第 3 级",
    "## 附录 A 使用 HEX2RAW",
    "## 附录 B 生成字节码",
    "## 参考文献",
]

REQUIRED_TEXT = [
    "$Attacklab::SERVER_NAME",
    "targetk.tar",
    "tar -xvf targetk.tar",
    "BUFFER_SIZE",
    "0x0a",
    "0xdeadbeef",
    "ef be ad de",
    "ctarget.l2.txt",
    "3347663060U",
    "48 89 c7",
    "0x400f18",
    "start_farm",
    "mid_farm",
    "end_farm",
    "0xc3",
    "0x90",
    "example.s",
    "example.d",
    "ACM Transactions on Information System Security",
    "USENIX Security Symposium",
]


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors = []

    headings = re.findall(r"(?m)^#{2,3} .+$", text)
    if headings != EXPECTED_HEADINGS:
        errors.append("heading order/content differs from the 15-section checklist")

    missing = [token for token in REQUIRED_TEXT if token not in text]
    if missing:
        errors.append("missing required text: " + ", ".join(missing))

    fence_count = len(re.findall(r"(?m)^```", text))
    if fence_count % 2:
        errors.append(f"unpaired code fences: {fence_count}")

    if "\ufffd" in text:
        errors.append("UTF-8 replacement character found")

    raw_latex = re.findall(r"\\cdot|\\sim|_\{|\^\{", text)
    if raw_latex:
        errors.append("raw LaTeX markers found: " + ", ".join(sorted(set(raw_latex))))

    image_refs = re.findall(r"!\[[^]]*\]\(([^)]+)\)", text)
    if len(image_refs) != 2:
        errors.append(f"expected 2 image references, found {len(image_refs)}")
    image_results = []
    for ref in image_refs:
        image_path = path.parent / ref
        if not image_path.is_file():
            errors.append(f"missing image: {ref}")
            continue
        with Image.open(image_path) as image:
            grayscale = image.convert("L")
            variance = sum(ImageStat.Stat(grayscale).var)
            image_results.append(f"{ref}={image.width}x{image.height},variance={variance:.1f}")
            if image.width < 1200 or image.height < 600 or variance < 100:
                errors.append(f"image is too small or nearly blank: {ref}")

    if not text.rstrip().endswith("2011 年。"):
        errors.append("document does not end with reference [2]")

    print(f"headings={len(headings)} fences={fence_count} images={len(image_refs)}")
    for result in image_results:
        print(result)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("OK: Attack Lab Markdown completeness checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
