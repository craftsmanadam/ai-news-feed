import json
from datetime import datetime
from pathlib import Path

from ai_news_feed.config import settings
from ai_news_feed.models import NewsItem
from ai_news_feed.sources.rss import fetch_rss_items


def _write_items(type: str, items: list[NewsItem]) -> Path:
    settings.feed_output_dir.mkdir(parents=True, exist_ok=True)
    day = datetime.now().strftime("%Y%m%d")
    destination = settings.feed_output_dir / f"{type}_items_{day}.json"
    content = [item.model_dump(mode="json") for item in items]
    destination.write_text(json.dumps(content, indent=2), encoding="utf-8")

    return destination


def collect_rss_feeds() -> list[NewsItem]:
    items: list[NewsItem] = []
    for feed_config in settings.load_feeds():
        items.extend(fetch_rss_items(feed_config))
    destination = _write_items("rss", items)
    return destination, items
