from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str


class RedisSettings(BaseSettings):
    server: str
    port: int


class RabbitmqSettings(BaseSettings):
    host: str
    port: int
    port_web: int
    default_user: str
    default_password: str


class Settings(BaseSettings):
    # host: str
    # port: int
    api_prefix: str = '/api/v1'
    rabbitmq: RabbitmqSettings = RabbitmqSettings(_env_file='.env', _env_prefix='rabbitmq_', _env_file_encoding='utf-8')
    redis: RedisSettings = RedisSettings(_env_file='.env', _env_prefix='redis_', _env_file_encoding='utf-8')
    postgres_test: PostgresSettings = PostgresSettings(
        _env_file='.env', _env_prefix='test_postgres_', _env_file_encoding='utf-8')
    postgres: PostgresSettings = PostgresSettings(_env_file='.env', _env_prefix='postgres_', _env_file_encoding='utf-8')


settings = Settings()
