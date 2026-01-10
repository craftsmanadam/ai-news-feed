import typer


from ai_news_feed.config import settings as config


app = typer.Typer(
    help="An agentic agent to aggregate Agentic AI news data and cureate it for consumption"
)


def logic_collect():
    typer.echo("Place holder for collection")


def logic_summarize():
    typer.echo("Place holder for summarization")


@app.command()
def collect():
    """Only collect source information."""
    logic_collect()


@app.command()
def summarize():
    """Collect and then summarize information."""
    logic_summarize()


@app.command()
def run():
    """Execute the full application."""
    typer.echo("Starting full application run...")
    logic_collect()
    logic_summarize()
    typer.echo("Full execution complete.")


@app.command()
def settings():
    """Print current settings"""
    typer.echo(config.model_dump_json(indent=2))


def main():
    app()


if __name__ == "__main__":
    main()
