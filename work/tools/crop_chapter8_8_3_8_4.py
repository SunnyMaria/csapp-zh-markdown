from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter8"
PAGES = CHAPTER / "pages"
ASSETS = CHAPTER / "8.4" / "assets"


CROPS = {
    "fig-8-16-fork-process-graph.jpg": (
        551,
        (460, 690, 900, 825),
    ),
    "fig-8-17-nested-fork-process-graph.jpg": (
        551,
        (440, 1140, 825, 1385),
    ),
    "fig-8-22-initial-user-stack.jpg": (
        558,
        (185, 920, 875, 1385),
    ),
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    for filename, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.jpg"
        output = ASSETS / filename

        with Image.open(source) as page:
            left, top, right, bottom = box
            if not (0 <= left < right <= page.width):
                raise ValueError(f"{filename}: invalid horizontal crop {box}")
            if not (0 <= top < bottom <= page.height):
                raise ValueError(f"{filename}: invalid vertical crop {box}")

            crop = page.crop(box)
            crop.save(
                output,
                "JPEG",
                quality=95,
                subsampling=0,
                optimize=True,
            )

        print(
            f"{output.relative_to(ROOT)}: "
            f"page {page_number}, box={box}, size={crop.size}"
        )


if __name__ == "__main__":
    main()
