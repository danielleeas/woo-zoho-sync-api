import os
import secrets
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:1027/database")
    ZOHO_ACCOUNTS_URL: str = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com")
    ZOHO_CLIENT_ID: str = os.getenv("ZOHO_CLIENT_ID", "1000.0000000000000000")
    ZOHO_CLIENT_SECRET: str = os.getenv("ZOHO_CLIENT_SECRET", "00000000000000000000000000000000")
    ZOHO_REDIRECT_URI: str = os.getenv("ZOHO_REDIRECT_URI", "http://example.com/oauth/callback")
    ZOHO_ORGANIZATION_ID: str = os.getenv("ZOHO_ORGANIZATION_ID", "00000000000000000000000000000000")
    WCM_CONSUMER_KEY: str = os.getenv("WCM_CONSUMER_KEY", "00000000000000000000000000000000")
    WCM_CONSUMER_SECRET: str = os.getenv("WCM_CONSUMER_SECRET", "00000000000000000000000000000000")
    WCM_URL: str = os.getenv("WCM_URL", "https://www.wcm.com")
    
    class Config:
        env_file = ".env"

def reload_env():
    """Reload environment variables from .env file"""
    load_dotenv(override=True)

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    reload_env()
    return Settings()

# For backward compatibility
settings = get_settings()
