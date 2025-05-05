import os
from functools import lru_cache

# 1) Pull in BaseSettings from pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict
# 2) Field, types still come from pydantic itself
from pydantic import AnyUrl, Field


# pick up APP_ENV so we can load resources/.env.<env>
APP_ENV = os.getenv("APP_ENV", "local").lower()
ENV_FILE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "resources", f".env.{APP_ENV}"
)


class Settings(BaseSettings):
    # ─── RPC Endpoints ───────────────────────────────────────


    # ─── Redis Connection ───────────────────────────────────
    redis_url: AnyUrl      = Field("redis://localhost:6379/0",
                                   env="REDIS_URL")

    # ─── Alerts ─────────────────────────────────────────────
    email_smtp_port: int      = Field(587,   env="EMAIL_SMTP_PORT")

    slack_webhook_url: AnyUrl | None   = Field(None, env="SLACK_WEBHOOK_URL")
    discord_webhook_url: AnyUrl | None = Field(None, env="DISCORD_WEBHOOK_URL")

    # ─── Other Settings ────────────────────────────────────
    alert_timeout_seconds: int = Field(
        300,
        env="ALERT_TIMEOUT_SECONDS",
        description="Seconds before a lock is considered stuck"
    )
    app_env: str = Field(
        APP_ENV,
        env="APP_ENV",
        description="Which .env file was loaded"
    )

    # ─── Pydantic-Settings config ───────────────────────────
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Cached instance so we only read/validate once.
    """
    return Settings()
