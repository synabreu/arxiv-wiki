from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .models import RankedPaper


def _bullets(items: list[str], fallback: str = "초록만으로 확인하기 어렵다.") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {fallback}"


def render_daily(ranked: list[RankedPaper], target_date: date) -> str:
    count = len(ranked)
    lines = [
        f"# {target_date.isoformat()} arXiv AI Top {count}",
        "",
        "> arXiv 신규 AI 논문 가운데 최근성, 주제 적합성, 개발자 관심도를 기준으로 자동 선별한 일일 요약이다.",
        "> 순위는 학술적 품질의 절대 평가가 아니며, 분석은 제목과 초록에 기반한다.",
        "",
        "[← 일별 아카이브로 돌아가기](index.md)",
        "",
        "## 오늘의 목록",
        "",
        "| 순위 | 논문 제목 | 원문 |",
        "|---:|---|---|",
    ]
    for index, item in enumerate(ranked, 1):
        title = _escape_table(item.paper.title)
        lines.append(
            f"| {index} | [{title}](#{index}-{_anchor(item.paper.title)}) | "
            f"[arXiv]({item.paper.abstract_url}) · [PDF]({item.paper.pdf_url}) |"
        )
    lines.append("")

    for index, item in enumerate(ranked, 1):
        paper = item.paper
        analysis = item.analysis
        lines += [
            f"## {index}. {paper.title}",
            "",
            f"- **arXiv:** [{paper.arxiv_id}]({paper.abstract_url}) · [PDF]({paper.pdf_url})",
            f"- **저자:** {', '.join(paper.authors)}",
            f"- **분야:** {', '.join(paper.categories)}",
            f"- **선정 점수:** {item.score:.2f}",
            f"- **선정 이유:** {', '.join(item.score_reasons[:5])}",
            "",
        ]
        if analysis is None:
            lines += ["### 초록", "", paper.summary, ""]
            continue
        lines += [
            "### 한 문장 요약", "", analysis.one_line_summary, "",
            "### 해결하려는 문제", "", analysis.problem, "",
            "### 핵심 기여", "", _bullets(analysis.contributions), "",
            "### 접근 방법", "", analysis.method, "",
            "### 주요 결과", "", _bullets(analysis.results), "",
            "### 한계", "", _bullets(analysis.limitations), "",
            "### 개발자 관점", "", _bullets(analysis.developer_takeaways), "",
            f"**근거 범위:** {analysis.confidence_note}", "",
        ]
    return "\n".join(lines).strip() + "\n"


def _anchor(title: str) -> str:
    return "-".join("".join(ch.lower() if ch.isalnum() or ch.isspace() else "" for ch in title).split())


def _escape_table(text: str) -> str:
    return text.replace("|", "\\|")


def _papers_from_daily(path: Path) -> list[tuple[str, str]]:
    """Return (title, arXiv URL) pairs from one generated daily Markdown file."""
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## \d+\. ", text)[1:]
    papers: list[tuple[str, str]] = []
    for section in sections:
        title = section.splitlines()[0].strip()
        match = re.search(r"(?m)^- \*\*arXiv:\*\* \[[^]]+\]\((https?://[^)]+)\)", section)
        papers.append((title, match.group(1) if match else ""))
    return papers


def write_archive_index(output_dir: Path) -> Path:
    lines = [
        "# 일별 arXiv AI 논문 아카이브",
        "",
        "날짜별로 선별된 AI 논문과 원문 링크를 확인할 수 있다.",
        "",
        "[← 홈으로 돌아가기](../index.md)",
        "",
        "| 날짜 | 논문 제목 | 원문 |",
        "|---|---|---|",
    ]

    for path in sorted(output_dir.glob("????-??-??.md"), reverse=True):
        target_date = path.stem
        papers = _papers_from_daily(path)
        if not papers:
            lines.append(f"| [{target_date}]({path.name}) | 요약 보기 | - |")
            continue
        for title, arxiv_url in papers:
            detail_url = f"{path.name}#{_anchor(title)}"
            # GitHub Pages prefixes numbered headings with the ranking number.
            text = path.read_text(encoding="utf-8")
            heading_match = re.search(rf"(?m)^## (\d+)\. {re.escape(title)}$", text)
            if heading_match:
                detail_url = f"{path.name}#{heading_match.group(1)}-{_anchor(title)}"
            original = f"[arXiv]({arxiv_url})" if arxiv_url else "-"
            lines.append(
                f"| [{target_date}]({path.name}) | [{_escape_table(title)}]({detail_url}) | {original} |"
            )

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return index_path


def write_daily(markdown: str, output_dir: Path, target_date: date) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{target_date.isoformat()}.md"
    path.write_text(markdown, encoding="utf-8")
    latest = output_dir.parent / "latest.md"
    latest.write_text(markdown, encoding="utf-8")
    write_archive_index(output_dir)
    return path
