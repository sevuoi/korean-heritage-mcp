from __future__ import annotations

from typing import Any

from kakao_heritage.utils.map_links import build_map_link

VENUE_KEYWORDS = ("박물관", "미술관", "기념관", "전시관", "불국사", "석굴암")
GENERIC_MANAGERS = ("", "개인", "미상", "관리자")


def visit_place_for(item: dict[str, Any]) -> str:
    name = str(item.get("name") or "문화유산")
    manager = str(item.get("manager") or "").strip()
    if manager not in GENERIC_MANAGERS and (
        manager in name or any(keyword in manager for keyword in VENUE_KEYWORDS)
    ):
        return manager
    return name


def _group_key(item: dict[str, Any]) -> str:
    latitude, longitude = item.get("latitude"), item.get("longitude")
    if latitude is not None and longitude is not None:
        return f"coordinate:{float(latitude):.3f},{float(longitude):.3f}"
    manager = str(item.get("manager") or "").strip()
    if manager not in GENERIC_MANAGERS and (
        manager in str(item.get("name") or "")
        or any(keyword in manager for keyword in VENUE_KEYWORDS)
    ):
        return f"manager:{manager}"
    return f"name:{item.get('name')}"


def _group_places(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for item in items:
        name = str(item.get("name") or "")
        if not name:
            continue
        key = _group_key(item)
        if key not in groups:
            groups[key] = {
                "visit_place": visit_place_for(item),
                "representative": item,
                "featured_heritage": [],
            }
        featured = groups[key]["featured_heritage"]
        if name not in featured:
            featured.append(name)
    merged: dict[str, dict[str, Any]] = {}
    for key, group in groups.items():
        representative_name = str(group["representative"].get("name") or "")
        visit_place = str(group["visit_place"])
        merge_key = (
            f"venue:{visit_place}" if visit_place != representative_name else key
        )
        if merge_key not in merged:
            merged[merge_key] = group
            continue
        featured = merged[merge_key]["featured_heritage"]
        for name in group["featured_heritage"]:
            if name not in featured:
                featured.append(name)
    return list(merged.values())


def create_trip_plan(
    region: str,
    start_location: str | None = None,
    heritage_items: list[dict[str, Any]] | None = None,
    days: int = 1,
    max_places_per_day: int = 5,
    exclude_places: list[str] | None = None,
    plan_variant: int = 1,
) -> dict[str, Any]:
    days = max(1, min(days, 7))
    max_places_per_day = max(1, min(max_places_per_day, 10))
    excluded = {place.replace(" ", "") for place in (exclude_places or [])}
    places = [
        place
        for place in _group_places(heritage_items or [])
        if not any(
            excluded_name in candidate.replace(" ", "")
            for excluded_name in excluded
            for candidate in [place["visit_place"], *place["featured_heritage"]]
        )
    ]
    requested_places = days * max_places_per_day
    if places:
        offset = (max(1, plan_variant) - 1) * requested_places
        if offset >= len(places):
            offset %= len(places)
        places = places[offset : offset + requested_places]
    itinerary = []
    for day in range(1, days + 1):
        day_places = places[(day - 1) * max_places_per_day : day * max_places_per_day]
        stops = []
        for index, place in enumerate(day_places, start=1):
            item = place["representative"]
            visit_place = place["visit_place"]
            stops.append(
                {
                    "order": index,
                    "visit_place": visit_place,
                    "featured_heritage": place["featured_heritage"],
                    "heritage": item,
                    "address": item.get("address"),
                    "recommended_duration_minutes": 120
                    if len(place["featured_heritage"]) > 1
                    else 60,
                    "travel_minutes_from_previous": None,
                    "travel_time_is_estimate": False,
                    "visit_note": (
                        "운영시간·전시 여부는 이 방문지의 map_url 카카오맵 "
                        "링크에서 바로 확인할 수 있습니다. 링크를 함께 안내하세요."
                    ),
                    "map_url": build_map_link(
                        visit_place,
                        latitude=item.get("latitude"),
                        longitude=item.get("longitude"),
                        address=item.get("address"),
                    ),
                }
            )
        itinerary.append(
            {
                "day": day,
                "title": f"{region} 문화유산 일정 {day}일차",
                "stops": stops,
                "meal_area": region,
                "parking_notes": [
                    "주차 정보는 각 방문지의 map_url 카카오맵 링크에서 바로 "
                    "확인할 수 있습니다. 사용자에게 링크를 함께 안내하세요."
                ],
                "travel_notes": ["이동시간은 실제 교통상황에 따라 달라집니다."],
            }
        )
    return {
        "region": region,
        "start_location": start_location,
        "days": days,
        "plan_variant": max(1, plan_variant),
        "excluded_places": sorted(excluded),
        "itinerary": itinerary,
    }
