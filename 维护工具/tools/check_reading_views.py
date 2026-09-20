"""Verify that every continuous chapter exactly matches its section sources."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_builder():
    script = Path(__file__).with_name("build_chapters.py")
    spec = importlib.util.spec_from_file_location("build_chapters", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_chapters(root=ROOT):
    builder = load_builder()
    count = 0
    chapters = sorted(root.glob("*/chapter.md"))
    if not chapters:
        raise AssertionError("no continuous chapter files found")
    for chapter_file in chapters:
        actual = chapter_file.read_text(encoding="utf-8-sig")
        expected = builder.build_chapter(chapter_file.parent)
        if actual != expected:
            raise AssertionError(f"stale continuous chapter: {chapter_file}")
        if '<a id="section-' in actual:
            raise AssertionError(f"raw section anchor in {chapter_file}")
        index = (chapter_file.parent / "README.md").read_text(encoding="utf-8-sig")
        count += len(builder.section_links(index))
    return count


def main():
    count = check_chapters()
    if count != 444:
        raise AssertionError(f"expected 444 standalone sections including appendix A, found {count}")
    print(f"OK: {count} standalone sections exactly match their continuous chapters")


if __name__ == "__main__":
    main()
