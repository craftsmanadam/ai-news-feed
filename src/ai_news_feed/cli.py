import typer
from datetime import datetime
from pydantic import TypeAdapter
from pathlib import Path

from ai_news_feed.config import settings as config
from ai_news_feed.models import FeedConfig, NewsItem
from ai_news_feed.pipeline.collect import collect_rss_feeds
from ai_news_feed.pipeline.summarize import summarize_items


app = typer.Typer(
    help="An agentic agent to aggregate Agentic AI news data and cureate it for consumption"
)

def _read_news_items(file: Path) -> list[NewsItem]:
    adapter = TypeAdapter(list[NewsItem])
    return adapter.validate_json(file.read_text(encoding="utf-8"))


def logic_collect() -> Path:
    destination, _ = collect_rss_feeds()
    return destination


def logic_summarize(file: Path):
    brief = summarize_items(_read_news_items(file))
    typer.echo(f"Summerization: {brief}")


@app.command()
def collect():
    """Only collect source information."""
    destination = logic_collect()
    typer.echo(f"Collected results: {destination}")


@app.command()
def summarize():
    """Collect and then summarize information."""
    file = logic_collect()
    logic_summarize(file)


@app.command()
def run():
    """Execute the full application."""
    typer.echo("Starting full application run...")
    file = logic_collect()
    logic_summarize(file)
    typer.echo("Full execution complete.")


@app.command()
def settings():
    """Print current settings"""
    adapter = TypeAdapter(list[FeedConfig])
    typer.echo(config.model_dump_json(indent=2))
    typer.echo(adapter.dump_json(config.load_rss_feeds(), indent=2).decode("utf-8"))


def main():
    app()


if __name__ == "__main__":
    main()
