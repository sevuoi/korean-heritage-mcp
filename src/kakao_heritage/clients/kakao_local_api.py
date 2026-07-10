from __future__ import annotations

from typing import Any

import httpx

from kakao_heritage.config import settings


class KakaoLocalApiClient:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(
            timeout=settings.kakao_api_timeout_seconds
        )

    async def search_keyword(self, query: str) -> list[dict[str, Any]]:
        if not settings.kakao_rest_api_key:
            return []
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {settings.kakao_rest_api_key}"}
        async with self._client as client:
            response = await client.get(url, headers=headers, params={"query": query})
            response.raise_for_status()
            return response.json().get("documents", [])

    async def geocode(self, query: str) -> dict[str, Any] | None:
        if not settings.kakao_rest_api_key:
            return None
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {settings.kakao_rest_api_key}"}
        async with self._client as client:
            response = await client.get(url, headers=headers, params={"query": query})
            response.raise_for_status()
            documents = response.json().get("documents", [])
            return documents[0] if documents else None
