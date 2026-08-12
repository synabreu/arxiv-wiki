from __future__ import annotations

from functools import lru_cache

from .arxiv_http import get


@lru_cache(maxsize=10)
def download_pdf(pdf_url: str) -> bytes:
    """Download a PDF once per process so analysis and figures share it."""
    return get(pdf_url, timeout=120).content

