import json
from datetime import datetime
from pathlib import Path

from ai_news_feed.config import settings
from ai_news_feed.models import NewsItem
from ai_news_feed.pipeline.dedupe import dedupe
from ai_news_feed.pipeline.rank import rank
from ai_news_feed.sources.rss import fetch_rss_items


def _write_items(prefix: str, items: list[NewsItem]) -> Path:
    settings.feed_output_dir.mkdir(parents=True, exist_ok=True)
    day = datetime.now().strftime("%Y%m%d")
    destination = settings.feed_output_dir / f"{prefix}_items_{day}UTC.json"
    content = [item.model_dump(mode="json") for item in items]
    destination.write_text(json.dumps(content, indent=2), encoding="utf-8")

    return destination


def collect_rss_feeds() -> tuple[str, list[NewsItem]]:
    items: list[NewsItem] = []
    for feed_config in settings.load_rss_feeds():
        items.extend(fetch_rss_items(feed_config))
    _write_items("rss_raw", items)
    items = rank(dedupe(items))
    destination = _write_items("rss", items)

    return destination, items
