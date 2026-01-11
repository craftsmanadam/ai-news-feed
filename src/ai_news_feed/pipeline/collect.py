from ai_news_feed.config import settings
from ai_news_feed.models import NewsItem
from ai_news_feed.sources.rss import fetch_rss_items


def collect_rss_feeds() -> list[NewsItem]:
    items: list[NewsItem] = []
    for feed_config in settings.load_feeds():
        items.extend(fetch_rss_items(feed_config))
    return items
