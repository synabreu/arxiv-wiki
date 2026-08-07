from datetime import UTC, datetime, timedelta

from arxiv_wiki.models import Paper
from arxiv_wiki.ranking import rank_papers
from arxiv_wiki.scholarly import ScholarlySignals

NOW = datetime(2026, 8, 7, tzinfo=UTC)


def paper(
    paper_id: str,
    title: str,
    summary: str,
    category: str = "cs.AI",
    age_hours: int = 1,
) -> Paper:
    published = NOW - timedelta(hours=age_hours)
    return Paper(
        arxiv_id=paper_id,
        title=title,
        authors=["A. Researcher"],
        summary=summary,
        published=published,
        updated=published,
        categories=[category],
        primary_category=category,
        abstract_url=f"https://arxiv.org/abs/{paper_id}",
        pdf_url=f"https://arxiv.org/pdf/{paper_id}",
    )


def test_llm_paper_ranks_above_unrelated_paper():
    llm = paper(
        "2608.00001v1",
        "Efficient LLM Inference",
        "A new large language model inference method.",
    )
    other = paper(
        "2608.00002v1",
        "Generic Optimization",
        "A generic numerical optimization method.",
        "math.OC",
    )
    ranked = rank_papers([other, llm], limit=2, now=NOW)
    assert ranked[0].paper.title == llm.title


def test_citations_and_author_impact_raise_otherwise_equal_paper():
    established = paper("2608.00003v1", "Method A", "An AI evaluation method.")
    unknown = paper("2608.00004v1", "Method B", "An AI evaluation method.")
    signals = {
        established.arxiv_id: ScholarlySignals(
            citation_count=120,
            influential_citation_count=15,
            max_author_h_index=70,
            max_author_citation_count=25000,
        )
    }

    ranked = rank_papers(
        [unknown, established], limit=2, scholarly_signals=signals, now=NOW
    )

    assert ranked[0].paper.arxiv_id == established.arxiv_id
    assert "인용 120회" in ranked[0].score_reasons[1]
    assert "h-index 70" in ranked[0].score_reasons[2]


def test_recent_reproducible_developer_paper_gets_quality_signals():
    strong = paper(
        "2608.00005v1",
        "Open-source Agent Benchmark",
        "We release code and a dataset, compare baselines, run ablation experiments, "
        "and evaluate tool use latency for an AI agent.",
    )
    weak = paper(
        "2608.00006v1",
        "An AI Idea",
        "We describe an AI idea.",
        age_hours=24,
    )

    ranked = rank_papers([weak, strong], limit=2, now=NOW)

    assert ranked[0].paper.arxiv_id == strong.arxiv_id
    assert any(reason.startswith("개발자 관심") for reason in ranked[0].score_reasons)
    assert any(reason.startswith("학술 신호") for reason in ranked[0].score_reasons)


def test_default_limit_is_top_five():
    papers = [
        paper(f"2608.{index:05d}v1", f"AI Paper {index}", "AI method")
        for index in range(7)
    ]
    assert len(rank_papers(papers, now=NOW)) == 5
