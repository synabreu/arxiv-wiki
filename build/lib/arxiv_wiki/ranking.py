from __future__ import annotations

import math
import re
from datetime import UTC, datetime

from .models import Paper, RankedPaper
from .scholarly import ScholarlySignals

AI_KEYWORD_WEIGHTS = {
    "large language model": 0.9,
    "llm": 0.8,
    "agent": 0.7,
    "reasoning": 0.6,
    "inference": 0.5,
    "multimodal": 0.6,
    "mixture of experts": 0.6,
    "retrieval augmented": 0.5,
    "rag": 0.4,
    "alignment": 0.4,
    "machine learning": 0.4,
    "neural network": 0.4,
}

CATEGORY_WEIGHTS = {
    "cs.AI": 1.5,
    "cs.CL": 1.5,
    "cs.LG": 1.4,
    "cs.CV": 1.1,
    "cs.SE": 0.9,
    "cs.DC": 0.8,
}

DEVELOPER_SIGNALS = {
    "open source": 0.4,
    "open-source": 0.4,
    "code": 0.25,
    "repository": 0.3,
    "agent": 0.25,
    "tool use": 0.3,
    "tool-use": 0.3,
    "inference": 0.25,
    "efficient": 0.25,
    "latency": 0.3,
    "memory": 0.2,
    "deployment": 0.3,
}

ACADEMIC_SIGNALS = {
    "benchmark": 0.25,
    "baseline": 0.25,
    "ablation": 0.3,
    "dataset": 0.2,
    "evaluation": 0.2,
    "experiment": 0.2,
    "theorem": 0.3,
    "proof": 0.3,
    "reproduc": 0.25,
    "statistical": 0.2,
}

# Labs/model families that are especially relevant to open-weight AI development.
# The scorer only uses public title/abstract text, so these are transparent keyword
# boosts rather than inferred author affiliations.
OPEN_WEIGHT_LAB_SIGNALS = {
    "nvidia": 1.4,
    "nemotron": 1.2,
    "openai": 1.0,
    "gpt-oss": 1.5,
    "alibaba": 1.4,
    "qwen": 1.5,
    "deepseek": 1.6,
    "moonshot ai": 1.4,
    "moonshot": 1.2,
    "kimi": 1.6,
    "meta": 0.8,
    "llama": 1.2,
    "mistral": 1.2,
    "zhipu": 1.1,
    "glm": 1.0,
}

OPEN_WEIGHT_RELEASE_SIGNALS = {
    "open weight": 1.6,
    "open-weight": 1.6,
    "open weights": 1.6,
    "open-weights": 1.6,
    "open model": 1.0,
    "open-model": 1.0,
    "model weights": 1.1,
    "weights released": 1.2,
    "release weights": 1.2,
    "checkpoint": 0.6,
    "checkpoints": 0.6,
    "hugging face": 0.5,
    "apache 2.0": 0.7,
    "mit license": 0.6,
}


def _contains(text: str, phrase: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) is not None


def _sum_present(text: str, weights: dict[str, float], cap: float) -> float:
    return min(sum(weight for term, weight in weights.items() if _contains(text, term)), cap)


def rank_papers(
    papers: list[Paper],
    limit: int = 5,
    scholarly_signals: dict[str, ScholarlySignals] | None = None,
    now: datetime | None = None,
) -> list[RankedPaper]:
    """Rank papers with transparent, capped signals suited to daily curation.

    In addition to recency, scholarly impact, AI fit and developer relevance,
    prioritize papers explicitly tied in the title/abstract to major open-weight
    labs/model families or to public weight/checkpoint releases.
    """
    current_time = now or datetime.now(UTC)
    signals_by_id = scholarly_signals or {}
    ranked: list[RankedPaper] = []

    for paper in papers:
        text = f"{paper.title} {paper.summary}".lower()
        signals = signals_by_id.get(paper.arxiv_id, ScholarlySignals())

        age_hours = max((current_time - paper.published).total_seconds() / 3600, 0)
        recency = max(0.0, 2.5 - math.log1p(age_hours) / 2.0)

        citation_impact = min(2.0, math.log1p(signals.citation_count) / 2.3)
        citation_impact += min(
            0.5, math.log1p(signals.influential_citation_count) / 2.0
        )

        author_impact = min(1.5, math.log1p(signals.max_author_h_index) / 2.5)
        author_impact += min(
            0.5, math.log1p(signals.max_author_citation_count) / 8.0
        )

        category_score = max(
            (CATEGORY_WEIGHTS.get(category, 0.0) for category in paper.categories),
            default=0.0,
        )
        ai_fit = min(category_score + _sum_present(text, AI_KEYWORD_WEIGHTS, 1.5), 3.0)
        developer_interest = _sum_present(text, DEVELOPER_SIGNALS, 1.5)
        academic_quality = _sum_present(text, ACADEMIC_SIGNALS, 1.5)
        if len(paper.summary) >= 800:
            academic_quality = min(academic_quality + 0.3, 1.8)

        open_weight_lab = _sum_present(text, OPEN_WEIGHT_LAB_SIGNALS, 2.5)
        open_weight_release = _sum_present(text, OPEN_WEIGHT_RELEASE_SIGNALS, 2.5)
        open_weight_focus = min(open_weight_lab + open_weight_release, 4.0)

        score = (
            recency
            + citation_impact
            + author_impact
            + ai_fit
            + developer_interest
            + academic_quality
            + open_weight_focus
        )
        reasons = [
            f"최근성 {recency:.1f}",
            f"인용 영향 {citation_impact:.1f} (인용 {signals.citation_count}회)",
            f"저자 영향 {author_impact:.1f} (최고 h-index {signals.max_author_h_index})",
            f"AI 주제 적합성 {ai_fit:.1f}",
            f"개발자 관심 {developer_interest:.1f}",
            f"학술 신호 {academic_quality:.1f}",
            f"오픈 웨이트·주요 연구조직 신호 {open_weight_focus:.1f}",
        ]
        ranked.append(
            RankedPaper(paper=paper, score=round(score, 2), score_reasons=reasons)
        )

    return sorted(
        ranked,
        key=lambda item: (
            -item.score,
            -signals_by_id.get(item.paper.arxiv_id, ScholarlySignals()).citation_count,
            -signals_by_id.get(
                item.paper.arxiv_id, ScholarlySignals()
            ).max_author_h_index,
            -item.paper.published.timestamp(),
        ),
    )[:limit]
