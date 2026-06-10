import feedparser
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))

_SEARCH = "https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"

FEEDS = {
    "헤드라인": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko",
    "정치":     _SEARCH.format(q="정치"),
    "경제":     _SEARCH.format(q="경제"),
    "사회":     _SEARCH.format(q="사회"),
    "세계":     _SEARCH.format(q="국제+세계"),
    "IT/과학":  _SEARCH.format(q="IT+과학+기술"),
}

def split_title_source(raw: str) -> tuple[str, str]:
    """'제목 - 출처' 형태에서 제목과 출처를 분리."""
    for sep in (" - ", " – ", " — "):
        if sep in raw:
            idx = raw.rfind(sep)
            return raw[:idx].strip(), raw[idx + len(sep):].strip()
    return raw.strip(), ""

def parse_feed(category: str, url: str) -> list[dict]:
    feed = feedparser.parse(url)
    items = []
    seen = set()
    for entry in feed.entries[:15]:
        raw_title = entry.get("title", "").strip()
        title, source = split_title_source(raw_title)
        if title in seen:
            continue
        seen.add(title)
        items.append({
            "title":  title,
            "source": source,
            "link":   entry.get("link", ""),
        })
        if len(items) == 10:
            break
    return items

def main():
    news_by_category = {}
    for category, url in FEEDS.items():
        items = parse_feed(category, url)
        if items:
            news_by_category[category] = items

    updated_at = datetime.now(KST).strftime("%Y년 %m월 %d일 %H:%M")

    root = Path(__file__).parent.parent
    env = Environment(loader=FileSystemLoader(root / "templates"))
    template = env.get_template("index.html")

    html = template.render(
        updated_at=updated_at,
        categories=list(news_by_category.keys()),
        news_by_category=news_by_category,
    )

    out = root / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    total = sum(len(v) for v in news_by_category.values())
    print(f"[done] {total}건 → {out}")

if __name__ == "__main__":
    main()
