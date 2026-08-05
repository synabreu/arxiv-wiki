from __future__ import annotations

import re
from pathlib import Path

from arxiv_wiki.figures import extract_key_visuals, insert_visuals

PDF_RE = re.compile(r"\[PDF\]\((https?://[^)]+)\)")


def main() -> None:
    docs_dir = Path("docs")
    papers_dir = docs_dir / "papers"
    changed = 0
    failed = 0

    for paper_path in sorted(papers_dir.glob("*.md")):
        markdown = paper_path.read_text(encoding="utf-8")
        match = PDF_RE.search(markdown)
        if not match:
            print(f"skip: PDF link not found: {paper_path}")
            continue

        try:
            visuals = extract_key_visuals(
                pdf_url=match.group(1),
                slug=paper_path.stem,
                docs_dir=docs_dir,
                limit=3,
            )
            if not visuals:
                print(f"skip: no visual caption found: {paper_path.name}")
                continue
            updated = insert_visuals(markdown, visuals)
            if updated != markdown:
                paper_path.write_text(updated, encoding="utf-8")
                changed += 1
                print(f"updated: {paper_path.name} ({len(visuals)} visuals)")
        except Exception as exc:
            failed += 1
            print(f"failed: {paper_path.name}: {exc}")

    print(f"completed: changed={changed}, failed={failed}")


if __name__ == "__main__":
    main()
