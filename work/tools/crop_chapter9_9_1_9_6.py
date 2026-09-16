from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "output" / "csapp-faithful" / "chapter9" / "pages"
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter9"

# (source page, target section, output name, left, top, right, bottom)
CROPS = [
    (596, "9.1", "fig-9-1-physical-addressing.png", 480, 230, 775, 490),
    (596, "9.1", "fig-9-2-virtual-addressing.png", 185, 610, 775, 875),
    (598, "9.3", "fig-9-3-dram-as-vm-cache.png", 190, 173, 720, 370),
    (599, "9.3", "fig-9-4-page-table.png", 330, 129, 715, 430),
    (599, "9.3", "fig-9-5-vm-page-hit.png", 100, 810, 710, 1108),
    (600, "9.3", "fig-9-6-vm-page-fault-before.png", 165, 335, 685, 655),
    (600, "9.3", "fig-9-7-vm-page-fault-after.png", 165, 788, 685, 1090),
    (601, "9.3", "fig-9-8-allocating-virtual-page.png", 330, 283, 720, 620),
    (602, "9.4", "fig-9-9-independent-address-spaces.png", 390, 135, 715, 358),
    (603, "9.5", "fig-9-10-page-level-memory-protection.png", 85, 435, 690, 710),
    (604, "9.6", "fig-9-12-address-translation-with-page-table.png", 140, 790, 770, 1120),
    (605, "9.6", "fig-9-13-page-hit-and-page-fault.png", 90, 360, 700, 860),
    (606, "9.6", "fig-9-14-physical-cache-with-vm.png", 160, 570, 705, 810),
    (607, "9.6", "fig-9-16-tlb-hit-and-miss.png", 25, 350, 720, 665),
    (608, "9.6", "fig-9-17-two-level-page-table.png", 125, 100, 785, 485),
    (608, "9.6", "fig-9-18-k-level-address-translation.png", 215, 858, 665, 1108),
    (609, "9.6", "fig-9-19-small-memory-addressing.png", 165, 553, 675, 740),
    (610, "9.6", "fig-9-20-small-memory-system.png", 125, 85, 690, 1045),
]


def main() -> None:
    for page_number, section, name, left, top, right, bottom in CROPS:
        source = PAGES / f"page-{page_number}.jpg"
        target_dir = CHAPTER / section / "assets"
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / name
        width = right - left
        height = bottom - top
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(source),
                "-vf",
                f"crop={width}:{height}:{left}:{top}",
                "-frames:v",
                "1",
                str(target),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
