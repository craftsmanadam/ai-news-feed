from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.secrets"), case_sensitive=True, extra="ignore"
    )

    FEED_OUTPUT_DIR: Path = Path("./output/")


settings = Settings()
