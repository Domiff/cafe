from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    IS_DEBUG: bool = Field(default=True)
    IS_DOCKERIZED: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="CAFE_"
    )


class DBSettings(AppSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    POSTGRES_DB: str = "POSTGRES_DB"
    POSTGRES_USER: str = "POSTGRES_USER"
    POSTGRES_PASSWORD: str = "POSTGRES_PASSWORD"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    def get_pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self,
            "DB_URL",
            self.get_pg_url() if self.IS_DOCKERIZED else self.SQLITE_URL,
        )


class LoginSettings(AppSettings):
    LOGTAIL_TOKEN: str
    LOGTAIL_HOST: str


class AdminSettings(AppSettings):
    SECRET_KEY: str


class StorageSettings(AppSettings):
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET_NAME: str = ""
    AWS_S3_ENDPOINT_URL: str = ""
    AWS_DEFAULT_ACL: str = ""
    AWS_S3_USE_SSL: bool = True


class Settings(AppSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    admin: AdminSettings = AdminSettings()
    logging: LoginSettings = LoginSettings()
    storage: StorageSettings = StorageSettings()


settings = Settings()
