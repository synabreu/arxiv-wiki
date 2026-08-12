from __future__ import annotations

import random
import time
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit

import requests

ARXIV_USER_AGENT = "arxiv-wiki/1.0 (mailto:synabreu@outlook.com)"
MIN_REQUEST_INTERVAL_SECONDS = 3.0
MAX_ATTEMPTS = 5
BASE_BACKOFF_SECONDS = 15.0
MAX_BACKOFF_SECONDS = 300.0
MAX_JITTER_SECONDS = 5.0
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}

_last_request_at: dict[str, float] = {}


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return None
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=UTC)
        return max(0.0, (retry_at - datetime.now(UTC)).total_seconds())


def _throttle(url: str) -> None:
    host = urlsplit(url).netloc.lower()
    last_request = _last_request_at.get(host)
    if last_request is not None:
        remaining = MIN_REQUEST_INTERVAL_SECONDS - (time.monotonic() - last_request)
        if remaining > 0:
            time.sleep(remaining)
    _last_request_at[host] = time.monotonic()


def _backoff_seconds(failure_index: int, retry_after: str | None) -> float:
    server_delay = _retry_after_seconds(retry_after)
    if server_delay is not None:
        return min(MAX_BACKOFF_SECONDS, max(MIN_REQUEST_INTERVAL_SECONDS, server_delay))
    exponential = BASE_BACKOFF_SECONDS * (2**failure_index)
    jitter = random.uniform(0.0, MAX_JITTER_SECONDS)
    return min(MAX_BACKOFF_SECONDS, max(MIN_REQUEST_INTERVAL_SECONDS, exponential + jitter))


def get(url: str, *, timeout: int) -> requests.Response:
    """GET an arXiv resource with polite throttling and bounded retries."""
    headers = {"User-Agent": ARXIV_USER_AGENT}
    last_response: requests.Response | None = None
    last_error: requests.RequestException | None = None

    for attempt in range(MAX_ATTEMPTS):
        _throttle(url)
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            last_error = exc
            if attempt == MAX_ATTEMPTS - 1:
                break
            delay = _backoff_seconds(attempt, None)
            print(
                f"arXiv request error {type(exc).__name__}; "
                f"retry {attempt + 2}/{MAX_ATTEMPTS} in {delay:.1f}s"
            )
            time.sleep(delay)
            continue

        last_response = response
        body = response.content[:200].decode("utf-8", errors="ignore").lower()
        rate_limited = response.status_code == 429 or "rate exceeded" in body
        transient = response.status_code in TRANSIENT_STATUS_CODES
        if rate_limited or transient:
            if attempt == MAX_ATTEMPTS - 1:
                break
            delay = _backoff_seconds(attempt, response.headers.get("Retry-After"))
            reason = "rate limit" if rate_limited else f"HTTP {response.status_code}"
            print(
                f"arXiv {reason} detected; retry {attempt + 2}/{MAX_ATTEMPTS} "
                f"in {delay:.1f}s"
            )
            time.sleep(delay)
            continue

        response.raise_for_status()
        return response

    if last_response is not None:
        raise RuntimeError(
            "arXiv request failed after "
            f"{MAX_ATTEMPTS} attempts: status={last_response.status_code}, "
            f"body={last_response.text[:200]}"
        )
    raise RuntimeError(f"arXiv request failed after {MAX_ATTEMPTS} attempts") from last_error
