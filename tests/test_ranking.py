from datetime import datetime, timezone

from arxiv_wiki.models import Paper
from arxiv_wiki.ranking import rank_papers


def paper(title: str, summary: str, category: str = "cs.AI") -> Paper:
    now = datetime.now(timezone.utc)
    return Paper(
        arxiv_id="2608.00001v1",
        title=title,
        authors=["A. Researcher"],
        summary=summary,
        published=now,
        updated=now,
        categories=[category],
        primary_category=category,
        abstract_url="https://arxiv.org/abs/2608.00001",
        pdf_url="https://arxiv.org/pdf/2608.00001",
    )


def test_llm_paper_ranks_above_unrelated_paper():
    llm = paper("Efficient LLM Inference", "A new large language model inference method.")
    other = paper("Generic Optimization", "A generic numerical optimization method.", "math.OC")
    ranked = rank_papers([other, llm], limit=2)
    assert ranked[0].paper.title == llm.title
