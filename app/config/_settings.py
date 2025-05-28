from pathlib import Path

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # settings FastAPI
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Athena Backend"

    SECRET_KEY: str

    JWT_ALGORITHM: str

    JWT_ACCESS_COOKIE_NAME: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_MOBILE_EXPIRE_MINUTES: int

    MAX_CONTENT_LENGTH: int = 500 * 1024 * 1024  # 100MB

    # settings db
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str


    @property
    def DATABASE_URL(self) -> str:  # noqa: N802
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    LOGLEVEL: str = "DEBUG"

    TMP_STORAGE_PATH: Path
    AGREEMENTS_STORAGE_PATH: Path
    STORAGE_TYPE: str = "S3"
    STRIPE_API_KEY: str
    STRIPE_SECRET: str
    STRIPE_WH_SECRET: str

    DO_SPACE_BUCKET: str
    DO_SPACE_FOLDER: str
    DO_SPACE_AGREEMENT_FOLDER: str
    DO_SPACE_IMAGE_FOLDER: str
    DO_SPACE_URL: str
    DO_SPACE_ORIGIN_URL: str
    DO_SPACE_KEY: str
    DO_SPACE_SECRET: str

    @property
    def DO_SPACE_URL_WITH_BUCKET(self) -> str:  # noqa: N802
        url = AnyUrl(self.DO_SPACE_URL)
        return f"{url.scheme}://{self.DO_SPACE_BUCKET}.{url.host}"

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


settings = Settings()  # type: ignore
