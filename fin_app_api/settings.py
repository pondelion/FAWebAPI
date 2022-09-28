import os
from typing import Optional
import secrets

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    # SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    LOCAL_DB_USERNAME: str
    LOCAL_DB_PASSWORD: str
    LOCAL_DB_HOST: str = '127.0.0.1'
    LOCAL_DB_NAME: str
    LOCAL_DB_PORT: int = 3306

    DEFAULT_DB_RECORD_REFRESH_SECS: int = 5*60

    DISABLE_AUTH: bool = False

    @property
    def LOCAL_MYSQL_DATABASE_URI(self) -> str:
        return f'mysql://{self.LOCAL_DB_USERNAME}:{self.LOCAL_DB_PASSWORD}@{self.LOCAL_DB_HOST}:{self.LOCAL_DB_PORT}/{self.LOCAL_DB_NAME}?charset=utf8mb4'


settings = Settings(
    SERVER_HOST='http://127.0.0.0.1',
    LOCAL_DB_USERNAME=os.environ['LOCAL_MYSQL_USER'],
    LOCAL_DB_PASSWORD=os.environ['LOCAL_MYSQL_PASSWORD'],
    LOCAL_DB_PORT=int(os.environ.get('LOCAL_DB_PORT', '3306')),
    LOCAL_DB_NAME=os.environ['LOCAL_MYSQL_DATABASE'],
    DISABLE_AUTH=False
)
