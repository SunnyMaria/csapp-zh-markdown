from __future__ import annotations

import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / "output" / "cachelab-zh" / "cachelab-zh.md"

HEADINGS = [
    "## 1 实验安排",
    "## 2 概述",
    "## 3 下载实验材料",
    "## 4 实验说明",
    "### 4.1 参考跟踪文件",
    "### 4.2 Part A：编写缓存模拟器",
    "### 4.3 Part B：优化矩阵转置",
    "## 5 评分",
    "### 5.1 Part A 的评分",
    "### 5.2 Part B 的评分",
    "#### 5.2.1 性能（26 分）",
    "### 5.3 代码风格评分",
    "## 6 开展实验",
    "### 6.1 开展 Part A",
    "### 6.2 开展 Part B",
    "### 6.3 综合测试",
    "## 7 提交实验",
]

TOKENS = [
    "linux> tar xvf cachelab-handout.tar",
    "linux> valgrind --log-fd=1 --tool=lackey -v --trace-mem=yes ls -l",
    "I 0400d7d4,8",
    " M 0421c7f0,4",
    "[space]operation address,size",
    "Usage: ./csim-ref [-hv] -s <s> -E <E> -b <b> -t <tracefile>",
    "S = 2<sup>s</sup>",
    "B = 2<sup>b</sup>",
    "hits:4 misses:5 evictions:3",
    "M 12,1 miss eviction hit",
    "printSummary(hit_count, miss_count, eviction_count);",
    'char transpose_submit_desc[] = "Transpose submission";',
    "void transpose_submit(int M, int N, int A[N][M], int B[M][N]);",
    "linux> ./csim -s 5 -E 1 -b 5 -t traces/long.trace",
    "265189",
    "21775",
    "21743",
    "m < 1,300",
    "m > 2,000",
    "m < 2,000",
    "m > 3,000",
    "#include <getopt.h>",
    "registerTransFunction(transpose_submit, transpose_submit_desc);",
    "func 0 (Transpose submission): hits:1766, misses:287, evictions:255",
    "func 3 (using a zig-zag access pattern): hits:1076, misses:977, evictions:945",
    "Summary for official submission (func 0): correctness=1 misses=287",
    "linux> ./csim-ref -v -s 5 -E 1 -b 5 -t trace.f0",
    "linux> ./driver.py",
    "userid-handin.tar",
    "[^1]:",
    "[^2]:",
]


def main() -> int:
    issues: list[str] = []
    if not DOCUMENT.exists():
        print(f"missing document: {DOCUMENT}")
        return 1

    text = DOCUMENT.read_text(encoding="utf-8")

    for heading in HEADINGS:
        if heading not in text:
            issues.append(f"missing heading: {heading}")
    for token in TOKENS:
        if token not in text:
            issues.append(f"missing technical token: {token}")

    test_commands = re.findall(r"^linux> \./csim -s ", text, flags=re.MULTILINE)
    if len(test_commands) != 8:
        issues.append(f"expected 8 Part A csim tests, found {len(test_commands)}")

    if text.count("```") % 2:
        issues.append("unbalanced fenced code blocks")
    if re.search(r"!\[[^\]]*\]\([^)]+\)", text):
        issues.append("unexpected image reference")
    if "PDF PAGE" in text:
        issues.append("raw PDF page marker found")
    if "\ufffd" in text:
        issues.append("Unicode replacement character found")

    bad_controls = sorted(
        {
            f"U+{ord(char):04X}"
            for char in text
            if unicodedata.category(char).startswith("C") and char not in "\n\r\t"
        }
    )
    if bad_controls:
        issues.append(f"unexpected Unicode controls: {bad_controls}")

    if issues:
        print("\n".join(issues))
        return 1
    print("OK: checked complete Cache Lab Markdown structure and technical content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
