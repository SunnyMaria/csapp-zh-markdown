from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "output" / "csapp-faithful" / "chapter8" / "pages"
CHAPTER_DIR = ROOT / "output" / "csapp-faithful" / "chapter8"
PAGE_WIDTH = 1009
PAGE_HEIGHT = 1515


# Coordinates are (left, top, right, bottom) in the rendered 1009 x 1515 page images.
# Each crop contains only the figure body; captions are reconstructed as searchable text.
CROPS = (
    (
        538,
        (500, 660, 960, 930),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-1-anatomy-of-an-exception.jpg",
    ),
    (
        539,
        (475, 475, 940, 748),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-2-exception-table.jpg",
    ),
    (
        539,
        (155, 850, 790, 976),
        CHAPTER_DIR
        / "8.1"
        / "assets"
        / "fig-8-3-generating-exception-handler-address.jpg",
    ),
    (
        540,
        (235, 770, 835, 990),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-5-interrupt-handling.jpg",
    ),
    (
        541,
        (150, 195, 795, 410),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-6-trap-handling.jpg",
    ),
    (
        541,
        (140, 740, 830, 948),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-7-fault-handling.jpg",
    ),
    (
        542,
        (220, 135, 875, 330),
        CHAPTER_DIR / "8.1" / "assets" / "fig-8-8-abort-handling.jpg",
    ),
    (
        544,
        (505, 1115, 960, 1348),
        CHAPTER_DIR / "8.2" / "assets" / "fig-8-12-logical-control-flows.jpg",
    ),
    (
        546,
        (250, 365, 825, 875),
        CHAPTER_DIR / "8.2" / "assets" / "fig-8-13-process-address-space.jpg",
    ),
    (
        547,
        (105, 1110, 825, 1370),
        CHAPTER_DIR / "8.2" / "assets" / "fig-8-14-process-context-switch.jpg",
    ),
)


def crop_figures() -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to crop the rendered page images")

    for page_number, box, output_path in CROPS:
        page_path = PAGES_DIR / f"page-{page_number}.jpg"
        left, top, right, bottom = box
        if not (
            0 <= left < right <= PAGE_WIDTH
            and 0 <= top < bottom <= PAGE_HEIGHT
        ):
            raise ValueError(
                f"Crop {box} is outside page {page_number} "
                f"({PAGE_WIDTH} x {PAGE_HEIGHT})"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        width = right - left
        height = bottom - top
        subprocess.run(
            [
                ffmpeg,
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(page_path),
                "-vf",
                f"crop={width}:{height}:{left}:{top}",
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(output_path),
            ],
            check=True,
        )
        print(f"{page_path.name} {box} -> {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    crop_figures()
