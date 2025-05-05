# src/crossbridge_sentinel/config.py
import os
from pydantic import BaseSettings, AnyUrl, Field
from functools import lru_cache

APP_ENV = os.getenv("APP_ENV", "local").lower()
ENV_FILE = os.path.join(
    os.path.dirname(__file__),          
    "..",                                 
    "..",                                
    "resources",
    f".env.{APP_ENV}"
)

class Settings(BaseSettings):
    eth_rpc_url: AnyUrl      = Field(..., env='ETH_RPC_URL')
    solana_rpc_url: AnyUrl   = Field(..., env='SOLANA_RPC_URL')
    redis_url: AnyUrl        = Field(..., env='REDIS_URL')

    class Config:
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
