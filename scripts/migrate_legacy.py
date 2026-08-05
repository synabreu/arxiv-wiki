from __future__ import annotations

import re
from pathlib import Path

DAILY_DIR = Path("docs/daily")
PAPERS_DIR = Path("docs/papers")
LEGACY_DATES = ("2026-08-04", "2026-08-05")
SECTION_RE = re.compile(r"(?m)^## (\d+)\. (.+)$")


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "paper"


def parse_legacy_page(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(SECTION_RE.finditer(text))
    papers: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end].strip()
        papers.append((title, section))
    return papers


def render_detail(title: str, section: str, target_date: str) -> str:
    body = SECTION_RE.sub(f"# {title}", section, count=1)
    return (
        f"{body}\n\n"
        f"---\n\n"
        f"- **소개 날짜:** {target_date}\n"
        f"- [← {target_date} 논문 목록으로 돌아가기](../daily/{target_date}.md)\n"
        f"- [일별 아카이브 보기](../daily/index.md)\n"
    )


def render_daily_list(target_date: str, titles: list[str], *, latest: bool = False) -> str:
    prefix = "papers" if latest else "../papers"
    lines = [
        f"# {target_date} arXiv AI 논문",
        "",
        "> 새로 선별된 논문의 제목만 표시한다. 제목을 선택하면 상세 분석 페이지로 이동한다.",
        "",
    ]
    if not latest:
        lines += ["[← 일별 아카이브로 돌아가기](index.md)", ""]
    lines += ["## 오늘의 목록", ""]
    for title in titles:
        lines.append(f"- [{title}]({prefix}/{slugify(title)}.md)")
    return "\n".join(lines).strip() + "\n"


def rebuild_archive() -> None:
    lines = [
        "# 일별 arXiv AI 논문 아카이브",
        "",
        "날짜별 논문 제목을 선택하면 개별 상세 분석 페이지로 이동한다.",
        "",
        "[← 홈으로 돌아가기](../index.md)",
        "",
        "| 날짜 | 논문 제목 |",
        "|---|---|",
    ]
    for path in sorted(DAILY_DIR.glob("????-??-??.md"), reverse=True):
        text = path.read_text(encoding="utf-8")
        links = re.findall(r"(?m)^- \[([^]]+)\]\((?:\.\./)?papers/([^)]+\.md)\)$", text)
        for title, filename in links:
            lines.append(f"| [{path.stem}]({path.name}) | [{title}](../papers/{filename}) |")
    (DAILY_DIR / "index.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    latest_titles: list[str] = []
    latest_date = ""

    for target_date in LEGACY_DATES:
        path = DAILY_DIR / f"{target_date}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^- \[[^]]+\]\(\.\./papers/[^)]+\.md\)$", text):
            titles = re.findall(r"(?m)^- \[([^]]+)\]\(\.\./papers/[^)]+\.md\)$", text)
        else:
            parsed = parse_legacy_page(path)
            titles = [title for title, _ in parsed]
            for title, section in parsed:
                detail_path = PAPERS_DIR / f"{slugify(title)}.md"
                detail_path.write_text(render_detail(title, section, target_date), encoding="utf-8")
            path.write_text(render_daily_list(target_date, titles), encoding="utf-8")

        if target_date >= latest_date:
            latest_date = target_date
            latest_titles = titles

    if latest_titles:
        Path("docs/latest.md").write_text(
            render_daily_list(latest_date, latest_titles, latest=True),
            encoding="utf-8",
        )

    rebuild_archive()


if __name__ == "__main__":
    main()
