from __future__ import annotations

from dataclasses import dataclass

import requests

from .models import Paper

API_ROOT = "https://api.semanticscholar.org/graph/v1"


@dataclass(frozen=True)
class ScholarlySignals:
    citation_count: int = 0
    influential_citation_count: int = 0
    max_author_h_index: int = 0
    max_author_citation_count: int = 0


def _arxiv_id(paper: Paper) -> str:
    return paper.arxiv_id.split("v", 1)[0]


def fetch_scholarly_signals(
    papers: list[Paper], api_key: str | None = None
) -> dict[str, ScholarlySignals]:
    """Fetch citation and author-impact signals without blocking daily generation."""
    if not papers:
        return {}

    headers = {"x-api-key": api_key} if api_key else {}
    try:
        paper_response = requests.post(
            f"{API_ROOT}/paper/batch",
            params={"fields": "paperId,citationCount,influentialCitationCount,authors"},
            json={"ids": [f"ARXIV:{_arxiv_id(paper)}" for paper in papers]},
            headers=headers,
            timeout=30,
        )
        paper_response.raise_for_status()
        paper_records = paper_response.json()

        author_ids = {
            author["authorId"]
            for record in paper_records
            if record
            for author in record.get("authors", [])
            if author.get("authorId")
        }
        author_metrics: dict[str, dict] = {}
        if author_ids:
            author_response = requests.post(
                f"{API_ROOT}/author/batch",
                params={"fields": "hIndex,citationCount"},
                json={"ids": sorted(author_ids)},
                headers=headers,
                timeout=30,
            )
            author_response.raise_for_status()
            author_metrics = {
                record["authorId"]: record
                for record in author_response.json()
                if record and record.get("authorId")
            }
    except (requests.RequestException, ValueError, TypeError, KeyError) as exc:
        print(f"학술 지표를 불러오지 못해 기본 순위 신호로 계속합니다: {exc}")
        return {}

    signals: dict[str, ScholarlySignals] = {}
    for paper, record in zip(papers, paper_records, strict=False):
        if not record:
            continue
        metrics = [
            author_metrics.get(author.get("authorId"), {})
            for author in record.get("authors", [])
        ]
        signals[paper.arxiv_id] = ScholarlySignals(
            citation_count=max(int(record.get("citationCount") or 0), 0),
            influential_citation_count=max(
                int(record.get("influentialCitationCount") or 0), 0
            ),
            max_author_h_index=max(
                (int(metric.get("hIndex") or 0) for metric in metrics), default=0
            ),
            max_author_citation_count=max(
                (int(metric.get("citationCount") or 0) for metric in metrics),
                default=0,
            ),
        )
    return signals
