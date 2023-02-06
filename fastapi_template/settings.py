import enum
from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir

from dotenv import find_dotenv
from pydantic import BaseSettings
from pydantic.types import PositiveInt, SecretStr
from yarl import URL

__all__ = ["settings"]

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    API_SERVER_PORT: PositiveInt
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    #: str: Name of API service
    API_INSTANCE_APP_NAME: str

    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr
    #: str: Postgresql database name.
    POSTGRES_DATABASE_NAME: str
    db_echo: bool = False

    #: SecretStr: Key for encrypt payload in jwt.
    AUTHJWT_SECRET_KEY: str

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            path=f"/{self.POSTGRES_DATABASE_NAME}",
        )


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))


settings: Settings = get_settings()
