import re
from datetime import UTC, date, datetime
from pathlib import Path

from arxiv_wiki.markdown import render_method, render_paper_detail
from arxiv_wiki.models import Paper, PaperAnalysis, RankedPaper


def test_markdown_contains_public_links_and_sections():
    now = datetime.now(UTC)
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
    markdown = render_paper_detail(
        RankedPaper(paper=paper, score=9, score_reasons=["test"], analysis=analysis),
        date(2026, 8, 3),
    )
    assert "https://arxiv.org/abs/2608.00001" in markdown
    assert "## 개발자 관점" in markdown


def test_method_markdown_table_is_rendered_as_bullets():
    method = """| 단계 | 설명 |
|---|---|
| 행동 | 도구를 호출한다. |
| 관찰 | 결과를 상태에 반영한다. |"""

    rendered = render_method(method)

    assert "|---|" not in rendered
    assert "* **행동:** 도구를 호출한다." in rendered
    assert "* **관찰:** 결과를 상태에 반영한다." in rendered


def test_method_escapes_equation_pipes_that_kramdown_treats_as_a_table():
    rendered = render_method("행동은 πθ(·|ht, ACT), 관찰은 πθ(·|ht, at, REHEARSE)로 생성한다.")

    assert rendered == "* 행동은 πθ(·\\|ht, ACT), 관찰은 πθ(·\\|ht, at, REHEARSE)로 생성한다."


def test_method_is_split_into_one_sentence_star_bullets():
    rendered = render_method("첫 번째 절차를 수행한다. 두 번째 절차를 수행한다. 결과를 확인한다.")

    assert rendered.splitlines() == [
        "* 첫 번째 절차를 수행한다.",
        "* 두 번째 절차를 수행한다.",
        "* 결과를 확인한다.",
    ]


def test_existing_paper_methods_do_not_contain_unescaped_pipes():
    for path in Path("docs/papers").glob("*.md"):
        markdown = path.read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^###? 접근 방법\s*\n(?P<body>.*?)(?=^###? |^\*\*근거 범위:\*\*|^---$|\Z)",
            markdown,
        )
        if match:
            body = match.group("body").strip()
            assert not re.search(r"(?<!\\)\|", body), path
            assert all(line.startswith("* ") for line in body.splitlines() if line.strip()), path
            assert render_method(body) == body, path
