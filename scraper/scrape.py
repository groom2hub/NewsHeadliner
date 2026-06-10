import feedparser
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))

FEEDS = {
    "헤드라인": "https://feeds.feedburner.com/navernews/top_news",
    "정치":     "https://feeds.feedburner.com/navernews/politics",
    "경제":     "https://feeds.feedburner.com/navernews/economy",
    "사회":     "https://feeds.feedburner.com/navernews/society",
    "세계":     "https://feeds.feedburner.com/navernews/world",
    "IT/과학":  "https://feeds.feedburner.com/navernews/it_science",
}

def parse_feed(category: str, url: str) -> list[dict]:
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:10]:
        items.append({
            "title":    entry.get("title", "").strip(),
            "link":     entry.get("link", ""),
            "summary":  entry.get("summary", "").strip(),
            "category": category,
        })
    return items

def main():
    all_news = []
    for category, url in FEEDS.items():
        all_news.extend(parse_feed(category, url))

    now = datetime.now(KST).strftime("%Y년 %m월 %d일 %H:%M KST")

    output = {
        "updated_at": now,
        "news": all_news,
    }

    out_path = Path(__file__).parent.parent / "site" / "data.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] {len(all_news)}건 저장 → {out_path}")

if __name__ == "__main__":
    main()
