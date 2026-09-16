from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path("output/csapp-faithful/chapter12")
PAGES = ROOT / "pages"

CROPS = [
    (717, (118, 638, 470, 853), ROOT / "12.1/assets/figure-12-1.png"),
    (717, (558, 622, 893, 852), ROOT / "12.1/assets/figure-12-2.png"),
    (717, (115, 1120, 470, 1400), ROOT / "12.1/assets/figure-12-3.png"),
    (717, (556, 1096, 893, 1399), ROOT / "12.1/assets/figure-12-4.png"),
    (722, (488, 306, 919, 504), ROOT / "12.2/assets/figure-12-7.png"),
    (
        726,
        (475, 744, 910, 1074),
        ROOT / "12.3/assets/fig-12-12-thread-execution.png",
    ),
    (
        736,
        (45, 555, 450, 890),
        ROOT / "12.5/assets/fig-12-19-progress-graph.png",
    ),
    (
        736,
        (485, 555, 905, 890),
        ROOT / "12.5/assets/fig-12-20-trajectory-example.png",
    ),
    (
        737,
        (270, 195, 790, 570),
        ROOT / "12.5/assets/fig-12-21-safe-unsafe-trajectories.png",
    ),
    (
        738,
        (170, 875, 780, 1355),
        ROOT / "12.5/assets/fig-12-22-semaphore-mutual-exclusion.png",
    ),
    (
        740,
        (265, 175, 710, 260),
        ROOT / "12.5/assets/fig-12-23-producer-consumer.png",
    ),
    (
        743,
        (170, 875, 890, 1100),
        ROOT / "12.5/assets/fig-12-27-prethreaded-server-organization.png",
    ),
    (
        746,
        (555, 265, 930, 445),
        ROOT / "12.6/assets/fig-12-30-program-set-relations.png",
    ),
    (
        749,
        (500, 845, 960, 1160),
        ROOT / "12.6/assets/fig-12-35-psum-local-performance.png",
    ),
    (
        752,
        (545, 1177, 930, 1372),
        ROOT / "12.7/assets/fig-12-39-function-set-relationships.png",
    ),
    (
        756,
        (205, 690, 802, 1165),
        ROOT / "12.7/assets/fig-12-44-deadlock-progress-graph.png",
    ),
    (
        757,
        (225, 468, 822, 936),
        ROOT / "12.7/assets/fig-12-45-deadlock-free-progress-graph.png",
    ),
]


def main() -> None:
    for page_number, box, output in CROPS:
        page = PAGES / f"page-{page_number}.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(page) as image:
            image.crop(box).save(output)
        print(f"{page.name} {box} -> {output}")


if __name__ == "__main__":
    main()
