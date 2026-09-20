"""Validate the original exercise answers and eight bundled lab handouts."""

import hashlib
import re
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COUNTS = [2, 54, 57, 44, 12, 21, 5, 8, 10, 5, 5, 15]
PACKAGES = {
    "datalab": "datalab-handout.tar",
    "bomblab": "bomb.tar",
    "attacklab": "target1.tar",
    "archlab": "archlab-handout.tar",
    "cachelab": "cachelab-handout.tar",
    "shlab": "shlab-handout.tar",
    "malloclab": "malloclab-handout.tar",
    "proxylab": "proxylab-handout.tar",
}


def main():
    for chapter, count in enumerate(COUNTS, 1):
        folders = list(ROOT.glob(f"第{chapter:02d}章-*"))
        if len(folders) != 1:
            raise SystemExit(f"Expected one directory for chapter {chapter}")
        path = folders[0] / "练习题答案.md"
        text = path.read_text(encoding="utf-8")
        actual = re.findall(r"^## 练习题 (\d+\.\d+)\s*$", text, re.M)
        expected = [f"{chapter}.{number}" for number in range(1, count + 1)]
        if actual != expected:
            raise SystemExit(f"Incorrect answer sequence: {path}")
        if text.count("```") % 2:
            raise SystemExit(f"Unbalanced code fences: {path}")

    labs = ROOT / "实验"
    manifest = (labs / "PACKAGES.md").read_text(encoding="utf-8")
    hashes = {path: digest for digest, path in re.findall(
        r"^([a-f0-9]{64})  (\S+)$", manifest, re.M
    )}
    if len(hashes) != len(PACKAGES):
        raise SystemExit("Expected eight archive checksums")
    for lab, archive in PACKAGES.items():
        folder = labs / f"{lab}-zh"
        text = (folder / f"{lab}-zh.md").read_text(encoding="utf-8")
        prose = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.M | re.S)
        if len(re.findall(r"^# ", prose, re.M)) != 1:
            raise SystemExit(f"Expected a single document title: {lab}")
        path = folder / archive
        if hashlib.sha256(path.read_bytes()).hexdigest() != hashes[path.relative_to(labs).as_posix()]:
            raise SystemExit(f"Archive checksum mismatch: {path}")
        with tarfile.open(path) as handle:
            if not handle.getmembers():
                raise SystemExit(f"Empty archive: {path}")
            # Read every payload without extracting or executing archive contents.
            for member in handle:
                if member.isfile():
                    with handle.extractfile(member) as payload:
                        if len(payload.read()) != member.size:
                            raise SystemExit(f"Truncated archive member: {member.name}")
    for path in labs.rglob("*"):
        if path.is_file() and path.suffix.lower() not in {".md", ".png", ".jpg", ".jpeg", ".tar"}:
            raise SystemExit(f"Unexpected lab document format: {path}")
    if any(path.name.lower() == "notes" for path in ROOT.rglob("*") if path.is_dir()):
        raise SystemExit("Personal notes must not be published")
    print(f"OK: {sum(COUNTS)} answers in 12 chapters; eight Markdown lab guides and verified archives")


if __name__ == "__main__":
    main()
