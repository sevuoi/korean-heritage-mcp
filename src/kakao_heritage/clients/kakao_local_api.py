from __future__ import annotations

import html
import re
from typing import Any
from urllib.parse import urlparse

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

    def geocode_region(self, query: str) -> dict[str, Any] | None:
        """Geocode a bare region name, preferring the highest-level match.

        An ambiguous name such as "양평" matches both neighborhood-level
        "서울 영등포구 양평동1가" and county-level "경기 양평군"; the shortest
        address (fewest depth tokens) is the broader administrative region.
        """
        documents = self._get(
            "https://dapi.kakao.com/v2/local/search/address.json", {"query": query}
        ).get("documents", [])
        regions = [d for d in documents if d.get("address_type") == "REGION"]
        if regions:
            return min(
                regions,
                key=lambda d: len(str(d.get("address_name") or "").split()),
            )
        if documents:
            return documents[0]
        keyword_results = self.search_keyword(query, size=1)
        return keyword_results[0] if keyword_results else None

    def resolve_place_url(self, url: str) -> dict[str, Any] | None:
        """Resolve a public Kakao place URL without requiring a REST API key."""
        parsed = urlparse(url)
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.hostname != "place.map.kakao.com"
            or not re.fullmatch(r"/\d+/?", parsed.path)
        ):
            return None
        place_id = parsed.path.strip("/")
        canonical_url = f"https://place.map.kakao.com/{place_id}"
        if self._client is not None:
            response = self._client.get(canonical_url)
        else:
            with httpx.Client(timeout=settings.kakao_api_timeout_seconds) as client:
                response = client.get(canonical_url)
        response.raise_for_status()
        return parse_kakao_place_html(response.text)

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


def parse_kakao_place_html(page: str) -> dict[str, Any] | None:
    """Extract public place metadata embedded in a Kakao place page."""

    def meta(name: str) -> str:
        match = re.search(
            rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)',
            page,
            flags=re.IGNORECASE,
        )
        return html.unescape(match.group(1)).strip() if match else ""

    coordinates = re.search(
        r"[?&]m=([+-]?\d+(?:\.\d+)?)%2C([+-]?\d+(?:\.\d+)?)",
        page,
        flags=re.IGNORECASE,
    )
    if not coordinates:
        return None
    longitude, latitude = coordinates.groups()
    return {
        "place_name": meta("twitter:title"),
        "address_name": meta("twitter:description"),
        "x": longitude,
        "y": latitude,
    }
