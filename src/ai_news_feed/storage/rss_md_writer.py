from pathlib import Path
from datetime import datetime, timezone, UTC
from ai_news_feed.config import settings
from ai_news_feed.models import DailyBrief


def _build_md(brief: DailyBrief) -> list[str]:
    lines: list[str] = []
    lines.append(f"# AI News Brief {brief.date.date().isoformat()}")
    lines.append("")
    if brief.sources:
        lines.append("## Sources")
        for s in brief.sources:
            lines.append(f"- {s}")
        lines.append("")
    lines.append("## Items")
    for item in brief.items:
        lines.append(f"- [{item.title}]({item.url}) ({item.source})")
        if item.raw_summary:
            lines.append(f"  - {item.raw_summary.strip()}")
    lines.append("")
    return lines


def _output_file() -> Path:
    settings.feed_output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%d")
    return settings.feed_output_dir / f"brief_{stamp}.md"


def write_brief_md(brief: DailyBrief) -> Path:
    brief_as_md = "\n".join(_build_md(brief))
    output_file = _output_file()
    output_file.write_text(brief_as_md, encoding="utf-8")
    return output_file
