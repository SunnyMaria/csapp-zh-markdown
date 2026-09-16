from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter7" / "pages"

CROPS = {
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter7"
    / "7.1"
    / "assets"
    / "figure-7-2-static-linking.jpg": ("page-501.jpg", (430, 725, 905, 1000)),
    ROOT
    / "output"
    / "csapp-faithful"
    / "chapter7"
    / "7.4"
    / "assets"
    / "figure-7-3-elf-relocatable-object-file.jpg": (
        "page-503.jpg",
        (515, 382, 830, 725),
    ),
}


def main() -> None:
    for output_path, (page_name, box) in CROPS.items():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(PAGES / page_name) as page:
            crop = page.crop(box)
            crop.save(output_path, quality=95, subsampling=0)
        print(f"{output_path.relative_to(ROOT)}: {crop.size}")


if __name__ == "__main__":
    main()
