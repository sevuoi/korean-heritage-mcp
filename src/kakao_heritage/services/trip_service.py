from __future__ import annotations

from typing import Any

from kakao_heritage.utils.map_links import build_map_link


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
    days = max(1, min(days, 7))
    max_places_per_day = max(1, min(max_places_per_day, 10))
    selected = deduped[: days * max_places_per_day]
    itinerary = []
    for day in range(1, days + 1):
        day_items = selected[(day - 1) * max_places_per_day : day * max_places_per_day]
        stops = []
        for index, item in enumerate(day_items, start=1):
            name = str(item.get("name") or "")
            stops.append(
                {
                    "order": index,
                    "heritage": item,
                    "recommended_duration_minutes": 60,
                    "travel_minutes_from_previous": 20 if index > 1 else 0,
                    "travel_time_is_estimate": True,
                    "visit_note": "운영시간과 관람 조건은 방문 전 확인하세요.",
                    "map_url": build_map_link(name),
                }
            )
        itinerary.append(
            {
                "day": day,
                "title": f"{region} 문화유산 일정 {day}일차",
                "stops": stops,
                "meal_area": region,
                "parking_notes": ["개별 방문지의 최신 주차 정보를 확인하세요."],
                "travel_notes": ["이동시간은 실제 교통상황에 따라 달라집니다."],
            }
        )
    return {
        "region": region,
        "days": days,
        "itinerary": itinerary,
    }
