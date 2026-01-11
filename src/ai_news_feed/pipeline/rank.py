from __future__ import annotations

from datetime import datetime, UTC
from ai_news_feed.models import NewsItem


KEYWORDS = {
    "agent": 2.0,
    "agents": 2.0,
    "tool": 1.5,
    "tools": 1.5,
    "mcp": 2.5,
    "eval": 2.0,
    "evaluation": 2.0,
    "framework": 1.5,
    "release": 1.0,
    "benchmark": 1.5,
    "security": 1.5,
}


def _recency_score(published_at: datetime | None) -> float:
    if not published_at:
        return 0.0
    now = datetime.now(UTC)
    dt = published_at
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    hours = max((now - dt).total_seconds() / 3600.0, 0.0)
    if hours <= 24:
        return 3.0
    if hours <= 72:
        return 2.0
    if hours <= 168:
        return 1.0
    return 0.0


def _keyword_score(text: str) -> float:
    t = text.lower()
    score = 0.0
    for k, w in KEYWORDS.items():
        if k in t:
            score += w
    return score


def _score_item(item: NewsItem) -> float:
    text = f"{item.title}\n{item.raw_summary or ''}"
    kw = _keyword_score(text)
    rec = _recency_score(item.published_at)
    return kw + rec


def rank(items: list[NewsItem]) -> list[NewsItem]:
    return sorted(items, key=_score_item, reverse=True)
