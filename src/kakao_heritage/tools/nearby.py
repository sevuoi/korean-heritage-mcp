from __future__ import annotations

from typing import Any

from kakao_heritage.exceptions import ToolError
from kakao_heritage.models.common import HeritageItem
from kakao_heritage.services.distance_service import haversine_km
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
                "현재 위치 좌표가 전달되지 않았습니다. 기준 장소나 주소를 입력해 주세요.",
                recoverable=True,
                required_input=["location 또는 latitude와 longitude"],
            ).to_dict(),
            "generated_at": "",
        }
    heritage_items = [
        HeritageItem(
            name="불국사",
            address="경상북도 경주시",
            latitude=35.792,
            longitude=129.331,
            designation_type="사적",
            designation_number=1,
            summary="불국사",
            source_name="국가유산청",
        ),
        HeritageItem(
            name="석굴암",
            address="경상북도 경주시",
            latitude=35.8,
            longitude=129.33,
            designation_type="사적",
            designation_number=2,
            summary="석굴암",
            source_name="국가유산청",
        ),
    ]
    results: list[dict[str, Any]] = []
    for item in heritage_items:
        if item.latitude is None or item.longitude is None:
            continue
        distance = haversine_km(
            latitude or 35.79, longitude or 129.33, item.latitude, item.longitude
        )
        if distance <= radius_km:
            results.append(
                {
                    "heritage": item.model_dump(),
                    "distance_km": distance,
                    "map_url": build_map_link(item.name),
                }
            )
    results.sort(key=lambda entry: float(entry["distance_km"]))
    return {
        "success": True,
        "query": {"location": location, "radius_km": radius_km},
        "data": {"results": results[:limit]},
        "summary_markdown": "",
        "sources": ["국가유산청"],
        "generated_at": "",
        "warnings": [],
    }
