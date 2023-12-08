from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # constants
    URL_PREFIX: str = '/api/v1/'
    DEFAULT_STR: str = 'To be implemented in .env file'
    SUPER_ONLY: str = '__Только для суперюзеров:__ '
    AUTH_ONLY: str = '__Только для авторизованных пользователей:__ '
    ALL_USERS: str = '__Для всех пользователей:__ '

    # environment variables
    app_title: str = DEFAULT_STR
    app_description: str = DEFAULT_STR
    secret_key: SecretStr = DEFAULT_STR
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'  # for GitHub tests

    # authentication
    admin_email: EmailStr = 'adm@adm.com'
    admin_password: str = 'adm'
    token_lifetime: int = 3600
    token_url: str = 'auth/jwt/login'
    auth_backend_name: str = 'jwt'
    password_length: int = 3

    # post settings
    post_min_anystr_length: int = 3
    title_max_length: int = 100
    content_max_length: int = 5000

    # cache
    redis_url: str = 'redis://redis:6379'  # for GitHub tests
    redis_expire: int = 3600
    redis_prefix: str = 'post:'

    # background tasks
    celery_task_period: int = 3600
    celery_broker_url: str = DEFAULT_STR


settings = Settings()
