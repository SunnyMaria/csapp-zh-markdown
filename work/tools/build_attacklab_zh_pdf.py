from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from build_attacklab_zh_docx import (
    ASSET_DIR,
    FONT_CJK,
    FONT_CJK_BOLD,
    FONT_MONO,
    SOURCE_MD,
    create_figure_2,
    create_figure_3,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PDF = ROOT / "output" / "attacklab-zh" / "attacklab-zh.pdf"
INLINE_RE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)")


def register_fonts():
    pdfmetrics.registerFont(TTFont("MicrosoftYaHei", str(FONT_CJK)))
    pdfmetrics.registerFont(TTFont("MicrosoftYaHei-Bold", str(FONT_CJK_BOLD)))
    pdfmetrics.registerFont(TTFont("Consolas", str(FONT_MONO)))


def inline_markup(text: str) -> str:
    parts = []
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            parts.append(f'<font name="Consolas" color="#1F4D78">{html.escape(part[1:-1])}</font>')
        elif part.startswith("**") and part.endswith("**"):
            parts.append(f'<font name="MicrosoftYaHei-Bold">{html.escape(part[2:-2])}</font>')
        elif part.startswith("*") and part.endswith("*"):
            parts.append(f'<i>{html.escape(part[1:-1])}</i>')
        else:
            parts.append(html.escape(part))
    return "".join(parts)


def image_flowable(path: Path, max_width=6.35 * inch, max_height=7.2 * inch):
    with PILImage.open(path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("MicrosoftYaHei", 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawCentredString(letter[0] / 2, 0.48 * inch, str(doc.page))
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "ChineseBody",
            parent=styles["BodyText"],
            fontName="MicrosoftYaHei",
            fontSize=10.5,
            leading=15.5,
            textColor=colors.HexColor("#202020"),
            spaceAfter=6,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "ChineseH1",
            parent=styles["Heading1"],
            fontName="MicrosoftYaHei-Bold",
            fontSize=16,
            leading=22,
            textColor=colors.HexColor("#2E74B5"),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "ChineseH2",
            parent=styles["Heading2"],
            fontName="MicrosoftYaHei-Bold",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#2E74B5"),
            spaceBefore=11,
            spaceAfter=6,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "course": ParagraphStyle(
            "Course",
            fontName="MicrosoftYaHei",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER,
            spaceBefore=52,
            spaceAfter=8,
        ),
        "title": ParagraphStyle(
            "DocTitle",
            fontName="MicrosoftYaHei-Bold",
            fontSize=22,
            leading=29,
            textColor=colors.HexColor("#202020"),
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "metadata": ParagraphStyle(
            "Metadata",
            fontName="MicrosoftYaHei",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#333333"),
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName="MicrosoftYaHei",
            fontSize=9.3,
            leading=13,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "CodeBlock",
            fontName="Consolas",
            fontSize=8.4,
            leading=11.2,
            textColor=colors.HexColor("#202020"),
            backColor=colors.HexColor("#F6F7F9"),
            borderPadding=7,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="MicrosoftYaHei",
            fontSize=10.5,
            leading=15.5,
            leftIndent=27,
            firstLineIndent=-13.5,
            bulletIndent=13.5,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "bullet2": ParagraphStyle(
            "Bullet2",
            fontName="MicrosoftYaHei",
            fontSize=10.5,
            leading=15.5,
            leftIndent=54,
            firstLineIndent=-13.5,
            bulletIndent=40.5,
            spaceAfter=4,
            wordWrap="CJK",
        ),
    }


def markdown_table(lines, body_style):
    rows = []
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if index == 1 and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append([Paragraph(inline_markup(cell), body_style) for cell in cells])
    widths = [0.8 * inch, 1.2 * inch, 0.8 * inch, 1.0 * inch, 1.7 * inch, 1.0 * inch]
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#7A7A7A")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")),
                ("FONTNAME", (0, 0), (-1, 0), "MicrosoftYaHei-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def build_pdf():
    register_fonts()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    create_figure_2(ASSET_DIR / "figure-2-rop-gadgets-zh.png")
    create_figure_3(ASSET_DIR / "figure-3-instruction-encodings-zh.png")
    styles = build_styles()
    story = []

    lines = SOURCE_MD.read_text(encoding="utf-8").splitlines()
    first_h1 = next(i for i, line in enumerate(lines) if line.startswith("# "))
    second_h1 = next(i for i in range(first_h1 + 1, len(lines)) if lines[i].startswith("# "))
    story.append(Paragraph(inline_markup(lines[first_h1][2:].strip()), styles["course"]))
    story.append(Paragraph(inline_markup(lines[second_h1][2:].strip()), styles["title"]))

    i = second_h1 + 1
    while i < len(lines) and not lines[i].startswith("## "):
        text = lines[i].rstrip().rstrip("  ")
        if text:
            story.append(Paragraph(inline_markup(text), styles["metadata"]))
        i += 1
    story.append(Spacer(1, 16))
    number_counter = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            story.append(KeepTogether([Preformatted("\n".join(code), styles["code"])]))
            i += 1
            continue
        if stripped.startswith("!["):
            match = re.match(r"!\[[^]]*\]\(([^)]+)\)", stripped)
            image = image_flowable(SOURCE_MD.parent / match.group(1)) if match else None
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if image is not None and i < len(lines) and lines[i].strip().startswith("*图 "):
                caption_text = inline_markup(lines[i].strip())
                story.append(KeepTogether([image, Paragraph(caption_text, styles["caption"])]))
                i += 1
            elif image is not None:
                story.append(image)
            continue
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            story.append(markdown_table(table_lines, styles["body"]))
            story.append(Spacer(1, 5))
            continue
        if stripped.startswith("## "):
            story.append(Paragraph(inline_markup(stripped[3:]), styles["h1"]))
            number_counter = 0
            i += 1
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(inline_markup(stripped[4:]), styles["h2"]))
            number_counter = 0
            i += 1
            continue
        if stripped.startswith("> "):
            callout = Table([[Paragraph(inline_markup(stripped[2:]), styles["body"])]] , colWidths=[6.3 * inch])
            callout.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
                        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#2E74B5")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 9),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ]
                )
            )
            story.append(callout)
            story.append(Spacer(1, 6))
            i += 1
            continue
        bullet = re.match(r"^(\s*)-\s+(.*)", line)
        if bullet:
            level = 1 if len(bullet.group(1)) >= 2 else 0
            story.append(Paragraph(inline_markup(bullet.group(2)), styles["bullet2" if level else "bullet"], bulletText="•"))
            number_counter = 0
            i += 1
            continue
        number = re.match(r"^(\s*)(\d+)\.\s+(.*)", line)
        if number:
            number_counter = int(number.group(2))
            level = 1 if len(number.group(1)) >= 2 else 0
            story.append(
                Paragraph(
                    inline_markup(number.group(3)),
                    styles["bullet2" if level else "bullet"],
                    bulletText=f"{number_counter}.",
                )
            )
            i += 1
            continue
        if stripped.startswith("*图 "):
            story.append(Paragraph(inline_markup(stripped), styles["caption"]))
            i += 1
            continue

        paragraph_lines = [(stripped, line.rstrip().endswith("  "))]
        i += 1
        while i < len(lines):
            candidate = lines[i]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (
                candidate_stripped.startswith(("## ", "### ", "```", "![", "|", "> "))
                or re.match(r"^\s*-\s+", candidate)
                or re.match(r"^\s*\d+\.\s+", candidate)
            ):
                break
            paragraph_lines.append((candidate_stripped, candidate.rstrip().endswith("  ")))
            i += 1
        pieces = []
        for index, (text, hard_break) in enumerate(paragraph_lines):
            pieces.append(inline_markup(text.rstrip()))
            if index != len(paragraph_lines) - 1:
                pieces.append("<br/>" if hard_break else " ")
        story.append(Paragraph("".join(pieces), styles["body"]))
        number_counter = 0

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=0.78 * inch,
        title="攻击实验：理解缓冲区溢出漏洞（中文完整翻译）",
        author="OpenAI Codex",
    )
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    build_pdf()
