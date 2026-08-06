from __future__ import annotations

import json
import os
import re

import fitz
import requests
from openai import OpenAI

from .models import Paper, PaperAnalysis

SYSTEM_PROMPT = """당신은 AI 논문을 정밀하게 분석하는 기술 편집자다.
반드시 제공된 논문 PDF 본문을 중심으로 작성한다. 초록은 보조 정보로만 사용한다.
연구 문제, 방법, 실험 설정, 정량 결과, 한계와 개발자 시사점을 논문 본문에서 찾아 구체적으로 정리한다.
확인되지 않은 수치나 구현 세부사항은 만들지 않는다. 저자가 직접 언급한 한계와 본문에서 합리적으로 확인되는 한계를 구분한다.
출력은 요청된 JSON 스키마를 따르며 한국어 평서체로 작성한다."""


def _normalize_pdf_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(pdf_url: str, max_chars: int = 120_000) -> str:
    """Download an arXiv PDF and extract enough full-text context for analysis."""
    response = requests.get(pdf_url, timeout=120)
    response.raise_for_status()
    document = fitz.open(stream=response.content, filetype="pdf")
    pages: list[str] = []
    try:
        for page_number, page in enumerate(document, start=1):
            text = _normalize_pdf_text(page.get_text("text"))
            if text:
                pages.append(f"\n\n===== PDF PAGE {page_number} =====\n{text}")
    finally:
        document.close()

    full_text = "".join(pages).strip()
    if len(full_text) <= max_chars:
        return full_text

    # Preserve the beginning, experimental/results-heavy middle, and conclusion/end.
    head = full_text[:45_000]
    tail = full_text[-25_000:]
    keywords = re.compile(
        r"(?i)(experiment|evaluation|result|benchmark|ablation|limitation|discussion|conclusion)"
    )
    middle_chunks: list[str] = []
    for match in keywords.finditer(full_text):
        start = max(0, match.start() - 3_000)
        end = min(len(full_text), match.start() + 7_000)
        chunk = full_text[start:end]
        if chunk not in middle_chunks:
            middle_chunks.append(chunk)
        if sum(len(item) for item in middle_chunks) >= 45_000:
            break
    return "\n\n".join([head, *middle_chunks, tail])[:max_chars]


def analyze_paper(paper: Paper, model: str | None = None) -> PaperAnalysis:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")

    try:
        pdf_text = extract_pdf_text(paper.pdf_url)
        source_note = "논문 PDF 본문 전체에서 추출한 텍스트"
    except Exception as exc:
        pdf_text = paper.summary
        source_note = f"PDF 추출 실패로 초록 사용: {type(exc).__name__}"

    prompt = f"""다음 arXiv 논문을 분석한다.

제목: {paper.title}
저자: {', '.join(paper.authors)}
분야: {', '.join(paper.categories)}
초록: {paper.summary}
분석 근거: {source_note}

[논문 PDF 본문]
{pdf_text}

작성 기준:
1. 한 문장 요약은 논문의 목적과 핵심 방법을 함께 담는다.
2. 해결하려는 문제는 기존 방법의 한계와 연구 질문을 구체적으로 설명한다.
3. 핵심 기여는 논문 본문에 명시된 기여를 최대 5개로 정리한다.
4. 접근 방법은 아키텍처, 알고리즘, 학습·추론 절차를 본문 기준으로 설명한다.
5. 주요 결과는 데이터셋, 비교 기준, 정량 수치를 가능한 한 포함한다.
6. 한계는 저자가 밝힌 한계와 실험 범위에서 드러나는 제약을 구분해 작성한다.
7. 개발자 관점은 재현, 구현, 배포, 비용, 안전성 측면의 구체적 시사점을 작성한다.
8. confidence_note에는 '논문 PDF 본문 기반 분석'임을 명시하고, PDF 추출 범위나 확인하기 어려운 부분이 있으면 함께 적는다."""

    response = client.responses.parse(
        model=selected_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        text_format=PaperAnalysis,
    )
    if response.output_parsed is None:
        raise RuntimeError(
            f"Structured output missing: {json.dumps(response.model_dump(), ensure_ascii=False)[:500]}"
        )
    return response.output_parsed
