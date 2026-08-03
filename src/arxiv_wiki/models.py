from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class Paper(BaseModel):
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: datetime
    updated: datetime
    categories: list[str]
    primary_category: str
    abstract_url: str
    pdf_url: str


class PaperAnalysis(BaseModel):
    one_line_summary: str
    problem: str
    contributions: list[str] = Field(min_length=1, max_length=5)
    method: str
    results: list[str] = Field(default_factory=list, max_length=5)
    limitations: list[str] = Field(default_factory=list, max_length=4)
    developer_takeaways: list[str] = Field(default_factory=list, max_length=5)
    keywords: list[str] = Field(default_factory=list, max_length=8)
    confidence_note: str


class RankedPaper(BaseModel):
    paper: Paper
    score: float
    score_reasons: list[str]
    analysis: PaperAnalysis | None = None
