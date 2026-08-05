from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path

from .analyzer import analyze_paper
from .arxiv_client import fetch_recent_papers
from .markdown import render_daily, write_daily
from .ranking import rank_papers

DEFAULT_CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.CV", "cs.SE", "cs.DC"]
ARXIV_ID_PATTERN = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)


def normalize_arxiv_id(value: str) -> str:
    """Return a version-independent arXiv ID such as 2608.02391."""
    match = ARXIV_ID_PATTERN.search(value)
    return match.group(1) if match else value.strip().lower()


def load_seen_arxiv_ids(output_dir: Path, state_path: Path) -> set[str]:
    """Load paper IDs already published in prior daily pages or state files."""
    seen: set[str] = set()

    if output_dir.exists():
        for markdown_path in output_dir.glob("*.md"):
            if markdown_path.name == "index.md":
                continue
            text = markdown_path.read_text(encoding="utf-8")
            seen.update(normalize_arxiv_id(match.group(0)) for match in ARXIV_ID_PATTERN.finditer(text))

    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            state = {}
        for paper_id in state.get("papers", []):
            seen.add(normalize_arxiv_id(str(paper_id)))
        for paper_id in state.get("seen_papers", []):
            seen.add(normalize_arxiv_id(str(paper_id)))

    return seen


def run(args: argparse.Namespace) -> Path | None:
    output_dir = Path(args.output_dir)
    state_path = Path("data/last_run.json")
    seen_ids = load_seen_arxiv_ids(output_dir, state_path)

    papers = fetch_recent_papers(args.categories, args.lookback_hours, args.max_results)
    new_papers = [paper for paper in papers if normalize_arxiv_id(paper.arxiv_id) not in seen_ids]
    ranked = rank_papers(new_papers, args.limit)

    if not ranked:
        print("새로 등록된 미처리 논문이 없습니다. 기존 아카이브와 중복된 논문은 제외했습니다.")
        return None

    for item in ranked:
        if args.no_llm:
            continue
        item.analysis = analyze_paper(item.paper, args.model)

    today = date.today()
    path = write_daily(render_daily(ranked, today), output_dir, today)

    newly_processed = {normalize_arxiv_id(item.paper.arxiv_id) for item in ranked}
    all_seen = sorted(seen_ids | newly_processed)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "date": today.isoformat(),
                "papers": [item.paper.arxiv_id for item in ranked],
                "seen_papers": all_seen,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily arXiv AI summaries")
    parser.add_argument("--categories", nargs="+", default=DEFAULT_CATEGORIES)
    parser.add_argument("--lookback-hours", type=int, default=72)
    parser.add_argument("--max-results", type=int, default=200)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", default="docs/daily")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL"))
    parser.add_argument("--no-llm", action="store_true", help="Generate from abstracts without OpenAI analysis")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    path = run(args)
    if path is not None:
        print(path)


if __name__ == "__main__":
    main()
