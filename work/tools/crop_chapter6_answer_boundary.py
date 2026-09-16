from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "output" / "csapp-faithful" / "chapter6" / "pages" / "page-495.jpg"


def main() -> None:
    with Image.open(PAGE) as image:
        image.crop((0, 0, image.width, min(390, image.height))).save(
            PAGE,
            quality=95,
            subsampling=0,
        )


if __name__ == "__main__":
    main()
