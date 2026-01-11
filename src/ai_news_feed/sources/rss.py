# NEWS_STACK_URL = "https://thenewstack.io/ai/feed/"
# MLM_URL = "https://feeds.feedburner.com/MachineLearningMastery"
# HUGGINGFACE_URL = "https://huggingface.co/blog/feed.xml"

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import List, Optional
import feedparser
from feedparser import FeedParserDict
import httpx

from ai_news_feed.models import FeedConfig, NewsItem


MAX_TIMEOUT = 15.0


def _stable_id(url: str) -> str:
   return hashlib.sha256(url.strip().encode("utf-8")).hexdigest()

def _parse_datetime(entry: dict) -> Optional[datetime]:
   for key in ("published_parsed", "updated_parsed"):
       value = entry.get(key)
       if value:
           return datetime(*value[:6], tzinfo=timezone.utc)
   return None

def _get_feed(feed: FeedConfig, timeout: float = MAX_TIMEOUT) -> FeedParserDict:
   if feed.kind != "rss":
       raise ValueError(f"fetch_rss_items only supports kind='rss', got {feed.kind!r}")
   with httpx.Client(timeout=timeout, follow_redirects=True) as client:
       resp = client.get(str(feed.url))
       resp.raise_for_status()
   return feedparser.parse(resp.text)

def _parse_newsitem(entry: FeedParserDict, feed: FeedConfig, parsed: FeedParserDict) -> NewsItem | None:
    title = (entry.get("title") or "").strip()
    url = (entry.get("link") or "").strip()
    if not title or not url:
        return None
    raw_summary = entry.get("summary") or entry.get("description")
    author = entry.get("author")
    published_at = _parse_datetime(entry)
    return NewsItem(
        id=_stable_id(url),
        title=title,
        url=url,
        source=feed.name,
        published_at=published_at,
        author=author,
        raw_summary=raw_summary,
        tags=list(feed.tags),
        raw={
            "feed_title": getattr(parsed.feed, "title", None),
            "entry_id": entry.get("id"),
        },
    )

def fetch_rss_items(feed: FeedConfig, timeout: float = MAX_TIMEOUT) -> List[NewsItem]:
   parsed = _get_feed(feed, timeout)
   items: List[NewsItem] = []
   for entry in (parsed.entries or [])[: feed.max_items]:
       rss_news_item = _parse_newsitem(entry, feed, parsed)
       if rss_news_item:
           items.append(rss_news_item)
   return items
