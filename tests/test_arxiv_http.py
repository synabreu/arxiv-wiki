from __future__ import annotations

from dataclasses import dataclass, field

import pytest
import requests

from arxiv_wiki import arxiv_http
from arxiv_wiki.pdf import download_pdf


@dataclass
class StubResponse:
    status_code: int = 200
    text: str = "ok"
    content: bytes = b"pdf"
    headers: dict[str, str] = field(default_factory=dict)

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


@pytest.fixture(autouse=True)
def reset_arxiv_request_state() -> None:
    arxiv_http._last_request_at.clear()
    download_pdf.cache_clear()


def test_rate_limit_body_retries_with_exponential_backoff_and_jitter(monkeypatch) -> None:
    responses = iter(
        [
            StubResponse(
                text="Rate exceeded.",
                content=b"Rate exceeded.",
                headers={"content-type": "text/html"},
            ),
            StubResponse(text="<feed />", headers={"content-type": "application/atom+xml"}),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(arxiv_http.requests, "get", lambda *args, **kwargs: next(responses))
    monkeypatch.setattr(arxiv_http.random, "uniform", lambda *args: 2.0)
    monkeypatch.setattr(arxiv_http.time, "sleep", sleeps.append)

    response = arxiv_http.get("https://export.arxiv.org/api/query", timeout=10)

    assert response.text == "<feed />"
    assert 17.0 in sleeps


def test_retry_after_header_is_respected(monkeypatch) -> None:
    responses = iter(
        [
            StubResponse(status_code=429, headers={"Retry-After": "42"}),
            StubResponse(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(arxiv_http.requests, "get", lambda *args, **kwargs: next(responses))
    monkeypatch.setattr(arxiv_http.time, "sleep", sleeps.append)

    arxiv_http.get("https://export.arxiv.org/api/query", timeout=10)

    assert 42.0 in sleeps


def test_distinct_requests_to_same_host_are_throttled(monkeypatch) -> None:
    sleeps: list[float] = []
    monotonic_values = iter([100.0, 101.0, 104.0])
    monkeypatch.setattr(arxiv_http.requests, "get", lambda *args, **kwargs: StubResponse())
    monkeypatch.setattr(arxiv_http.time, "monotonic", lambda: next(monotonic_values))
    monkeypatch.setattr(arxiv_http.time, "sleep", sleeps.append)

    arxiv_http.get("https://arxiv.org/pdf/2608.00001", timeout=10)
    arxiv_http.get("https://arxiv.org/pdf/2608.00002", timeout=10)

    assert sleeps == [2.0]


def test_pdf_download_is_cached(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get(url: str, **kwargs) -> StubResponse:
        calls.append(url)
        return StubResponse(content=b"one pdf")

    monkeypatch.setattr(arxiv_http.requests, "get", fake_get)

    assert download_pdf("https://arxiv.org/pdf/2608.00001") == b"one pdf"
    assert download_pdf("https://arxiv.org/pdf/2608.00001") == b"one pdf"
    assert calls == ["https://arxiv.org/pdf/2608.00001"]


def test_repeated_rate_limits_fail_after_bounded_attempts(monkeypatch) -> None:
    calls = 0

    def fake_get(*args, **kwargs) -> StubResponse:
        nonlocal calls
        calls += 1
        return StubResponse(status_code=429, text="Rate exceeded.", content=b"Rate exceeded.")

    monkeypatch.setattr(arxiv_http.requests, "get", fake_get)
    monkeypatch.setattr(arxiv_http.random, "uniform", lambda *args: 0.0)
    monkeypatch.setattr(arxiv_http.time, "sleep", lambda seconds: None)

    with pytest.raises(RuntimeError, match="failed after 5 attempts"):
        arxiv_http.get("https://export.arxiv.org/api/query", timeout=10)

    assert calls == 5
