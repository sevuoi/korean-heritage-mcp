from __future__ import annotations

from typing import Any

import httpx

from kakao_heritage.config import settings
from kakao_heritage.parsers.heritage_xml import (
    parse_heritage_detail_xml,
    parse_heritage_list_xml,
)


class HeritageApiClient:
    """Client for the National Heritage Administration API.

    Heritage place data is provided as XML and parsed by the XML parser module.
    """

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(
            timeout=settings.heritage_api_timeout_seconds
        )

    async def get_list(self, query: str | None = None) -> list[dict[str, Any]]:
        url = settings.heritage_api_list_url
        params: dict[str, str] = {"searchType": "default"}
        if query:
            params["searchKeyword"] = query
        async with self._client as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            items = parse_heritage_list_xml(response.text)
            return [item.model_dump() for item in items]

    async def get_detail(self, heritage_id: str) -> dict[str, Any] | None:
        url = settings.heritage_api_detail_url
        params = {
            "ccbaKdcd": heritage_id.split("-")[0],
            "ccbaAsno": heritage_id.split("-")[1],
            "ccbaCtcd": heritage_id.split("-")[2],
        }
        async with self._client as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            item = parse_heritage_detail_xml(response.text)
            return item.model_dump() if item else None
