from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter9"
    / "pages"
    / "page-653.jpg"
)
ANSWER_BOUNDARY_Y = 160


def main() -> None:
    with Image.open(PAGE) as source:
        if source.height <= ANSWER_BOUNDARY_Y:
            print(f"{PAGE.relative_to(ROOT)}: already cropped ({source.height}px)")
            return

        width = source.width
        cropped = source.crop((0, 0, width, ANSWER_BOUNDARY_Y))
        cropped.save(
            PAGE,
            "JPEG",
            quality=95,
            subsampling=0,
            optimize=True,
        )

    print(
        f"{PAGE.relative_to(ROOT)}: cropped to "
        f"{width}x{ANSWER_BOUNDARY_Y}"
    )


if __name__ == "__main__":
    main()
