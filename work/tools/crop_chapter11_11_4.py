import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter11"
PAGES = CHAPTER / "pages"
ASSETS = CHAPTER / "11.4" / "assets"


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Crops contain only the spatial figures; captions remain editable Markdown.
CROPS = {
    ASSETS / "fig-11-12-socket-interface-overview.png": (
        687,
        (116, 891, 974, 1399),
    ),
    ASSETS / "fig-11-14-listening-and-connected-descriptors.png": (
        691,
        (181, 126, 965, 467),
    ),
    ASSETS / "fig-11-15-getaddrinfo-data-structure.png": (
        692,
        (190, 133, 774, 570),
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
