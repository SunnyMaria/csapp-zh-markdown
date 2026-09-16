import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter10"
PAGES = CHAPTER / "pages"


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Crops contain only the spatial diagrams; captions remain editable Markdown.
CROPS = {
    CHAPTER / "10.8" / "assets" / "fig-10-12-open-file-kernel-structures.png": (
        670,
        (170, 294, 772, 621),
    ),
    CHAPTER / "10.8" / "assets" / "fig-10-13-file-sharing.png": (
        670,
        (184, 812, 772, 1166),
    ),
    CHAPTER / "10.8" / "assets" / "fig-10-14-child-inherits-open-files.png": (
        671,
        (235, 125, 783, 457),
    ),
    CHAPTER / "10.9" / "assets" / "fig-10-15-dup2-redirection.png": (
        672,
        (194, 754, 737, 1081),
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
    $crop.Save($targetPath, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $graphics.Dispose()
    $crop.Dispose()
    $page.Dispose()
}
"""


def main() -> None:
    for output, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.png"
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
            ["powershell.exe", "-NoProfile", "-Command", POWERSHELL_CROP],
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
