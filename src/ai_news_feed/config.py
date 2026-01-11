from pathlib import Path
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_news_feed.models import FeedConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.secrets"), case_sensitive=True, extra="ignore"
    )

    feed_output_dir: Path = Path("./output/")
    rss_feeds_file: Path = Path("rss_feeds.yaml")

    def load_feeds(self) -> list[FeedConfig]:
        data = yaml.safe_load(self.rss_feeds_file.read_text())
        return [FeedConfig(**item) for item in data["feeds"]]


settings = Settings()
