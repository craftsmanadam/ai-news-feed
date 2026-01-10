from pydantic import BaseModel

from datetime import datetime
from pydantic import HttpUrl, Field
from typing import Literal


PRIORITY_TAG = Literal[
    "must_read", "worth_a_glance", "breaking", "falling", "evergreen"
]


class Source(BaseModel):
    name: str = Field(..., description="Name of the outlet (e.g., BBC, TechCrunch)")
    url: HttpUrl = Field(..., description="Direct link to the article or reference")
    reliability_score: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Agent's assessment of source credibility (1-10)",
    )


class NewsItem(BaseModel):
    title: str = Field(..., description="The full title of the news article")
    url: HttpUrl = Field(..., description="The direct URL to the news source")
    source: str = Field(
        ..., description="The name of the publishing outlet (e.g., 'Reuters')"
    )
    published_at: datetime = Field(
        ..., description="ISO 8601 formatted publication date and time"
    )
    summary: str = Field(
        ..., description="A concise 2-3 sentence overview of the article"
    )
    author: str | None = Field(None, description="The name of the article's author")
    tags: list[str] = Field(
        default_factory=list,
        description="A list of relevant topics or categories (e.g., ['tech', 'AI', 'finance'])",
    )


class DailyBrief(BaseModel):
    date: datetime = Field(..., description="ISO 8601 formatted date of brief")
    indicators: set[PRIORITY_TAG] = Field(
        default_factory=set,
        description="Priority indicators for this brief. Use 'must_read' for critical news.",
    )
    sources: list[Source] = Field(
        default_factory=list,
        description="A list of verified sources used to compile this brief.",
    )
