from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter7" / "pages"
ASSETS = ROOT / "output" / "csapp-faithful" / "chapter7" / "7.12" / "assets"

CROPS = {
    "fig-7-18-got-global-variable-reference.jpg": (
        "page-526.jpg",
        (160, 530, 870, 825),
    ),
    "fig-7-19-plt-got-external-function-calls.jpg": (
        "page-527.jpg",
        (25, 650, 865, 1140),
    ),
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for filename, (page_name, box) in CROPS.items():
        with Image.open(PAGES / page_name) as page:
            page.crop(box).save(ASSETS / filename, quality=95, subsampling=0)
        print(f"created {ASSETS / filename}")


if __name__ == "__main__":
    main()
