from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz
import requests

CAPTION_RE = re.compile(
    r"(?im)^\s*(figure|fig\.?|table)\s+([0-9]+|[ivx]+)\s*[:.]\s*([^\n]{0,220})"
)


@dataclass(frozen=True)
class PaperVisual:
    image_path: str
    caption: str
    page_number: int
    kind: str


def _caption(text: str) -> str:
    return " ".join(text.split())[:300]


def extract_key_visuals(pdf_url: str, slug: str, docs_dir: Path, limit: int = 3) -> list[PaperVisual]:
    response = requests.get(pdf_url, timeout=90)
    response.raise_for_status()
    document = fitz.open(stream=response.content, filetype="pdf")
    output_dir = docs_dir / "assets" / "papers" / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    found: list[PaperVisual] = []
    seen: set[tuple[int, str]] = set()
    for page_index, page in enumerate(document):
        for block in page.get_text("blocks"):
            match = CAPTION_RE.search(str(block[4]))
            if not match:
                continue
            caption = _caption(match.group(0))
            key = (page_index, caption.lower())
            if key in seen:
                continue
            seen.add(key)

            kind = "table" if match.group(1).lower().startswith("table") else "figure"
            caption_rect = fitz.Rect(block[0], block[1], block[2], block[3])
            page_rect = page.rect
            margin = page_rect.width * 0.04
            if kind == "table":
                clip = fitz.Rect(
                    page_rect.x0 + margin,
                    max(page_rect.y0, caption_rect.y0 - 15),
                    page_rect.x1 - margin,
                    min(page_rect.y1, caption_rect.y1 + page_rect.height * 0.48),
                )
            else:
                clip = fitz.Rect(
                    page_rect.x0 + margin,
                    max(page_rect.y0, caption_rect.y0 - page_rect.height * 0.52),
                    page_rect.x1 - margin,
                    min(page_rect.y1, caption_rect.y1 + 15),
                )
            if clip.width < 100 or clip.height < 100:
                continue

            name = f"visual-{len(found) + 1}.jpg"
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), clip=clip, alpha=False)
            pixmap.save(str(output_dir / name), jpg_quality=84)
            found.append(
                PaperVisual(
                    image_path=f"../assets/papers/{slug}/{name}",
                    caption=caption,
                    page_number=page_index + 1,
                    kind=kind,
                )
            )
            if len(found) >= limit:
                document.close()
                return found

    document.close()
    return found


def render_visuals(visuals: list[PaperVisual]) -> str:
    if not visuals:
        return ""
    lines = [
        "<!-- paper-visuals:start -->",
        "## 주요 그림·그래프·표",
        "",
        "> 원문 PDF에서 자동 추출한 자료다. 정확한 해석은 원문 캡션과 본문을 함께 확인해야 한다.",
        "",
    ]
    for visual in visuals:
        label = "표" if visual.kind == "table" else "그림·그래프"
        lines.extend([
            f"![{visual.caption}]({visual.image_path})",
            "",
            f"*{label} · 원문 PDF {visual.page_number}쪽 · {visual.caption}*",
            "",
        ])
    lines.append("<!-- paper-visuals:end -->")
    return "\n".join(lines).strip() + "\n"


def insert_visuals(markdown: str, visuals: list[PaperVisual]) -> str:
    """Place visuals after the developer perspective and before the evidence note."""
    block = render_visuals(visuals)
    if not block:
        return markdown

    cleaned = re.sub(
        r"\n?<!-- paper-visuals:start -->.*?<!-- paper-visuals:end -->\n?",
        "\n",
        markdown,
        flags=re.DOTALL,
    )

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
