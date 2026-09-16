from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter11"
    / "pages"
    / "page-714.png"
)
ANSWER_BOUNDARY_Y = 510


def main() -> None:
    with Image.open(PAGE) as source:
        if source.height <= ANSWER_BOUNDARY_Y:
            print(f"{PAGE.relative_to(ROOT)}: already cropped ({source.height}px)")
            return

        cropped = source.crop((0, 0, source.width, ANSWER_BOUNDARY_Y))
        cropped.save(PAGE, "PNG", optimize=True)

    print(f"{PAGE.relative_to(ROOT)}: cropped to {source.width}x{ANSWER_BOUNDARY_Y}")


if __name__ == "__main__":
    main()
