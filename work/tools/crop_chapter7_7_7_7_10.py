from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter7"
PAGES = CHAPTER / "pages"


CROPS = {
    CHAPTER / "7.8" / "assets" / "fig-7-13-typical-elf-executable.jpg": (
        519,
        (145, 350, 750, 695),
    ),
    CHAPTER / "7.9" / "assets" / "fig-7-15-linux-x86-64-runtime-memory-image.jpg": (
        521,
        (165, 250, 770, 720),
    ),
    CHAPTER / "7.10" / "assets" / "fig-7-16-dynamic-linking-shared-libraries.jpg": (
        522,
        (470, 430, 915, 875),
    ),
}


def main() -> None:
    for output, (page_number, box) in CROPS.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        source = PAGES / f"page-{page_number}.jpg"
        with Image.open(source) as page:
            crop = page.crop(box)
            crop.save(
                output,
                "JPEG",
                quality=95,
                subsampling=0,
                optimize=True,
            )
        print(f"{output.relative_to(ROOT)}: page {page_number}, box={box}")


if __name__ == "__main__":
    main()
