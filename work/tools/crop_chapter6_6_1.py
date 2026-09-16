from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter6" / "pages"
ASSETS = ROOT / "output" / "csapp-faithful" / "chapter6" / "6.1" / "assets"


CROPS = {
    "figure-6-1-inverted-pendulum.jpg": (436, (205, 610, 775, 805)),
    "figure-6-3-dram-chip.jpg": (437, (150, 685, 830, 995)),
    "figure-6-4-reading-dram-supercell.jpg": (438, (80, 250, 930, 615)),
    "figure-6-5-reading-memory-module.jpg": (439, (65, 325, 900, 895)),
    "figure-6-6-cpu-main-memory-bus.jpg": (441, (160, 665, 710, 900)),
    "figure-6-7-memory-read-transaction.jpg": (442, (245, 285, 810, 960)),
    "figure-6-8-memory-write-transaction.jpg": (443, (155, 120, 735, 860)),
    "figure-6-9-disk-construction.jpg": (444, (70, 135, 960, 445)),
    "figure-6-10-disk-dynamics.jpg": (445, (15, 655, 930, 980)),
    "figure-6-11-io-bus-structure.jpg": (448, (235, 280, 900, 835)),
    "figure-6-12-reading-disk-sector.jpg": (449, (25, 250, 940, 1040)),
    "figure-6-13-solid-state-disk.jpg": (450, (180, 945, 830, 1240)),
    "figure-6-16-processor-memory-gap.jpg": (453, (75, 335, 800, 690)),
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    for output_name, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.jpg"
        with Image.open(source) as page:
            crop = page.crop(box)
            crop.save(
                ASSETS / output_name,
                "JPEG",
                quality=95,
                subsampling=0,
                optimize=True,
            )
        print(f"{output_name}: page {page_number}, box={box}")


if __name__ == "__main__":
    main()
