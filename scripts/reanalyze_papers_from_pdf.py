from __future__ import annotations

import argparse
import re
from datetime import UTC, datetime
from pathlib import Path

from arxiv_wiki.analyzer import analyze_paper
from arxiv_wiki.models import Paper


def _match(pattern: str, text: str, fallback: str = "") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def _replace_section(text: str, heading: str, body: str) -> str:
    pattern = rf"(?ms)^(##|###) {re.escape(heading)}\s*\n.*?(?=^(?:##|###) |^\*\*근거 범위:\*\*|^---$|\Z)"
    replacement = f"### {heading}\n\n{body.strip()}\n\n"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)

    confidence = "\n**근거 범위:**"
    if confidence in text:
        return text.replace(confidence, f"\n{replacement}**근거 범위:**", 1)
    return text.rstrip() + "\n\n" + replacement


def _bullets(items: list[str], fallback: str) -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {fallback}"


def parse_paper(path: Path) -> Paper:
    text = path.read_text(encoding="utf-8")
    title = _match(r"^# (.+)$", text, path.stem)
    arxiv_id = _match(r"\*\*arXiv:\*\* \[([^]]+)\]", text)
    abstract_url = _match(r"\*\*arXiv:\*\* \[[^]]+\]\(([^)]+)\)", text)
    pdf_url = _match(r"\[PDF\]\(([^)]+)\)", text)
    authors = [item.strip() for item in _match(r"\*\*저자:\*\* (.+)$", text).split(",") if item.strip()]
    categories = [item.strip() for item in _match(r"\*\*분야:\*\* (.+)$", text).split(",") if item.strip()]
    summary = _match(
        r"(?ms)^(?:##|###) 한 문장 요약\s*\n(.+?)(?=^(?:##|###) )",
        text,
        "기존 상세 페이지를 PDF 본문 기반으로 다시 분석한다.",
    )
    now = datetime.now(UTC)
    return Paper(
        arxiv_id=arxiv_id,
        title=title,
        authors=authors,
        summary=summary,
        published=now,
        updated=now,
        categories=categories,
        primary_category=categories[0] if categories else "cs.AI",
        abstract_url=abstract_url,
        pdf_url=pdf_url,
    )


def update_page(path: Path, model: str | None) -> None:
    original = path.read_text(encoding="utf-8")
    paper = parse_paper(path)
    if not paper.pdf_url:
        print(f"skip {path.name}: PDF URL missing")
        return

    analysis = analyze_paper(paper, model)
    updated = original
    updated = _replace_section(updated, "한 문장 요약", analysis.one_line_summary)
    updated = _replace_section(updated, "해결하려는 문제", analysis.problem)
    updated = _replace_section(updated, "핵심 기여", _bullets(analysis.contributions, "본문에서 확인하기 어렵다."))
    updated = _replace_section(updated, "접근 방법", analysis.method)
    updated = _replace_section(updated, "주요 결과", _bullets(analysis.results, "본문에서 정량 결과를 확인하기 어렵다."))
    updated = _replace_section(updated, "한계", _bullets(analysis.limitations, "논문에서 명시적 한계를 확인하기 어렵다."))
    updated = _replace_section(updated, "개발자 관점", _bullets(analysis.developer_takeaways, "추가 재현 검증이 필요하다."))
    updated = re.sub(
        r"\*\*근거 범위:\*\*.*?(?=\n---|\Z)",
        f"**근거 범위:** {analysis.confidence_note}\n",
        updated,
        count=1,
        flags=re.DOTALL,
    )
    path.write_text(updated, encoding="utf-8")
    print(f"updated {path.name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers-dir", default="docs/papers")
    parser.add_argument("--model", default=None)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    paths = sorted(Path(args.papers_dir).glob("*.md"))
    if args.limit > 0:
        paths = paths[: args.limit]
    for path in paths:
        try:
            update_page(path, args.model)
        except Exception as exc:
            print(f"failed {path.name}: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
