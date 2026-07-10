from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient
from kakao_heritage.exceptions import ToolError
from kakao_heritage.services.distance_service import haversine_km
from kakao_heritage.services.heritage_codes import city_code
from kakao_heritage.utils.map_links import build_map_link


def find_nearby_heritage(
    latitude: float | None = None,
    longitude: float | None = None,
    location: str | None = None,
    radius_km: float = 10.0,
    designation_types: list[str] | None = None,
    period: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    if (latitude is None) != (longitude is None):
        raise ToolError(
            "INVALID_COORDINATES",
            "위도와 경도는 함께 입력해야 합니다.",
            recoverable=True,
            required_input=["latitude", "longitude"],
        )
    if latitude is None and not location:
        return {
            "success": False,
            "error": ToolError(
                "LOCATION_REQUIRED",
                "기준 장소나 위도·경도를 입력해 주세요.",
                recoverable=True,
                required_input=["location 또는 latitude와 longitude"],
            ).to_dict(),
        }
    kakao = KakaoLocalApiClient()
    if not kakao.configured:
        return {
            "success": False,
            "error": {
                "code": "KAKAO_API_KEY_REQUIRED",
                "message": "주변 검색을 사용하려면 서버에 KAKAO_REST_API_KEY를 설정해야 합니다.",
                "recoverable": True,
                "required_input": ["KAKAO_REST_API_KEY"],
            },
        }
    try:
        if latitude is None or longitude is None:
            resolved = kakao.geocode(str(location))
            if not resolved:
                return {
                    "success": False,
                    "error": {
                        "code": "LOCATION_NOT_FOUND",
                        "message": f"기준 장소를 찾지 못했습니다: {location}",
                        "recoverable": True,
                        "required_input": ["더 구체적인 장소명 또는 주소"],
                    },
                }
            latitude, longitude = float(resolved["y"]), float(resolved["x"])
        region = kakao.region_from_coordinates(longitude, latitude)
        region_name = str(region.get("region_1depth_name") or "") if region else ""
        heritage_items = HeritageApiClient().get_list(
            city_code=city_code(region_name), page_unit=1000
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

    allowed_types = set(designation_types or [])
    results: list[dict[str, Any]] = []
    for item in heritage_items:
        item_latitude, item_longitude = item.get("latitude"), item.get("longitude")
        if item_latitude is None or item_longitude is None:
            continue
        if allowed_types and item.get("designation_type") not in allowed_types:
            continue
        distance = haversine_km(
            latitude, longitude, float(item_latitude), float(item_longitude)
        )
        if distance <= max(0.1, min(radius_km, 50.0)):
            results.append(
                {
                    "heritage": item,
                    "distance_km": distance,
                    "map_url": build_map_link(str(item.get("name") or "")),
                }
            )
    results.sort(key=lambda entry: float(entry["distance_km"]))
    warnings = ["시대 필터는 상세 정보 확인이 필요합니다."] if period else []
    return {
        "success": True,
        "query": {
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": radius_km,
            "designation_types": designation_types,
            "period": period,
        },
        "data": {
            "reference_location": {
                "name": location,
                "region": region_name,
                "latitude": latitude,
                "longitude": longitude,
            },
            "results": results[: max(1, min(limit, 20))],
        },
        "sources": ["국가유산청 국가유산 정보 Open API", "Kakao Local API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": warnings,
    }
