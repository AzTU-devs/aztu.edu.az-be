from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30

    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: str | None = None

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Admin seeding (used once on first startup if admin_users table is empty)
    ADMIN_SEED_USERNAME: str | None = None
    ADMIN_SEED_PASSWORD: str | None = None

    # OpenAI
    OPEN_AI_KEY: str = ""

    # Scopus (article counters)
    SCOPUS_API_KEY: str = ""

    # App behaviour
    ENVIRONMENT: str = "production"  # development | production
    ALLOWED_ORIGINS: list[str] = [
        "https://aztu.edu.az",
        "https://www.aztu.edu.az",
    ]
    MAX_UPLOAD_SIZE_BYTES: int = 20 * 1024 * 1024  # 10 MB

    # Security headers / CORS extras
    ALLOW_PRIVATE_NETWORK_ACCESS: bool = False

    # Randomized docs path; if unset, docs are disabled
    DOCS_TOKEN: str | None = None

    # Public base URL used to build absolute media URLs (no trailing slash)
    PUBLIC_BASE_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        if not v or len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be set and at least 32 characters")
        return v

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def no_wildcard_origin(cls, v: list[str]) -> list[str]:
        if "*" in v:
            raise ValueError(
                "ALLOWED_ORIGINS must not contain '*' — list explicit origins instead"
            )
        return v

    @model_validator(mode="after")
    def production_guards(self) -> "Settings":
        if self.ENVIRONMENT == "development":
            dev_origins = ["http://localhost:3000", "http://localhost:5173"]
            for origin in dev_origins:
                if origin not in self.ALLOWED_ORIGINS:
                    self.ALLOWED_ORIGINS.append(origin)
        return self


settings = Settings()
