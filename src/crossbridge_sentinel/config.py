import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl, Field
from pathlib import Path

APP_ENV = os.getenv("APP_ENV", "local").lower()
ENV_FILE = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..",
        "resources/env",
        f".env.{APP_ENV}",
    )
)
class Settings(BaseSettings):
    # ─── RPC Endpoints ────────────────────────────────────────
    ethereum_rpc_url: AnyUrl  = Field(..., env="ETHEREUM_RPC_URL")
    solana_rpc_url:   AnyUrl  = Field(..., env="SOLANA_RPC_URL")
    eth_bridge_addr: str  = Field(..., env="ETH_BRIDGE_ADDR")
    eth_bridge_abi_path: Path = Field(
        ..., env="ETH_BRIDGE_ABI_PATH",
        description="Filesystem path to your Ethereum bridge contract ABI JSON"
    )
    print(f"path : {eth_bridge_abi_path}")
    # ─── Redis & PubSub ──────────────────────────────────────
    redis_url:        str     = Field(
        "redis://localhost:6379/0", env="REDIS_URL"
    )

    # ─── Alerting Hooks ──────────────────────────────────────
    slack_webhook_url: AnyUrl | None = Field(
        None, env="SLACK_WEBHOOK_URL"
    )
    discord_webhook_url: AnyUrl | None = Field(
        None, env="DISCORD_WEBHOOK_URL"
    )

    # ─── Email Alerts ─────────────────────────────────────────
    email_smtp_host: str     = Field(..., env="EMAIL_SMTP_HOST")
    email_smtp_port: int     = Field(587,   env="EMAIL_SMTP_PORT")
    email_username:  str     = Field(..., env="EMAIL_SMTP_USER")
    email_password:  str     = Field(..., env="EMAIL_SMTP_PASS")

    # ─── Other Settings ──────────────────────────────────────
    alert_timeout_seconds: int = Field(
        300,
        env="ALERT_TIMEOUT_SECONDS",
        description="Seconds before a lock is considered stuck",
    )
    app_env: str = Field(
        APP_ENV,
        env="APP_ENV",
        description="Which .env file was loaded",
    )

    class Config:
        # tell Pydantic v1 exactly where to load your .env.<env> file
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"      # don’t error if there’s an extra line in .env

@lru_cache()
def get_settings() -> Settings:
    return Settings()
