from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import RankedPaper


def _bullets(items: list[str], fallback: str = "초록만으로 확인하기 어렵다.") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {fallback}"


def render_daily(ranked: list[RankedPaper], target_date: date) -> str:
    lines = [
        f"# {target_date.isoformat()} arXiv AI Top 10",
        "",
        "> arXiv 신규 AI 논문 가운데 최근성, 주제 적합성, 개발자 관심도를 기준으로 자동 선별한 일일 요약이다.",
        "> 순위는 학술적 품질의 절대 평가가 아니며, 분석은 제목과 초록에 기반한다.",
        "",
        "## 오늘의 목록",
        "",
    ]
    for index, item in enumerate(ranked, 1):
        lines.append(f"{index}. [{item.paper.title}](#{index}-{_anchor(item.paper.title)})")
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


def write_daily(markdown: str, output_dir: Path, target_date: date) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{target_date.isoformat()}.md"
    path.write_text(markdown, encoding="utf-8")
    latest = output_dir.parent / "latest.md"
    latest.write_text(markdown, encoding="utf-8")
    return path
