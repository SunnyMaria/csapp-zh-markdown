from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output/csapp-faithful/chapter10/pages/page-658.png"
OUTPUT = (
    ROOT
    / "output/csapp-faithful/chapter10/10.2/assets"
    / "fig-10-1-linux-directory-hierarchy.png"
)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as page:
        figure = page.crop((130, 1152, 890, 1392))
        figure.save(OUTPUT, optimize=True)


if __name__ == "__main__":
    main()
