from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient


def find_heritage_facilities(
    heritage_name: str,
    facility_types: list[str] | None = None,
    radius_m: int = 1500,
    limit_per_type: int = 5,
) -> dict[str, Any]:
    kakao = KakaoLocalApiClient()
    if not kakao.configured:
        return {
            "success": False,
            "error": {
                "code": "KAKAO_API_KEY_REQUIRED",
                "message": "주변 시설 검색을 사용하려면 서버에 KAKAO_REST_API_KEY를 설정해야 합니다.",
                "recoverable": True,
                "required_input": ["KAKAO_REST_API_KEY"],
            },
        }
    try:
        heritage = HeritageApiClient().search_first(heritage_name)
        if (
            not heritage
            or not heritage.get("longitude")
            or not heritage.get("latitude")
        ):
            return {
                "success": False,
                "error": {
                    "code": "HERITAGE_LOCATION_NOT_FOUND",
                    "message": "문화유산의 위치를 확인하지 못했습니다.",
                    "recoverable": True,
                    "required_input": ["정확한 문화유산명"],
                },
            }
        types = facility_types or ["주차장", "음식점", "카페"]
        results: list[dict[str, Any]] = []
        for facility_type in types:
            places = kakao.search_keyword(
                facility_type,
                longitude=float(heritage["longitude"]),
                latitude=float(heritage["latitude"]),
                radius_m=radius_m,
                size=limit_per_type,
            )
            for place in places[:limit_per_type]:
                results.append(
                    {
                        "name": place.get("place_name"),
                        "category": facility_type,
                        "category_name": place.get("category_name"),
                        "address": place.get("address_name"),
                        "road_address": place.get("road_address_name"),
                        "latitude": float(place["y"]) if place.get("y") else None,
                        "longitude": float(place["x"]) if place.get("x") else None,
                        "distance_m": int(place["distance"])
                        if place.get("distance")
                        else None,
                        "phone": place.get("phone"),
                        "place_url": place.get("place_url"),
                    }
                )
    except httpx.HTTPError:
        return {
            "success": False,
            "error": {
                "code": "EXTERNAL_API_UNAVAILABLE",
                "message": "국가유산청 또는 Kakao Local API에 연결하지 못했습니다.",
                "recoverable": True,
                "required_input": [],
            },
        }
    return {
        "success": True,
        "query": {
            "heritage_name": heritage_name,
            "facility_types": types,
            "radius_m": radius_m,
            "limit_per_type": limit_per_type,
        },
        "data": {"heritage": heritage, "results": results},
        "sources": ["국가유산청 국가유산 정보 Open API", "Kakao Local API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": [],
    }
