import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter11"
PAGES = CHAPTER / "pages"


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Crops contain only the spatial diagrams; captions remain editable Markdown.
CROPS = {
    CHAPTER / "11.1" / "assets" / "fig-11-1-client-server-transaction.png": (
        677,
        (190, 1114, 895, 1228),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-2-network-host-hardware.png": (
        678,
        (185, 540, 780, 970),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-3-ethernet-segment.png": (
        678,
        (585, 1240, 905, 1385),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-4-bridged-ethernet.png": (
        679,
        (170, 414, 920, 870),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-5-lan-conceptual-view.png": (
        679,
        (660, 1270, 975, 1385),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-6-small-internet.png": (
        680,
        (75, 120, 880, 285),
    ),
    CHAPTER / "11.2" / "assets" / "fig-11-7-internet-data-transfer.png": (
        681,
        (130, 230, 930, 660),
    ),
    CHAPTER / "11.3" / "assets" / "fig-11-8-internet-application-organization.png": (
        681,
        (175, 1015, 840, 1338),
    ),
    CHAPTER / "11.3" / "assets" / "fig-11-10-internet-domain-name-hierarchy.png": (
        684,
        (205, 755, 815, 1125),
    ),
    CHAPTER / "11.3" / "assets" / "fig-11-11-internet-connection.png": (
        686,
        (155, 775, 845, 955),
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
try {
    if ($left -lt 0 -or $top -lt 0 -or
        $left + $width -gt $page.Width -or
        $top + $height -gt $page.Height) {
        throw "Crop is outside source image bounds"
    }

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
    }
}
finally {
    $page.Dispose()
}
"""


def main() -> None:
    for output, (page_number, box) in CROPS.items():
        source = PAGES / f"page-{page_number}.png"
        if not source.is_file():
            raise FileNotFoundError(source)

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
