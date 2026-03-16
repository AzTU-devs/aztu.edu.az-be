import secrets
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
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Admin seeding (used once on first startup if admin_users table is empty)
    ADMIN_SEED_USERNAME: str | None = None
    ADMIN_SEED_PASSWORD: str | None = None

    # App behaviour
    ENVIRONMENT: str = "production"  # development | production
    ALLOWED_ORIGINS: list[str] = ["https://aztu.edu.az"]
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        # Allow empty string only in development; production requires 32+ chars
        if v and len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        return v

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def no_wildcard_in_production(cls, v: list[str]) -> list[str]:
        return v

    @model_validator(mode="after")
    def production_guards(self) -> "Settings":
        if self.ENVIRONMENT == "production":
            if not self.JWT_SECRET_KEY or len(self.JWT_SECRET_KEY) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must be set and at least 32 characters in production. "
                    f"Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
                )
            if "*" in self.ALLOWED_ORIGINS:
                raise ValueError("Wildcard CORS origin not allowed in production")
        return self


settings = Settings()
