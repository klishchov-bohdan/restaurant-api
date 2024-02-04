from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8', env_prefix='postgres_')
    host: str
    port: int
    user: str
    password: str
    db: str


class Settings(BaseSettings):
    # host: str
    # port: int
    postgres_test: PostgresSettings = PostgresSettings(
        _env_file='.env.test', _env_prefix='postgres_', _env_file_encoding='utf-8')
    postgres: PostgresSettings = PostgresSettings(_env_file='.env', _env_prefix='postgres_', _env_file_encoding='utf-8')


settings = Settings()
