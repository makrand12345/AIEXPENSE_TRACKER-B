from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration settings"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MONGO_URI: str | None = None
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()