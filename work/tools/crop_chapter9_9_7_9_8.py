import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter9"
PAGES = CHAPTER / "pages"


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Crops contain only the figure bodies; printed captions remain editable text.
CROPS = {
    CHAPTER / "9.7" / "assets" / "fig-9-21-core-i7-memory-system.jpg": (
        613,
        (63, 105, 710, 579),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-22-core-i7-address-translation.jpg": (
        613,
        (43, 610, 693, 1090),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-23-level-1-2-3-pte-format.jpg": (
        614,
        (132, 184, 714, 539),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-24-level-4-pte-format.jpg": (
        614,
        (132, 666, 714, 1042),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-25-core-i7-page-table-translation.jpg": (
        615,
        (35, 414, 713, 820),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-26-linux-process-virtual-memory.jpg": (
        616,
        (428, 340, 807, 786),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-27-linux-virtual-memory-organization.jpg": (
        617,
        (77, 108, 649, 518),
    ),
    CHAPTER / "9.7" / "assets" / "fig-9-28-linux-page-fault-handling.jpg": (
        618,
        (190, 282, 720, 655),
    ),
    CHAPTER / "9.8" / "assets" / "fig-9-29-shared-object.jpg": (
        619,
        (49, 656, 707, 963),
    ),
    CHAPTER / "9.8" / "assets" / "fig-9-30-private-copy-on-write-object.jpg": (
        620,
        (72, 365, 790, 678),
    ),
    CHAPTER / "9.8" / "assets" / "fig-9-31-loader-mappings.jpg": (
        621,
        (135, 511, 700, 887),
    ),
    CHAPTER / "9.8" / "assets" / "fig-9-32-mmap-parameters.jpg": (
        622,
        (210, 229, 710, 488),
    ),
}


POWERSHELL_CROP = r"""
Add-Type -AssemblyName System.Drawing
$sourcePath = $env:CROP_SOURCE
$targetPath = $env:CROP_TARGET
$left = [int]$env:CROP_LEFT
$top = [int]$env:CROP_TOP
$width = [int]$env:CROP_WIDTH
$height = [int]$env:CROP_HEIGHT
$page = [System.Drawing.Image]::FromFile($sourcePath)
$crop = [System.Drawing.Bitmap]::new($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($crop)
try {
    $sourceRect = [System.Drawing.Rectangle]::new($left, $top, $width, $height)
    $targetRect = [System.Drawing.Rectangle]::new(0, 0, $width, $height)
    $graphics.DrawImage(
        $page,
        $targetRect,
        $sourceRect,
        [System.Drawing.GraphicsUnit]::Pixel
    )
    $crop.Save($targetPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
}
finally {
    $graphics.Dispose()
    $crop.Dispose()
    $page.Dispose()
}
"""


def main() -> None:
    for output, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.jpg"
        output.parent.mkdir(parents=True, exist_ok=True)
        left, top, right, bottom = box
        if not (0 <= left < right and 0 <= top < bottom):
            raise ValueError(f"{output.name}: invalid crop {box}")

        environment = os.environ.copy()
        environment.update(
            {
                "CROP_SOURCE": str(source),
                "CROP_TARGET": str(output),
                "CROP_LEFT": str(left),
                "CROP_TOP": str(top),
                "CROP_WIDTH": str(right - left),
                "CROP_HEIGHT": str(bottom - top),
            }
        )
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                POWERSHELL_CROP,
            ],
            check=True,
            env=environment,
        )

        print(
            f"{output.relative_to(ROOT)}: "
            f"page {page_number}, box={box}, "
            f"size=({right - left}, {bottom - top})"
        )


if __name__ == "__main__":
    main()
