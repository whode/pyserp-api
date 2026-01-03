from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PYSERP_",
        case_sensitive=False,
    )

    env: str = "production"
    log_level: str = "INFO"
    include_debug_info: bool = False

    ssl_verify: bool = True
    semaphore_limit: int = 100
    switch_period: int = 3
    results_per_page: int | None = None
    pages_per_time_default: int | None = None
    proxies: list[str] = Field(default_factory=list)

    google_headers: dict[str, str] = Field(default_factory=dict)
    google_cookies: dict[str, str] = Field(default_factory=dict)
    google_apply_default_headers: bool = True
    google_apply_default_cookies: bool = True

    bing_headers: dict[str, str] = Field(default_factory=dict)
    bing_cookies: dict[str, str] = Field(default_factory=dict)
    bing_apply_default_headers: bool = True
    bing_apply_default_cookies: bool = False

    @field_validator("semaphore_limit", "switch_period")
    @classmethod
    def _positive_int(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("value must be greater than zero")
        return value

    @field_validator("results_per_page", "pages_per_time_default", mode="before")
    @classmethod
    def _empty_str_to_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("results_per_page", "pages_per_time_default")
    @classmethod
    def _positive_optional_int(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("value must be greater than zero")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
