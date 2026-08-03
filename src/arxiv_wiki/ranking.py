from __future__ import annotations

import math
import re
from datetime import datetime, timezone

from .models import Paper, RankedPaper

KEYWORD_WEIGHTS = {
    "large language model": 3.0,
    "llm": 2.5,
    "agent": 2.2,
    "reasoning": 2.0,
    "inference": 2.0,
    "multimodal": 1.8,
    "mixture of experts": 1.8,
    "retrieval augmented": 1.6,
    "rag": 1.4,
    "alignment": 1.4,
    "benchmark": 1.2,
    "efficient": 1.0,
    "scaling": 1.0,
}

CATEGORY_WEIGHTS = {
    "cs.AI": 2.0,
    "cs.CL": 2.0,
    "cs.LG": 1.8,
    "cs.CV": 1.3,
    "cs.SE": 1.1,
    "cs.DC": 1.1,
}


def rank_papers(papers: list[Paper], limit: int = 10) -> list[RankedPaper]:
    now = datetime.now(timezone.utc)
    ranked: list[RankedPaper] = []
    for paper in papers:
        text = f"{paper.title} {paper.summary}".lower()
        reasons: list[str] = []
        score = 0.0

        age_hours = max((now - paper.published).total_seconds() / 3600, 0)
        recency = max(0.0, 3.0 - math.log1p(age_hours) / 1.5)
        score += recency
        reasons.append(f"최근성 {recency:.1f}")

        for keyword, weight in KEYWORD_WEIGHTS.items():
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                score += weight
                reasons.append(f"핵심어: {keyword}")

        category_score = max((CATEGORY_WEIGHTS.get(c, 0.3) for c in paper.categories), default=0)
        score += category_score
        reasons.append(f"분야 가중치 {category_score:.1f}")

        if len(paper.summary) > 800:
            score += 0.4
            reasons.append("구체적인 초록")
        if any(token in text for token in ("state-of-the-art", "outperform", "open-source", "open source")):
            score += 0.7
            reasons.append("재현·성능 신호")

        ranked.append(RankedPaper(paper=paper, score=round(score, 2), score_reasons=reasons))

    return sorted(ranked, key=lambda item: (-item.score, item.paper.published))[:limit]
