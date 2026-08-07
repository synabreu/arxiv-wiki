from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path

from .analyzer import analyze_paper
from .arxiv_client import fetch_recent_papers
from .markdown import write_daily
from .ranking import rank_papers
from .scholarly import fetch_scholarly_signals

DEFAULT_CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.CV", "cs.SE", "cs.DC"]
ARXIV_ID_PATTERN = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)


def normalize_arxiv_id(value: str) -> str:
    match = ARXIV_ID_PATTERN.search(value)
    return match.group(1) if match else value.strip().lower()


def load_seen_arxiv_ids(output_dir: Path, state_path: Path) -> set[str]:
    seen: set[str] = set()
    docs_root = output_dir.parent
    for markdown_dir in (output_dir, docs_root / "papers"):
        if not markdown_dir.exists():
            continue
        for markdown_path in markdown_dir.glob("*.md"):
            if markdown_path.name == "index.md":
                continue
            text = markdown_path.read_text(encoding="utf-8")
            seen.update(normalize_arxiv_id(match.group(0)) for match in ARXIV_ID_PATTERN.finditer(text))
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            state = {}
        for paper_id in state.get("papers", []) + state.get("seen_papers", []):
            seen.add(normalize_arxiv_id(str(paper_id)))
    return seen


def run(args: argparse.Namespace) -> Path | None:
    output_dir = Path(args.output_dir)
    state_path = Path("data/last_run.json")
    seen_ids = load_seen_arxiv_ids(output_dir, state_path)
    papers = fetch_recent_papers(args.categories, args.lookback_hours, args.max_results)
    new_papers = [paper for paper in papers if normalize_arxiv_id(paper.arxiv_id) not in seen_ids]
    scholarly_signals = fetch_scholarly_signals(
        new_papers, os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    )
    ranked = rank_papers(new_papers, args.limit, scholarly_signals=scholarly_signals)
    if not ranked:
        print("새로 등록된 미처리 논문이 없습니다. 기존 아카이브와 중복된 논문은 제외했습니다.")
        return None
    for item in ranked:
        if not args.no_llm:
            item.analysis = analyze_paper(item.paper, args.model)
    today = date.today()
    path = write_daily(ranked, output_dir, today)
    newly_processed = {normalize_arxiv_id(item.paper.arxiv_id) for item in ranked}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps({"date": today.isoformat(), "papers": [item.paper.arxiv_id for item in ranked], "seen_papers": sorted(seen_ids | newly_processed)}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily arXiv AI summaries")
    parser.add_argument("--categories", nargs="+", default=DEFAULT_CATEGORIES)
    parser.add_argument("--lookback-hours", type=int, default=72)
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output-dir", default="docs/daily")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL"))
    parser.add_argument("--no-llm", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    path = run(args)
    if path is not None:
        print(path)


if __name__ == "__main__":
    main()
