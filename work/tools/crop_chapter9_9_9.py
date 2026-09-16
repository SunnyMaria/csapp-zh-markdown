import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "output" / "csapp-faithful" / "chapter9" / "pages"
ASSETS_DIR = (
    ROOT / "output" / "csapp-faithful" / "chapter9" / "9.9" / "assets"
)


# Coordinates are (left, top, right, bottom) in the rendered page images.
# Each crop contains only the spatial figure body; captions remain searchable text.
CROPS = (
    (
        623,
        (452, 232, 708, 600),
        "fig-9-33-heap.png",
    ),
    (
        625,
        (374, 159, 725, 572),
        "fig-9-34-malloc-free-blocks.png",
    ),
    (
        628,
        (160, 838, 808, 1051),
        "fig-9-35-simple-heap-block-format.png",
    ),
    (
        629,
        (25, 417, 787, 532),
        "fig-9-36-implicit-free-list.png",
    ),
    (
        630,
        (82, 703, 761, 811),
        "fig-9-37-splitting-free-block.png",
    ),
    (
        631,
        (17, 211, 704, 317),
        "fig-9-38-false-fragmentation.png",
    ),
    (
        631,
        (397, 875, 707, 1113),
        "fig-9-39-boundary-tag-block-format.png",
    ),
    (
        632,
        (120, 229, 750, 631),
        "fig-9-40-boundary-tag-coalescing.png",
    ),
    (
        634,
        (78, 817, 808, 961),
        "fig-9-42-implicit-free-list-invariant.png",
    ),
    (
        639,
        (98, 612, 705, 873),
        "fig-9-48-doubly-linked-free-list-block-format.png",
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
try {
    if (
        $left -lt 0 -or
        $top -lt 0 -or
        $width -le 0 -or
        $height -le 0 -or
        ($left + $width) -gt $page.Width -or
        ($top + $height) -gt $page.Height
    ) {
        throw "Invalid crop rectangle for $sourcePath"
    }

    $crop = [System.Drawing.Bitmap]::new($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($crop)
    try {
        $sourceRect = [System.Drawing.Rectangle]::new(
            $left,
            $top,
            $width,
            $height
        )
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
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for page_number, box, filename in CROPS:
        source_path = PAGES_DIR / f"page-{page_number}.jpg"
        output_path = ASSETS_DIR / filename
        left, top, right, bottom = box

        environment = os.environ.copy()
        environment.update(
            {
                "CROP_SOURCE": str(source_path),
                "CROP_TARGET": str(output_path),
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
            f"{source_path.name} {box} -> "
            f"{output_path.relative_to(ROOT)}"
        )


if __name__ == "__main__":
    main()
