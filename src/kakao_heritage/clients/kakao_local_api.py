from __future__ import annotations

from typing import Any

import httpx

from kakao_heritage.config import settings


class KakaoLocalApiClient:
    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client

    @property
    def configured(self) -> bool:
        return bool(settings.kakao_rest_api_key)

    def _get(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        if not settings.kakao_rest_api_key:
            return {"documents": []}
        headers = {"Authorization": f"KakaoAK {settings.kakao_rest_api_key}"}
        if self._client is not None:
            response = self._client.get(url, headers=headers, params=params)
        else:
            with httpx.Client(timeout=settings.kakao_api_timeout_seconds) as client:
                response = client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search_keyword(
        self,
        query: str,
        *,
        longitude: float | None = None,
        latitude: float | None = None,
        radius_m: int | None = None,
        size: int = 15,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"query": query, "size": max(1, min(size, 15))}
        if longitude is not None and latitude is not None:
            params.update({"x": longitude, "y": latitude})
        if radius_m is not None:
            params["radius"] = max(0, min(radius_m, 20000))
        return self._get(
            "https://dapi.kakao.com/v2/local/search/keyword.json", params
        ).get("documents", [])

    def geocode(self, query: str) -> dict[str, Any] | None:
        documents = self._get(
            "https://dapi.kakao.com/v2/local/search/address.json", {"query": query}
        ).get("documents", [])
        if documents:
            return documents[0]
        keyword_results = self.search_keyword(query, size=1)
        return keyword_results[0] if keyword_results else None

    def region_from_coordinates(
        self, longitude: float, latitude: float
    ) -> dict[str, Any] | None:
        documents = self._get(
            "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json",
            {"x": longitude, "y": latitude},
        ).get("documents", [])
        administrative = next(
            (item for item in documents if item.get("region_type") == "H"), None
        )
        return administrative or (documents[0] if documents else None)
