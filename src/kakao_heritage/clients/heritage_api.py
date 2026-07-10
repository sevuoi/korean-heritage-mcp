from __future__ import annotations

from typing import Any

import httpx

from kakao_heritage.config import settings
from kakao_heritage.parsers.heritage_xml import (
    parse_heritage_detail_xml,
    parse_heritage_list_xml,
)


class HeritageApiClient:
    """Synchronous client for the National Heritage Administration XML API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client

    def _get(self, url: str, params: dict[str, str]) -> httpx.Response:
        if self._client is not None:
            response = self._client.get(url, params=params)
        else:
            with httpx.Client(timeout=settings.heritage_api_timeout_seconds) as client:
                response = client.get(url, params=params)
        response.raise_for_status()
        return response

    def get_list(
        self,
        *,
        name: str | None = None,
        designation_code: str | None = None,
        city_code: str | None = None,
        period: str | None = None,
        page_unit: int = 100,
        page_index: int = 1,
    ) -> list[dict[str, Any]]:
        params = {
            "pageUnit": str(max(1, min(page_unit, 1000))),
            "pageIndex": str(max(1, page_index)),
            "ccbaCncl": "N",
        }
        if name:
            params["ccbaMnm1"] = name
        if designation_code:
            params["ccbaKdcd"] = designation_code
        if city_code:
            params["ccbaCtcd"] = city_code
        if period:
            params["ccbaPcd1"] = period
        response = self._get(settings.heritage_api_list_url, params)
        return [item.model_dump() for item in parse_heritage_list_xml(response.text)]

    def find_by_designation(
        self, designation_code: str, designation_number: int
    ) -> dict[str, Any] | None:
        for page_index in range(1, 11):
            items = self.get_list(
                designation_code=designation_code,
                page_unit=500,
                page_index=page_index,
            )
            for item in items:
                if item.get("designation_number") == designation_number:
                    return item
            if len(items) < 500:
                break
        return None

    def get_detail(self, heritage_id: str) -> dict[str, Any] | None:
        parts = heritage_id.split("-", 2)
        if len(parts) != 3 or not all(parts):
            return None
        response = self._get(
            settings.heritage_api_detail_url,
            {"ccbaKdcd": parts[0], "ccbaAsno": parts[1], "ccbaCtcd": parts[2]},
        )
        item = parse_heritage_detail_xml(response.text)
        return item.model_dump() if item else None

    def search_first(self, name: str) -> dict[str, Any] | None:
        items = self.get_list(name=name, page_unit=20)
        exact = next((item for item in items if item.get("name") == name), None)
        return exact or (items[0] if items else None)
