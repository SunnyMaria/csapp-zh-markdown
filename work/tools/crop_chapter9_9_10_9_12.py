import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "output" / "csapp-faithful" / "chapter9" / "pages"
CHAPTER_DIR = ROOT / "output" / "csapp-faithful" / "chapter9"


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Each crop contains only the two-dimensional figure body. Captions remain text.
CROPS = (
    (
        642,
        (170, 764, 655, 956),
        CHAPTER_DIR / "9.10" / "assets" / "fig-9-49-reachability-graph.png",
    ),
    (
        643,
        (100, 250, 633, 356),
        CHAPTER_DIR / "9.10" / "assets" / "fig-9-50-conservative-gc.png",
    ),
    (
        644,
        (155, 405, 682, 673),
        CHAPTER_DIR / "9.10" / "assets" / "fig-9-52-mark-and-sweep-example.png",
    ),
    (
        645,
        (184, 105, 560, 189),
        CHAPTER_DIR / "9.10" / "assets" / "fig-9-53-balanced-tree-pointers.png",
    ),
)

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
    $crop.Save($targetPath, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $graphics.Dispose()
    $crop.Dispose()
    $page.Dispose()
}
"""


def crop_figures() -> None:
    for page_number, box, output_path in CROPS:
        page_path = PAGES_DIR / f"page-{page_number}.jpg"
        left, top, right, bottom = box
        if not (0 <= left < right and 0 <= top < bottom):
            raise ValueError(f"Invalid crop {box} for page {page_number}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        environment = os.environ.copy()
        environment.update(
            {
                "CROP_SOURCE": str(page_path),
                "CROP_TARGET": str(output_path),
                "CROP_LEFT": str(left),
                "CROP_TOP": str(top),
                "CROP_WIDTH": str(right - left),
                "CROP_HEIGHT": str(bottom - top),
            }
        )
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", POWERSHELL_CROP],
            check=True,
            env=environment,
        )
        print(f"{page_path.name} {box} -> {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    crop_figures()
