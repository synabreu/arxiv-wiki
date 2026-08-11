from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import pymupdf

from .pdf import download_pdf

# Only accept captions that explicitly start with "Figure".
# Excludes "Fig.", "Table", and ordinary sentences that merely mention a figure.
CAPTION_RE = re.compile(
    r"(?im)^\s*Figure\s+([0-9]+|[ivx]+)\s*[:.]\s*([^\n]{1,220})"
)


@dataclass(frozen=True)
class PaperVisual:
    image_path: str
    caption: str
    page_number: int
    kind: str = "figure"


def _caption(text: str) -> str:
    return " ".join(text.split())[:300]


def _intersection_area(first: pymupdf.Rect, second: pymupdf.Rect) -> float:
    intersection = first & second
    if intersection.is_empty:
        return 0.0
    return max(0.0, intersection.width) * max(0.0, intersection.height)


def _has_graphic_content(page: pymupdf.Page, clip: pymupdf.Rect) -> bool:
    """Return True only when the candidate region contains an image or drawing.

    This prevents a caption and surrounding prose from being exported as a
    misleading "visual" when the selected region contains text only.
    """
    clip_area = max(1.0, clip.width * clip.height)

    for image in page.get_images(full=True):
        xref = image[0]
        for image_rect in page.get_image_rects(xref):
            if _intersection_area(image_rect, clip) >= clip_area * 0.03:
                return True

    drawing_area = 0.0
    for drawing in page.get_drawings():
        drawing_rect = pymupdf.Rect(drawing["rect"])
        drawing_area += _intersection_area(drawing_rect, clip)
        if drawing_area >= clip_area * 0.04:
            return True

    return False


def extract_key_visuals(
    pdf_url: str,
    slug: str,
    docs_dir: Path,
    limit: int = 3,
) -> list[PaperVisual]:
    document = pymupdf.open(stream=download_pdf(pdf_url), filetype="pdf")

    output_dir = docs_dir / "assets" / "papers" / slug
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    found: list[PaperVisual] = []
    seen: set[tuple[int, str]] = set()

    try:
        for page_index, page in enumerate(document):
            for block in page.get_text("blocks"):
                block_text = str(block[4]).strip()
                match = CAPTION_RE.match(block_text)
                if not match:
                    continue

                caption = _caption(match.group(0))
                key = (page_index, caption.lower())
                if key in seen:
                    continue
                seen.add(key)

                caption_rect = pymupdf.Rect(block[0], block[1], block[2], block[3])
                page_rect = page.rect
                margin = page_rect.width * 0.04
                clip = pymupdf.Rect(
                    page_rect.x0 + margin,
                    max(page_rect.y0, caption_rect.y0 - page_rect.height * 0.52),
                    page_rect.x1 - margin,
                    min(page_rect.y1, caption_rect.y1 + 15),
                )

                if clip.width < 100 or clip.height < 100:
                    continue
                if not _has_graphic_content(page, clip):
                    continue

                name = f"figure-{len(found) + 1}.jpg"
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(1.6, 1.6),
                    clip=clip,
                    alpha=False,
                )
                pixmap.save(str(output_dir / name), jpg_quality=84)
                found.append(
                    PaperVisual(
                        image_path=f"../assets/papers/{slug}/{name}",
                        caption=caption,
                        page_number=page_index + 1,
                    )
                )

                if len(found) >= limit:
                    return found
    finally:
        document.close()

    return found


def render_visuals(visuals: list[PaperVisual]) -> str:
    if not visuals:
        return ""

    lines = [
        "<!-- paper-visuals:start -->",
        "## 주요 Figure",
        "",
        "> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.",
        "",
    ]
    for visual in visuals:
        lines.extend(
            [
                f"![{visual.caption}]({visual.image_path})",
                "",
                f"*Figure · 원문 PDF {visual.page_number}쪽 · {visual.caption}*",
                "",
            ]
        )
    lines.append("<!-- paper-visuals:end -->")
    return "\n".join(lines).strip() + "\n"


def insert_visuals(markdown: str, visuals: list[PaperVisual]) -> str:
    """Place valid Figure visuals after the developer perspective.

    Existing visual blocks are always removed first. Therefore old Table,
    Fig., or text-only entries disappear even when no valid Figure is found.
    """
    cleaned = re.sub(
        r"\n?<!-- paper-visuals:start -->.*?<!-- paper-visuals:end -->\n?",
        "\n",
        markdown,
        flags=re.DOTALL,
    )

    block = render_visuals(visuals)
    if not block:
        return cleaned.strip() + "\n"

    confidence_marker = "\n**근거 범위:**"
    if confidence_marker in cleaned:
        return cleaned.replace(
            confidence_marker,
            f"\n{block}\n**근거 범위:**",
            1,
        )

    navigation_marker = "\n---\n"
    if navigation_marker in cleaned:
        return cleaned.replace(
            navigation_marker,
            f"\n{block}\n---\n",
            1,
        )

    return cleaned.rstrip() + "\n\n" + block
