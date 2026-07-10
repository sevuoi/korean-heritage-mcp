from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="K-Heritage Guide")
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")

    mcp_transport: str = Field(default="stdio")
    mcp_host: str = Field(default="127.0.0.1")
    mcp_port: int = Field(
        default=8000, validation_alias=AliasChoices("MCP_PORT", "PORT")
    )
    mcp_path: str = Field(default="/mcp")

    kakao_rest_api_key: str | None = Field(default=None)

    heritage_api_list_url: str = Field(
        default="http://www.khs.go.kr/cha/SearchKindOpenapiList.do"
    )
    heritage_api_detail_url: str = Field(
        default="http://www.khs.go.kr/cha/SearchKindOpenapiDt.do"
    )
    heritage_api_timeout_seconds: int = Field(default=15)
    kakao_api_timeout_seconds: int = Field(default=10)

    heritage_list_cache_ttl_seconds: int = Field(default=21600)
    heritage_detail_cache_ttl_seconds: int = Field(default=86400)
    kakao_search_cache_ttl_seconds: int = Field(default=1800)

    default_search_radius_km: float = Field(default=10.0)
    max_search_radius_km: float = Field(default=50.0)
    default_result_limit: int = Field(default=10)
    max_result_limit: int = Field(default=20)

    default_trip_days: int = Field(default=1)
    default_max_places_per_day: int = Field(default=5)


settings = Settings()
