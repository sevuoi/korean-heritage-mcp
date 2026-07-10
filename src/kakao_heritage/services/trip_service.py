from __future__ import annotations

from typing import Any


def create_trip_plan(
    region: str,
    start_location: str | None = None,
    heritage_items: list[dict[str, Any]] | None = None,
    days: int = 1,
    max_places_per_day: int = 5,
) -> dict[str, Any]:
    items = heritage_items or []
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        name = str(item.get("name") or "")
        if name and name not in seen:
            deduped.append(item)
            seen.add(name)
    selected = deduped[:max_places_per_day]
    stops = []
    for index, item in enumerate(selected, start=1):
        stops.append(
            {
                "order": index,
                "heritage": {
                    "name": item.get("name"),
                    "address": item.get("address"),
                    "latitude": item.get("latitude"),
                    "longitude": item.get("longitude"),
                    "designation_type": item.get("designation_type"),
                },
                "recommended_duration_minutes": 60,
                "travel_minutes_from_previous": 20 if index > 1 else 0,
                "travel_time_is_estimate": True,
                "visit_note": "추천 관람시간",
                "map_url": "https://map.kakao.com/",
            }
        )
    return {
        "region": region,
        "days": days,
        "itinerary": [
            {
                "day": 1,
                "title": f"{region} 문화유산 일정",
                "stops": stops,
                "meal_area": region,
                "parking_notes": ["주차장 확인 필요"],
                "travel_notes": ["예상 이동시간 포함"],
            }
        ],
    }
