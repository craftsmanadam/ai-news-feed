# AI-NEWS-FEED

AI-NEWS-FEED is a Python-based system that aggregates AI news from RSS feeds, deduplicates items, ranks them by relevance, and uses AI (via pydantic-ai) to generate daily briefs. The goal is to automatically identify and summarize the most important AI/agent-related news for software engineering teams.

## Features

- **Multi-stage Pipeline**: Collect → Dedupe → Rank → Summarize
- **Smart Deduplication**: Canonicalizes URLs to remove tracking parameters and duplicates
- **Intelligent Ranking**: Scores articles by keyword relevance and recency
- **AI-Powered Summaries**: Uses pydantic-ai with GitHub Models API (Phi-4) to generate structured daily briefs
- **Flexible Output**: JSON and Markdown formats for easy consumption
- **Containerized Deployment**: Docker and Docker Compose support

## Architecture

### Pipeline Stages

1. **Collect** (`pipeline/collect.py`): Fetches items from RSS feeds defined in `rss_feeds.yaml`
2. **Dedupe** (`pipeline/dedupe.py`): Removes duplicate items by canonicalizing URLs (strips tracking params like utm_*, fbclid, etc.)
3. **Rank** (`pipeline/rank.py`): Scores items based on:
   - Keyword relevance (agent, tools, MCP, eval, benchmark, security)
   - Recency (≤24h = 3pts, ≤72h = 2pts, ≤1wk = 1pt)
4. **Summarize** (`pipeline/summarize.py`): Uses pydantic-ai with GitHub Models API (Phi-4) to generate `DailyBrief`

### Data Models

- **FeedConfig**: RSS feed configuration (name, URL, reliability_score, tags, max_items)
- **NewsItem**: Individual news article with id, title, URL, source, published_at, raw_summary, tags
- **DailyBrief**: Final output with date, indicators (must_read/worth_a_glance/etc), sources, ranked items

## Prerequisites

- Python 3.11+ (managed via pyenv)
- Poetry for dependency management
- Docker for containerized execution
- `.env.secrets` file with the following:
  - `github_token`: Required for GitHub Models API access
  - `GEMINI_API_KEY`: Legacy, may be removed in future
- dotenv and direnv configured (`direnv allow`)

## Quick Start

### Initial Setup

```bash
# Bootstrap the development environment
# Installs pyenv, poetry, docker, and project dependencies
bin/bootstrap.sh

# Allow direnv to load environment variables
direnv allow
```

### Running the Application

#### Via Poetry (Local Development)

```bash
# Run full pipeline: collect → dedupe → rank → summarize
poetry run ai-news-feed run

# Only collect RSS feeds
poetry run ai-news-feed collect

# Collect and summarize (skip intermediate steps)
poetry run ai-news-feed summarize

# Print current configuration
poetry run ai-news-feed settings
```

#### Via Docker

```bash
# Build Docker image
bin/build.sh

# Run containerized application
bin/run.sh

# Or using Docker Compose
docker compose up
```

## Configuration

### RSS Feeds (`rss_feeds.yaml`)

Edit this file to add or modify RSS feeds. Each feed requires:

```yaml
feeds:
  - name: Feed Name                # Human-friendly name
    url: https://example.com/rss   # RSS/Atom feed URL
    tags: [ai, agents, news]       # Topic tags
    reliability_score: 8           # Trust rating (1-10)
    kind: rss                      # Always 'rss' (for now)
    max_items: 25                  # Items to fetch per feed (1-200)
```

### Environment Variables

Settings are loaded from `.env` and `.env.secrets` files:

- `feed_output_dir`: Where JSON/MD outputs are written (default: `./output/`)
- `rss_feeds_file`: YAML file with feed configurations (default: `rss_feeds.yaml`)
- `github_token`: Required for GitHub Models API access

## Output Files

The application generates the following outputs in the `output/` directory:

- `rss_raw_items_YYYYMMDDUTC.json`: Raw collected items before deduplication
- `rss_items_YYYYMMDDUTC.json`: Deduplicated and ranked items
- `brief_YYYYMMDD.md`: Markdown-formatted daily brief

Example brief format:
```markdown
# AI News Brief 2026-01-13

## Sources
- The News Stack
- Hugging Face Blog
- OpenAI Blog

## Items
1. [Article Title](https://example.com/article)
   Summary of the article...
```

## Development

### Common Development Commands

```bash
# Run tests with coverage
bin/unit_tests.sh  # Minimum coverage enforced

# Format and lint code (uses ruff)
bin/format.sh

# Watch tests during development
bin/watch_unit_tests.sh

# Build Docker image with version tagging
bin/build.sh

# Run code analysis and security checks
bin/analyze_code.sh

# Full verification (clean → analyze → test)
make verify
```

### Testing

```bash
# Run all unit tests
poetry run pytest tests/unit

# Run with verbose output
poetry run pytest tests/unit -v

# Run specific test file
poetry run pytest tests/unit/test_specific.py

# Run without coverage
poetry run pytest tests/unit --no-cov
```

### Makefile Targets

- `make bootstrap`: Install dependencies and setup environment
- `make format`: Format code with ruff
- `make build`: Build Docker image
- `make test`: Run unit tests
- `make verify`: Full verification pipeline (clean → analyze → test)
- `make start`: Start Docker container
- `make stop`: Stop Docker container

## Docker Deployment

The application is containerized using a Python 3.11-slim base image with Poetry for dependency management.

### Using Docker Run

```bash
docker run --env-file ./.env.secrets \
  --mount type=bind,source="$(pwd)/output_docker",target=/src/output \
  craftsmanadam/ai-news-feed:latest
```

### Using Docker Compose

```bash
docker compose up
```

The compose file:
- Loads secrets from `.env.secrets`
- Names the container `ai-news-feed-1`
- Runs the full pipeline on startup

## Project Structure

```
ai-news-feed/
├── src/ai_news_feed/          # Main application code
│   ├── cli.py                 # Typer CLI interface
│   ├── models.py              # Pydantic data models
│   ├── config.py              # Settings and configuration
│   ├── pipeline/              # Pipeline stages
│   │   ├── collect.py         # RSS feed collection
│   │   ├── dedupe.py          # Deduplication logic
│   │   ├── rank.py            # Relevance ranking
│   │   └── summarize.py       # AI-powered summarization
│   ├── sources/               # Data source integrations
│   │   └── rss.py             # RSS feed fetcher
│   └── storage/               # Output writers
│       └── rss_md_writer.py   # Markdown formatter
├── tests/                     # Test suite
│   └── unit/                  # Unit tests
├── bin/                       # Development scripts
├── output/                    # Generated output files
├── rss_feeds.yaml            # RSS feed configuration
├── pyproject.toml            # Poetry configuration
├── Dockerfile                # Container build
├── docker-compose.yml        # Compose configuration
└── Makefile                  # Development automation
```

## AI Integration

The summarization step uses pydantic-ai with:

- **Provider**: OpenAI-compatible (GitHub Models API endpoint)
- **Model**: Phi-4 (configurable via `DEFAULT_MODEL` in `summarize.py`)
- **Output**: Structured `DailyBrief` using pydantic-ai's `PromptedOutput`
- **Prompt Engineering**: System prompt emphasizes:
  - Primary sources preferred
  - Factual accuracy required
  - No URL modifications
  - Concise, actionable summaries

## Code Style

- **Formatter**: ruff (replaces black)
- **Linter**: ruff with autofix enabled
- **Type hints**: Required for all function signatures
- **Import sorting**: Handled by ruff

## Contributing

This is a personal playground project, but suggestions and improvements are welcome.

## License

Not specified - personal project
