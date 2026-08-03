from datetime import date, datetime, timezone

from arxiv_wiki.markdown import render_daily
from arxiv_wiki.models import Paper, PaperAnalysis, RankedPaper


def test_markdown_contains_public_links_and_sections():
    now = datetime.now(timezone.utc)
    paper = Paper(
        arxiv_id="2608.00001v1",
        title="Example Paper",
        authors=["A. Author"],
        summary="Abstract",
        published=now,
        updated=now,
        categories=["cs.AI"],
        primary_category="cs.AI",
        abstract_url="https://arxiv.org/abs/2608.00001",
        pdf_url="https://arxiv.org/pdf/2608.00001",
    )
    analysis = PaperAnalysis(
        one_line_summary="한 줄 요약",
        problem="문제",
        contributions=["기여"],
        method="방법",
        results=["결과"],
        limitations=["한계"],
        developer_takeaways=["시사점"],
        keywords=["LLM"],
        confidence_note="제목과 초록 기반",
    )
    markdown = render_daily(
        [RankedPaper(paper=paper, score=9, score_reasons=["test"], analysis=analysis)],
        date(2026, 8, 3),
    )
    assert "https://arxiv.org/abs/2608.00001" in markdown
    assert "### 개발자 관점" in markdown
