from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter6" / "pages"
ASSETS = ROOT / "output" / "csapp-faithful" / "chapter6" / "6.3" / "assets"

CROPS = {
    "fig-6-21-memory-hierarchy.jpg": ("page-457.jpg", (25, 835, 855, 1347)),
    "fig-6-22-caching-principle.jpg": ("page-458.jpg", (190, 1040, 825, 1340)),
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for output_name, (page_name, box) in CROPS.items():
        with Image.open(PAGES / page_name) as page:
            crop = page.crop(box)
            crop.save(ASSETS / output_name, quality=95, subsampling=0)
        print(f"{output_name}: {crop.size}")


if __name__ == "__main__":
    main()
