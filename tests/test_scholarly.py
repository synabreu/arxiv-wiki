from datetime import UTC, datetime

import requests

from arxiv_wiki.models import Paper
from arxiv_wiki.scholarly import fetch_scholarly_signals


class Response:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def paper() -> Paper:
    now = datetime.now(UTC)
    return Paper(
        arxiv_id="2608.01234v2",
        title="AI Paper",
        authors=["A. Author"],
        summary="An AI paper.",
        published=now,
        updated=now,
        categories=["cs.AI"],
        primary_category="cs.AI",
        abstract_url="https://arxiv.org/abs/2608.01234",
        pdf_url="https://arxiv.org/pdf/2608.01234",
    )


def test_fetches_paper_and_author_metrics_in_batches(monkeypatch):
    calls = []

    def fake_post(url, **kwargs):
        calls.append((url, kwargs))
        if url.endswith("/paper/batch"):
            return Response(
                [
                    {
                        "paperId": "p1",
                        "citationCount": 12,
                        "influentialCitationCount": 3,
                        "authors": [{"authorId": "a1"}],
                    }
                ]
            )
        return Response([{"authorId": "a1", "hIndex": 42, "citationCount": 9000}])

    monkeypatch.setattr(requests, "post", fake_post)
    target = paper()
    result = fetch_scholarly_signals([target], api_key="secret")

    assert calls[0][1]["json"] == {"ids": ["ARXIV:2608.01234"]}
    assert calls[0][1]["headers"] == {"x-api-key": "secret"}
    assert result[target.arxiv_id].citation_count == 12
    assert result[target.arxiv_id].influential_citation_count == 3
    assert result[target.arxiv_id].max_author_h_index == 42
    assert result[target.arxiv_id].max_author_citation_count == 9000


def test_api_failure_returns_empty_signals(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(requests, "post", fail)
    assert fetch_scholarly_signals([paper()]) == {}
