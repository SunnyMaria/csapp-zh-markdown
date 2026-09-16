from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter10"
    / "pages"
    / "page-673.png"
)
TARGET = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter10"
    / "10.11"
    / "assets"
    / "fig-10-16-io-package-layers.png"
)

# The crop contains only the spatial package hierarchy. The printed caption is
# reproduced as editable Markdown text below the image.
CROP_BOX = (165, 1120, 920, 1370)


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(PAGE) as source:
        left, top, right, bottom = CROP_BOX
        if not (0 <= left < right <= source.width):
            raise ValueError(f"invalid horizontal crop {CROP_BOX} for {source.size}")
        if not (0 <= top < bottom <= source.height):
            raise ValueError(f"invalid vertical crop {CROP_BOX} for {source.size}")

        source.crop(CROP_BOX).save(TARGET, "PNG", optimize=True)

    print(f"{PAGE.relative_to(ROOT)} {CROP_BOX} -> {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
