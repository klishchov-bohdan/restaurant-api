from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8', env_prefix='postgres_')
    host: str
    port: int
    user: str
    password: str
    db: str


class RedisSettings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8', env_prefix='postgres_')
    server: str
    port: int


class Settings(BaseSettings):
    # host: str
    # port: int
    api_prefix: str = '/api/v1'
    redis: RedisSettings = RedisSettings(_env_file='.env', _env_prefix='redis_', _env_file_encoding='utf-8')
    postgres_test: PostgresSettings = PostgresSettings(
        _env_file='.env', _env_prefix='test_postgres_', _env_file_encoding='utf-8')
    postgres: PostgresSettings = PostgresSettings(_env_file='.env', _env_prefix='postgres_', _env_file_encoding='utf-8')


settings = Settings()
