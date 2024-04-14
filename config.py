from logging import getLogger
from typing import Literal

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


def get_current_external_ip() -> str | None:
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error while getting external IP: {e}")
        return None
    return response.json()["ip"]


class Config(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    # LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@"
            f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    REDIS_HOST: str
    REDIS_PORT: int

    EXTERNAL_IP: str = get_current_external_ip()

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=False)


configuration = Config()
