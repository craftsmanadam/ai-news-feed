from __future__ import annotations
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from ai_news_feed.models import NewsItem

DROP_QUERY_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "ref_src",
    "source",
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
}


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    query = [
        (k, v)
        for (k, v) in parse_qsl(parsed.query, keep_blank_values=True)
        if k not in DROP_QUERY_KEYS
    ]
    query.sort()
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            urlencode(query),
            "",
        )
    )


def dedupe(items: list[NewsItem]) -> list[NewsItem]:
    seen: set[str] = set()
    keep: list[NewsItem] = []
    for item in items:
        key = _canonicalize_url(str(item.url))
        if key in seen:
            continue
        seen.add(key)
        keep.append(item)
    return keep
