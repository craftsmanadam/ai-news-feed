from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, HttpUrl

PRIORITY_TAG = Literal[
    "must_read", "worth_a_glance", "breaking", "falling", "evergreen"
]


class FeedConfig(BaseModel):
    name: str = Field(..., description="Human-friendly feed name (e.g., 'OpenAI Blog')")
    url: HttpUrl = Field(..., description="RSS/Atom feed URL")
    kind: Literal["rss"] = Field(default="rss", description="Feed type")
    reliability_score: int = Field(
        default=7, ge=1, le=10, description="Trust/credibility weighting (1-10)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags to apply to all items from this feed (e.g., ['frameworks']).",
    )
    max_items: int = Field(
        default=25,
        ge=1,
        le=200,
        description="Max items to take per fetch for this feed",
    )


class NewsItem(BaseModel):
    id: str = Field(
        ..., description="Stable identifier (usually a hash of canonical URL)"
    )
    title: str = Field(..., description="Article title")
    url: HttpUrl = Field(..., description="Canonical URL for the item")
    source: str = Field(..., description="Feed name or publisher name")
    published_at: datetime | None = Field(
        default=None, description="Publication datetime, if available"
    )
    author: str | None = Field(default=None, description="Author if provided by feed")
    raw_summary: str | None = Field(
        default=None, description="Raw summary/excerpt as provided by RSS/Atom"
    )
    tags: list[str] = Field(default_factory=list, description="Topic tags")
    raw: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw metadata payload for debugging and future enrichment",
    )


class DailyBrief(BaseModel):
    date: datetime = Field(..., description="Date/time the brief was generated")
    indicators: set[PRIORITY_TAG] = Field(default_factory=set)
    sources: list[str] = Field(
        default_factory=list,
        description="List of feed names used to compile this brief",
    )
    items: list[NewsItem] = Field(default_factory=list, description="Ranked items")
