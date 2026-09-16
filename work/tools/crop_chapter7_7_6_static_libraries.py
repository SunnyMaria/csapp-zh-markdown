from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter7"
    / "pages"
    / "page-513.jpg"
)
OUTPUT = (
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter7"
    / "7.6"
    / "assets"
    / "fig-7-8-linking-with-static-libraries.jpg"
)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(PAGE) as page:
        crop = page.crop((125, 405, 835, 690))
        crop.save(OUTPUT, quality=95, subsampling=0)
    print(f"{OUTPUT.relative_to(ROOT)}: {crop.size}")


if __name__ == "__main__":
    main()
