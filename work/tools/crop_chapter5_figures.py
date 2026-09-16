from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "output" / "csapp-faithful" / "chapter5"


FIGURES = [
    (
        CHAPTER / "pages" / "page-382.jpg",
        (205, 1000, 835, 1392),
        CHAPTER / "5.2" / "assets" / "figure-5-2-prefix-sum-performance.jpg",
    ),
    (
        CHAPTER / "pages" / "page-383.jpg",
        (490, 945, 910, 1045),
        CHAPTER / "5.3" / "assets" / "figure-5-3-vector-data-type.jpg",
    ),
    (
        CHAPTER / "pages" / "page-388.jpg",
        (190, 420, 870, 770),
        CHAPTER / "5.4" / "assets" / "figure-5-8-lowercase-performance.jpg",
    ),
    (
        CHAPTER / "pages" / "page-394.jpg",
        (225, 135, 850, 755),
        CHAPTER / "5.7" / "assets" / "figure-5-11-out-of-order-processor.jpg",
    ),
    (
        CHAPTER / "pages" / "page-399.jpg",
        (145, 430, 850, 745),
        CHAPTER / "5.7" / "assets" / "figure-5-13-combine4-loop-operations.jpg",
    ),
    (
        CHAPTER / "pages" / "page-400.jpg",
        (205, 300, 855, 650),
        CHAPTER / "5.7" / "assets" / "figure-5-14-combine4-data-flow-abstraction.jpg",
    ),
    (
        CHAPTER / "pages" / "page-400.jpg",
        (605, 690, 925, 1335),
        CHAPTER / "5.7" / "assets" / "figure-5-15-combine4-critical-path.jpg",
    ),
    (
        CHAPTER / "pages" / "page-404.jpg",
        (250, 225, 835, 510),
        CHAPTER / "5.8" / "assets" / "figure-5-17-k-by-1-unrolling-performance.jpg",
    ),
    (
        CHAPTER / "pages" / "page-404.jpg",
        (180, 925, 865, 1225),
        CHAPTER / "5.8" / "assets" / "figure-5-18-combine5-loop-operations.jpg",
    ),
    (
        CHAPTER / "pages" / "page-405.jpg",
        (35, 145, 345, 1090),
        CHAPTER / "5.8" / "assets" / "figure-5-19-combine5-data-flow-abstraction.jpg",
    ),
    (
        CHAPTER / "pages" / "page-405.jpg",
        (360, 135, 805, 990),
        CHAPTER / "5.8" / "assets" / "figure-5-20-combine5-critical-path.jpg",
    ),
    (
        CHAPTER / "pages" / "page-407.jpg",
        (70, 450, 875, 795),
        CHAPTER / "5.9" / "assets" / "figure-5-22-combine6-loop-operations.jpg",
    ),
    (
        CHAPTER / "pages" / "page-408.jpg",
        (85, 135, 455, 815),
        CHAPTER / "5.9" / "assets" / "figure-5-23-combine6-data-flow-abstraction.jpg",
    ),
    (
        CHAPTER / "pages" / "page-408.jpg",
        (495, 125, 925, 815),
        CHAPTER / "5.9" / "assets" / "figure-5-24-combine6-critical-paths.jpg",
    ),
    (
        CHAPTER / "pages" / "page-408.jpg",
        (245, 955, 835, 1190),
        CHAPTER / "5.9" / "assets" / "figure-5-25-k-by-k-unrolling-performance.jpg",
    ),
    (
        CHAPTER / "pages" / "page-410.jpg",
        (130, 835, 870, 1240),
        CHAPTER / "5.9" / "assets" / "figure-5-27-combine7-loop-operations.jpg",
    ),
    (
        CHAPTER / "pages" / "page-411.jpg",
        (45, 135, 390, 825),
        CHAPTER / "5.9" / "assets" / "figure-5-28-combine7-data-flow-abstraction.jpg",
    ),
    (
        CHAPTER / "pages" / "page-411.jpg",
        (410, 125, 825, 865),
        CHAPTER / "5.9" / "assets" / "figure-5-29-combine7-critical-path.jpg",
    ),
    (
        CHAPTER / "pages" / "page-411.jpg",
        (175, 970, 810, 1210),
        CHAPTER / "5.9" / "assets" / "figure-5-30-k-by-1a-unrolling-performance.jpg",
    ),
    (
        CHAPTER / "pages" / "page-420.jpg",
        (600, 1045, 965, 1300),
        CHAPTER / "5.12" / "assets" / "figure-5-34-load-store-units.jpg",
    ),
    (
        CHAPTER / "pages" / "page-421.jpg",
        (170, 240, 775, 565),
        CHAPTER / "5.12" / "assets" / "figure-5-35-write-read-loop-operations.jpg",
    ),
    (
        CHAPTER / "pages" / "page-421.jpg",
        (155, 990, 790, 1350),
        CHAPTER / "5.12" / "assets" / "figure-5-36-write-read-data-flow-abstraction.jpg",
    ),
    (
        CHAPTER / "pages" / "page-422.jpg",
        (255, 430, 790, 1190),
        CHAPTER / "5.12" / "assets" / "figure-5-37-write-read-critical-paths.jpg",
    ),
    (
        CHAPTER / "pages" / "page-427.jpg",
        (55, 205, 900, 845),
        CHAPTER / "5.14" / "assets" / "figure-5-38-bigram-profiling-results.jpg",
    ),
]


for source, box, target in FIGURES:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image.crop(box).save(target, quality=95, subsampling=0)
