from __future__ import annotations

import json
import os

from openai import OpenAI

from .models import Paper, PaperAnalysis

SYSTEM_PROMPT = """당신은 AI 논문을 일반 사용자와 개발자 모두에게 설명하는 기술 편집자다.
반드시 제공된 제목과 초록에 근거해 작성한다. 확인되지 않은 수치, 결과, 구현 세부사항은 만들지 않는다.
초록만으로 알 수 없는 내용은 명확히 '초록만으로 확인하기 어렵다'고 표시한다.
출력은 요청된 JSON 스키마를 따라야 하며 한국어 평서체로 작성한다."""


def analyze_paper(paper: Paper, model: str | None = None) -> PaperAnalysis:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
    prompt = f"""다음 arXiv 논문을 분석한다.

제목: {paper.title}
저자: {', '.join(paper.authors)}
분야: {', '.join(paper.categories)}
초록: {paper.summary}

일반 사용자도 이해할 수 있는 표현을 사용하되, 개발자 시사점은 구체적으로 작성한다."""
    response = client.responses.parse(
        model=selected_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        text_format=PaperAnalysis,
    )
    if response.output_parsed is None:
        raise RuntimeError(f"Structured output missing: {json.dumps(response.model_dump(), ensure_ascii=False)[:500]}")
    return response.output_parsed
