from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient


def resolve_location(location: str) -> dict[str, Any]:
    client = KakaoLocalApiClient()
    if not client.configured:
        return {
            "success": False,
            "error": {
                "code": "KAKAO_API_KEY_REQUIRED",
                "message": "장소 검색을 사용하려면 서버에 KAKAO_REST_API_KEY를 설정해야 합니다.",
                "recoverable": True,
                "required_input": ["KAKAO_REST_API_KEY"],
            },
        }
    try:
        result = client.geocode(location)
    except httpx.HTTPError:
        result = None
    if not result:
        return {
            "success": False,
            "error": {
                "code": "LOCATION_NOT_FOUND",
                "message": f"장소나 주소를 찾지 못했습니다: {location}",
                "recoverable": True,
                "required_input": ["더 구체적인 장소명 또는 주소"],
            },
        }
    address = result.get("address") or {}
    road_address = result.get("road_address") or {}
    return {
        "success": True,
        "query": {"location": location},
        "data": {
            "location": {
                "name": result.get("place_name") or location,
                "address": result.get("address_name") or address.get("address_name"),
                "road_address": result.get("road_address_name")
                or road_address.get("address_name"),
                "latitude": float(result["y"]),
                "longitude": float(result["x"]),
                "source": "Kakao Local API",
            }
        },
        "sources": ["Kakao Local API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": [],
    }
