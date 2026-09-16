from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter6" / "pages"
ASSETS = ROOT / "output" / "csapp-faithful" / "chapter6" / "6.4" / "assets"


CROPS = {
    "fig-6-24-typical-cache-bus-structure.jpg": (461, (130, 760, 760, 1035)),
    "fig-6-25-general-cache-organization.jpg": (462, (110, 245, 860, 805)),
    "fig-6-27-direct-mapped-cache.jpg": (463, (195, 960, 770, 1130)),
    "fig-6-28-direct-mapped-set-selection.jpg": (464, (175, 350, 875, 570)),
    "fig-6-29-direct-mapped-line-match.jpg": (464, (175, 915, 865, 1170)),
    "fig-6-31-middle-bit-cache-indexing.jpg": (468, (170, 842, 915, 1320)),
    "fig-6-32-set-associative-cache.jpg": (469, (55, 755, 870, 1005)),
    "fig-6-33-set-associative-set-selection.jpg": (470, (180, 125, 870, 425)),
    "fig-6-34-set-associative-line-match.jpg": (470, (185, 600, 840, 875)),
    "fig-6-35-fully-associative-cache.jpg": (471, (60, 155, 830, 300)),
    "fig-6-36-fully-associative-set-selection.jpg": (471, (95, 445, 800, 625)),
    "fig-6-37-fully-associative-line-match.jpg": (471, (85, 775, 850, 1105)),
    "fig-6-38-core-i7-cache-hierarchy.jpg": (474, (250, 780, 805, 1245)),
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for filename, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.jpg"
        with Image.open(source) as page:
            crop = page.crop(box)
            crop.save(ASSETS / filename, quality=95, subsampling=0)
        print(f"{filename}: page {page_number}, box={box}")


if __name__ == "__main__":
    main()
