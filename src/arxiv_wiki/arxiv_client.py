from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

from dateutil.parser import isoparse

from .arxiv_http import get
from .models import Paper

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


def _text(node: ET.Element | None, default: str = "") -> str:
    return " ".join((node.text or default).split()) if node is not None else default


def fetch_recent_papers(categories: list[str], lookback_hours: int = 48, max_results: int = 50, timeout: int = 120) -> list[Paper]:
    query = " OR ".join(f"cat:{category}" for category in categories)
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{API_URL}?{urlencode(params)}"
    response = get(url, timeout=timeout)

    content_type = response.headers.get("content-type", "")
    if "xml" not in content_type and "atom" not in content_type:
        raise RuntimeError(
            f"Unexpected arXiv response: content-type={content_type}, body={response.text[:200]}"
        )

    root = ET.fromstring(response.text)
    cutoff = datetime.now(UTC) - timedelta(hours=lookback_hours)
    papers: list[Paper] = []

    for entry in root.findall(f"{ATOM}entry"):
        published = isoparse(_text(entry.find(f"{ATOM}published")))
        if published < cutoff:
            continue
        entry_url = _text(entry.find(f"{ATOM}id"))
        arxiv_id = entry_url.rsplit("/", 1)[-1]
        links = {
            link.attrib.get("title", link.attrib.get("rel", "")): link.attrib.get("href", "")
            for link in entry.findall(f"{ATOM}link")
        }
        categories_found = [node.attrib.get("term", "") for node in entry.findall(f"{ATOM}category")]
        primary = entry.find(f"{ARXIV}primary_category")
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=_text(entry.find(f"{ATOM}title")),
                authors=[_text(a.find(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")],
                summary=_text(entry.find(f"{ATOM}summary")),
                published=published,
                updated=isoparse(_text(entry.find(f"{ATOM}updated"))),
                categories=categories_found,
                primary_category=(primary.attrib.get("term", "") if primary is not None else ""),
                abstract_url=entry_url,
                pdf_url=links.get("pdf", f"https://arxiv.org/pdf/{arxiv_id}"),
            )
        )

    return papers
