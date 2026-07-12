from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient
from kakao_heritage.exceptions import ToolError
from kakao_heritage.services.distance_service import haversine_km
from kakao_heritage.services.heritage_codes import city_code
from kakao_heritage.services.trip_service import visit_place_for
from kakao_heritage.utils.map_links import build_map_link


def find_nearby_heritage(
    latitude: float | None = None,
    longitude: float | None = None,
    location: str | None = None,
    region: str | None = None,
    map_place_url: str | None = None,
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

    kakao = KakaoLocalApiClient()
    resolved_with_kakao = False
    resolved_from_place_url = False
    region_name = region or ""
    try:
        if latitude is None and longitude is None and map_place_url:
            resolved = kakao.resolve_place_url(map_place_url)
            if resolved:
                latitude, longitude = float(resolved["y"]), float(resolved["x"])
                location = location or str(resolved.get("place_name") or "")
                region_name = region_name or str(resolved.get("address_name") or "")
                resolved_from_place_url = True
        if latitude is None and longitude is None and kakao.configured:
            resolved = None
            if location:
                resolved = kakao.geocode(location)
            elif region_name:
                resolved = kakao.geocode_region(region_name)
            if resolved:
                latitude, longitude = float(resolved["y"]), float(resolved["x"])
                resolved_with_kakao = True

        if (
            latitude is not None
            and longitude is not None
            and not city_code(region_name)
        ):
            if kakao.configured:
                resolved_region = kakao.region_from_coordinates(longitude, latitude)
                region_name = (
                    str(resolved_region.get("region_1depth_name") or "")
                    if resolved_region
                    else ""
                )
            if not region_name:
                region_name = location or ""

        if not region_name:
            region_name = location or ""
        parent_city_code = city_code(region_name)
        if not parent_city_code:
            return {
                "success": False,
                "error": {
                    "code": "MAP_CONTEXT_REQUIRED",
                    "message": (
                        "지도 도구에서 확인한 위도, 경도와 시도 지역명을 함께 "
                        "전달해 주세요. 예: latitude, longitude, region='서울'."
                    ),
                    "recoverable": True,
                    "required_input": ["latitude", "longitude", "region"],
                },
            }
        if latitude is None or longitude is None:
            return {
                "success": False,
                "error": {
                    "code": "MAP_COORDINATES_REQUIRED",
                    "message": (
                        f"{location or region_name}의 정확한 주변 검색을 위해 먼저 지도 "
                        "도구에서 위도·경도를 확인해 주세요. 지역 전체 결과를 반경 "
                        "검색 결과로 대신 제공하지 않습니다."
                    ),
                    "recoverable": True,
                    "required_input": ["latitude", "longitude", "region"],
                },
            }
        heritage_items = HeritageApiClient().get_list(
            city_code=parent_city_code, page_unit=500
        )
    except httpx.HTTPError:
        return {
            "success": False,
            "error": {
                "code": "EXTERNAL_API_UNAVAILABLE",
                "message": "국가유산청 API에 연결하지 못했습니다.",
                "recoverable": True,
                "required_input": [],
            },
        }

    allowed_types = set(designation_types or [])
    filtered_items = [
        item
        for item in heritage_items
        if not allowed_types or item.get("designation_type") in allowed_types
    ]
    max_results = max(1, min(limit, 20))
    warnings: list[str] = []

    results: list[dict[str, Any]] = []
    radius = max(0.1, min(radius_km, 50.0))
    for item in filtered_items:
        item_latitude = item.get("latitude")
        item_longitude = item.get("longitude")
        if item_latitude is None or item_longitude is None:
            continue
        distance = haversine_km(
            latitude,
            longitude,
            float(item_latitude),
            float(item_longitude),
        )
        if distance <= radius:
            visit_place = visit_place_for(item)
            results.append(
                {
                    "heritage": item,
                    "visit_place": visit_place,
                    "distance_km": distance,
                    "map_url": build_map_link(
                        visit_place,
                        latitude=float(item_latitude),
                        longitude=float(item_longitude),
                        address=item.get("address"),
                    ),
                }
            )
    results.sort(key=lambda entry: float(entry["distance_km"]))

    if period:
        warnings.append("시대 필터는 개별 상세 정보에서 추가 확인이 필요합니다.")
    sources = ["국가유산청 국가유산 정보 Open API"]
    if resolved_with_kakao:
        sources.append("Kakao Local API")
    if resolved_from_place_url:
        sources.append("카카오맵 공개 장소 페이지")
    return {
        "success": True,
        "query": {
            "location": location,
            "region": region_name,
            "map_place_url": map_place_url,
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": radius_km,
            "designation_types": designation_types,
            "period": period,
        },
        "data": {
            "search_mode": "distance",
            "reference_location": {
                "name": location,
                "region": region_name,
                "latitude": latitude,
                "longitude": longitude,
            },
            "results": results[:max_results],
        },
        "sources": sources,
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": warnings,
    }
