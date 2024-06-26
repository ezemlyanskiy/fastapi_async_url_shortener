from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env_name: str = 'Local'
    base_url: str = 'http://localhost:8000'
    db_url: str = 'sqlite+aiosqlite:///./shortener.sqlite3'

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f'Loading settings for: {settings.env_name}')
    return settings
