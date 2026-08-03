from __future__ import annotations

import argparse
import json
import os
from datetime import date
from pathlib import Path

from .analyzer import analyze_paper
from .arxiv_client import fetch_recent_papers
from .markdown import render_daily, write_daily
from .ranking import rank_papers

DEFAULT_CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.CV", "cs.SE", "cs.DC"]


def run(args: argparse.Namespace) -> Path:
    papers = fetch_recent_papers(args.categories, args.lookback_hours, args.max_results)
    ranked = rank_papers(papers, args.limit)
    if not ranked:
        raise RuntimeError("선택할 신규 논문이 없습니다. lookback-hours를 늘려 보십시오.")

    for item in ranked:
        if args.no_llm:
            continue
        item.analysis = analyze_paper(item.paper, args.model)

    today = date.today()
    output_dir = Path(args.output_dir)
    path = write_daily(render_daily(ranked, today), output_dir, today)

    state_path = Path("data/last_run.json")
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps({"date": today.isoformat(), "papers": [x.paper.arxiv_id for x in ranked]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily arXiv AI Top 10 Markdown")
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
    print(path)


if __name__ == "__main__":
    main()
