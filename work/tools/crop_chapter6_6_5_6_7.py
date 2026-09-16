from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter6"

CROPS = (
    (
        CHAPTER / "pages" / "page-481.jpg",
        CHAPTER / "6.6" / "assets" / "fig-6-41-memory-mountain.jpg",
        (45, 620, 870, 1085),
    ),
    (
        CHAPTER / "pages" / "page-482.jpg",
        CHAPTER / "6.6" / "assets" / "fig-6-42-temporal-locality-ridges.jpg",
        (150, 495, 900, 985),
    ),
    (
        CHAPTER / "pages" / "page-483.jpg",
        CHAPTER / "6.6" / "assets" / "fig-6-43-spatial-locality-slope.jpg",
        (125, 200, 735, 575),
    ),
    (
        CHAPTER / "pages" / "page-485.jpg",
        CHAPTER / "6.6" / "assets" / "fig-6-46-matrix-multiplication-performance.jpg",
        (100, 705, 790, 1100),
    ),
)


def main() -> None:
    for source, target, box in CROPS:
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as page:
            crop = page.crop(box)
            crop.save(target, quality=95, optimize=True)
        print(f"{target.relative_to(ROOT)} {crop.size[0]}x{crop.size[1]}")


if __name__ == "__main__":
    main()
