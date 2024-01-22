from pydantic import PostgresDsn, Field, ConfigDict, Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='postgres_')
    host: str
    port: int
    user: str
    password: str
    db: str


class Settings(BaseSettings):
    # host: str
    # port: int
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
