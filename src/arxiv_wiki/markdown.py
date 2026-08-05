from __future__ import annotations

import re
import unicodedata
from datetime import date
from pathlib import Path

from .models import RankedPaper


def _bullets(items: list[str], fallback: str = "초록만으로 확인하기 어렵다.") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {fallback}"


def paper_filename(title: str) -> str:
    """Create a stable, URL-safe Markdown filename from a paper title."""
    normalized = unicodedata.normalize("NFKC", title).strip().lower()
    slug = re.sub(r"[^\w\s-]", "", normalized, flags=re.UNICODE)
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return f"{slug or 'paper'}.md"


def render_daily(ranked: list[RankedPaper], target_date: date) -> str:
    lines = [
        f"# {target_date.isoformat()} arXiv AI 논문",
        "",
        "> 오늘 새로 선별된 논문 목록이다. 제목을 누르면 상세 요약 페이지로 이동한다.",
        "",
        "[← 일별 아카이브로 돌아가기](index.md)",
        "",
        "## 오늘의 목록",
        "",
    ]
    for item in ranked:
        filename = paper_filename(item.paper.title)
        lines.append(f"- [{item.paper.title}](../papers/{filename})")
    return "\n".join(lines).strip() + "\n"


def render_paper_detail(item: RankedPaper, target_date: date) -> str:
    paper = item.paper
    analysis = item.analysis
    lines = [
        f"# {paper.title}",
        "",
        f"- **게시일:** {target_date.isoformat()}",
        f"- **arXiv:** [{paper.arxiv_id}]({paper.abstract_url}) · [PDF]({paper.pdf_url})",
        f"- **저자:** {', '.join(paper.authors)}",
        f"- **분야:** {', '.join(paper.categories)}",
        f"- **선정 점수:** {item.score:.2f}",
        f"- **선정 이유:** {', '.join(item.score_reasons[:5])}",
        "",
        f"[← {target_date.isoformat()} 목록으로 돌아가기](../daily/{target_date.isoformat()}.md)",
        "",
    ]
    if analysis is None:
        lines += ["## 초록", "", paper.summary, ""]
        return "\n".join(lines).strip() + "\n"

    lines += [
        "## 한 문장 요약", "", analysis.one_line_summary, "",
        "## 해결하려는 문제", "", analysis.problem, "",
        "## 핵심 기여", "", _bullets(analysis.contributions), "",
        "## 접근 방법", "", analysis.method, "",
        "## 주요 결과", "", _bullets(analysis.results), "",
        "## 한계", "", _bullets(analysis.limitations), "",
        "## 개발자 관점", "", _bullets(analysis.developer_takeaways), "",
        f"**근거 범위:** {analysis.confidence_note}", "",
    ]
    return "\n".join(lines).strip() + "\n"


def _escape_table(text: str) -> str:
    return text.replace("|", "\\|")


def _papers_from_daily(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    papers: list[tuple[str, str]] = []
    for match in re.finditer(r"(?m)^- \[([^]]+)\]\((\.\./papers/[^)]+)\)$", text):
        papers.append((match.group(1), match.group(2)))
    return papers


def write_archive_index(output_dir: Path) -> Path:
    lines = [
        "# 일별 arXiv AI 논문 아카이브",
        "",
        "날짜별 논문 제목을 선택하면 상세 요약 페이지로 이동한다.",
        "",
        "[← 홈으로 돌아가기](../index.md)",
        "",
        "| 날짜 | 논문 제목 |",
        "|---|---|",
    ]
    for path in sorted(output_dir.glob("????-??-??.md"), reverse=True):
        target_date = path.stem
        papers = _papers_from_daily(path)
        if not papers:
            lines.append(f"| [{target_date}]({path.name}) | 목록 보기 |")
            continue
        for title, detail_url in papers:
            lines.append(f"| [{target_date}]({path.name}) | [{_escape_table(title)}]({detail_url}) |")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return index_path


def write_daily(ranked: list[RankedPaper], output_dir: Path, target_date: date) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    papers_dir = output_dir.parent / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)

    daily_markdown = render_daily(ranked, target_date)
    path = output_dir / f"{target_date.isoformat()}.md"
    path.write_text(daily_markdown, encoding="utf-8")
    (output_dir.parent / "latest.md").write_text(daily_markdown, encoding="utf-8")

    for item in ranked:
        detail_path = papers_dir / paper_filename(item.paper.title)
        detail_path.write_text(render_paper_detail(item, target_date), encoding="utf-8")

    write_archive_index(output_dir)
    return path
