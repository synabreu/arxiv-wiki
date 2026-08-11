from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar

from arxiv_wiki import arxiv_client


class AtomResponse:
    headers: ClassVar[dict[str, str]] = {"content-type": "application/atom+xml"}
    text: ClassVar[str] = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
          xmlns:arxiv="http://arxiv.org/schemas/atom">
      <entry>
        <id>https://arxiv.org/abs/2608.00001v1</id>
        <updated>2600-08-11T00:00:00Z</updated>
        <published>2600-08-11T00:00:00Z</published>
        <title>Test paper</title>
        <summary>Test summary</summary>
        <author><name>Test Author</name></author>
        <category term="cs.AI" />
        <arxiv:primary_category term="cs.AI" />
        <link title="pdf" href="https://arxiv.org/pdf/2608.00001v1" />
      </entry>
    </feed>"""


def test_categories_are_combined_into_one_api_request(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get(url: str, *, timeout: int) -> AtomResponse:
        calls.append(url)
        return AtomResponse()

    monkeypatch.setattr(arxiv_client, "get", fake_get)
    monkeypatch.setattr(arxiv_client, "datetime", _FutureDateTime)

    papers = arxiv_client.fetch_recent_papers(["cs.AI", "cs.CL"], lookback_hours=72)

    assert len(calls) == 1
    assert "cat%3Acs.AI+OR+cat%3Acs.CL" in calls[0]
    assert [paper.arxiv_id for paper in papers] == ["2608.00001v1"]


class _FutureDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2600, 8, 11, 12, tzinfo=UTC)
