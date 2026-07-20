import hashlib
from pathlib import Path

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

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_USERNAME: str | None = None
    ELASTICSEARCH_PASSWORD: str | None = None
    SEARCH_INDEX_PREFIX: str = "aztu"

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
        "https://admin.aztu.edu.az",
        "https://www.admin.aztu.edu.az"
    ]
    MAX_UPLOAD_SIZE_BYTES: int = 20 * 1024 * 1024  # 10 MB

    # Security headers / CORS extras
    ALLOW_PRIVATE_NETWORK_ACCESS: bool = False

    # Randomized docs path; if unset, docs are disabled
    DOCS_TOKEN: str | None = None

    # API key required for public GET endpoints (skipped for aztu.edu.az domain)
    PUBLIC_API_KEY: str = ""
    # Domains exempt from the public GET API-key check (Origin/Referer host match)
    PUBLIC_API_KEY_EXEMPT_HOSTS: list[str] = [
        "aztu.edu.az",
        "www.aztu.edu.az",
        "admin.aztu.edu.az",
        "www.admin.aztu.edu.az"
    ]

    # Public base URL used to build absolute media URLs (no trailing slash)
    PUBLIC_BASE_URL: str = ""

    # Visitor analytics. The salt is mixed into sha256(salt + ip + user agent +
    # day) so the stored visitor hash cannot be reversed to an IP. Left unset it
    # is derived from JWT_SECRET_KEY: a shipped constant would be public, and the
    # IPv4 space is small enough to brute-force a known-salt digest back to an IP.
    VISIT_HASH_SALT: str = ""
    SITE_VISIT_RETENTION_DAYS: int = 400

    # RBAC
    # "audit"  — denials are logged and recorded, the request still proceeds
    # "enforce" — denials return 403
    PERMISSION_ENFORCEMENT_MODE: str = "audit"
    AUDIT_LOG_RETENTION_DAYS: int = 365
    # First-boot override: this username alone becomes super_admin, every other
    # role-less admin becomes viewer. Unset -> all role-less admins are promoted.
    RBAC_BOOTSTRAP_SUPERADMIN: str | None = None

    class Config:
        # Absolute, not ".env". A relative path resolves against the process's
        # working directory, so the file is silently skipped whenever the service
        # is started from anywhere other than the repo root — and because most
        # fields carry defaults, that failure is silent rather than loud.
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        if not v or len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be set and at least 32 characters")
        return v

    @field_validator("PERMISSION_ENFORCEMENT_MODE")
    @classmethod
    def enforcement_mode_is_known(cls, v: str) -> str:
        value = (v or "").strip().lower()
        if value not in ("audit", "enforce"):
            raise ValueError("PERMISSION_ENFORCEMENT_MODE must be 'audit' or 'enforce'")
        return value

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def no_wildcard_origin(cls, v: list[str]) -> list[str]:
        if "*" in v:
            raise ValueError(
                "ALLOWED_ORIGINS must not contain '*' — list explicit origins instead"
            )
        return v

    @model_validator(mode="after")
    def derive_visit_hash_salt(self) -> "Settings":
        if not self.VISIT_HASH_SALT.strip():
            self.VISIT_HASH_SALT = hashlib.sha256(
                f"visit-salt|{self.JWT_SECRET_KEY}".encode("utf-8")
            ).hexdigest()
        return self

    @model_validator(mode="after")
    def production_guards(self) -> "Settings":
        if self.ENVIRONMENT == "development":
            dev_origins = ["http://localhost:3000", "http://localhost:5173"]
            for origin in dev_origins:
                if origin not in self.ALLOWED_ORIGINS:
                    self.ALLOWED_ORIGINS.append(origin)
        return self


settings = Settings()
