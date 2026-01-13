from __future__ import annotations

import json

from datetime import datetime, UTC
from collections.abc import Iterable
from pydantic_ai import Agent
from pydantic_ai.output import PromptedOutput
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ai_news_feed.models import DailyBrief, NewsItem
from ai_news_feed.config import settings


DEFAULT_MODEL = "Phi-4"
GITHUB_ENDPOINT = "https://models.inference.ai.azure.com"


def _prompt(items_json: str) -> str:
    return (
        "Create a DailyBrief from the collected AI news items.\n"
        "Rules:\n"
        "- Pick the most important items and order them most important first.\n"
        "- important items are ones that affect how software teams write AI solutions and agentic agents`\n"
        "- indicators: include 'must_read' if there is major, high-impact news.\n"
        "- sources: list unique source names used.\n"
        "- items: include only the selected items (not necessarily all).\n"
        "- Keep each item's raw_summary as-is if present; do not fabricate missing summaries.\n"
        "- Do not change urls\n"
        "- Do not create new items\n"
        "\n"
        f"Today (UTC) is {datetime.now(UTC).date().isoformat()}.\n"
        "\n"
        "ITEMS JSON:\n"
        f"{items_json}"
    )


def _build_agent(model_name: str = DEFAULT_MODEL) -> Agent[None, DailyBrief]:
    provider = OpenAIProvider(
        base_url=GITHUB_ENDPOINT,
        api_key=settings.github_token.get_secret_value(),
    )
    model = OpenAIChatModel(
        model_name=model_name,
        provider=provider
    )
    return Agent(
        model=model,
        output_type=PromptedOutput(DailyBrief),
        system_prompt=(
            "You create a daily AI news brief for a software engineering leader (technical).\n"
            "Use ONLY the provided items. Do not invent facts.\n"
            "If details are missing, say so.\n"
            "Prefer primary sources (vendor blogs, official releases) when choosing must-read items.\n"
            "Keep summaries concise and actionable.\n"
        ),
    )


def _items_payload(items: Iterable[NewsItem]) -> str:
    minimal = []
    for i in items:
        minimal.append(
            {
                "title": i.title,
                "url": str(i.url),
                "source": i.source,
                "published_at": i.published_at.isoformat() if i.published_at else None,
                "raw_summary": i.raw_summary,
                "tags": i.tags,
            }
        )
    return json.dumps(minimal, ensure_ascii=False)


def summarize_items(
    items: list[NewsItem], top_n: int = 10, model_name: str = DEFAULT_MODEL
) -> DailyBrief:
    agent = _build_agent(model_name=model_name)
    trimmed = items[:top_n]
    items_json = _items_payload(trimmed)
    result = agent.run_sync(
        _prompt(items_json),
        model_settings={
            "temperature": 0.2,
            "tool_choice": "auto"
        }
    )
    brief = result.output
    if not getattr(brief, "date", None):
        brief.date = datetime.now(UTC)
    if brief.sources:
        brief.sources = sorted(set(brief.sources))
    return brief
