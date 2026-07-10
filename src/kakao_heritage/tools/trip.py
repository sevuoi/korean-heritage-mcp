from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from kakao_heritage.services.trip_service import create_trip_plan
from kakao_heritage.tools.search import search_heritage


def plan_heritage_trip(
    region: str,
    start_location: str | None = None,
    days: int = 1,
    transport: str = "car",
    themes: list[str] | None = None,
    companions: str | None = None,
    pace: str = "normal",
    include_food: bool = True,
    include_parking: bool = True,
    max_places_per_day: int = 5,
) -> dict[str, Any]:
    result_limit = max(1, min(days * max_places_per_day, 20))
    candidate_limit = min(result_limit * 4, 20)
    search_result = search_heritage(
        query=themes[0] if themes else None, region=region, limit=candidate_limit
    )
    if not search_result.get("success"):
        return search_result
    heritage_items = search_result.get("data", {}).get("results", [])
    if not heritage_items and themes:
        search_result = search_heritage(region=region, limit=candidate_limit)
        heritage_items = search_result.get("data", {}).get("results", [])
    plan = create_trip_plan(
        region=region,
        start_location=start_location,
        heritage_items=heritage_items,
        days=days,
        max_places_per_day=max_places_per_day,
    )
    return {
        "success": True,
        "query": {
            "region": region,
            "days": days,
            "transport": transport,
            "themes": themes,
            "companions": companions,
            "pace": pace,
            "include_food": include_food,
            "include_parking": include_parking,
        },
        "data": plan,
        "sources": ["국가유산청 국가유산 정보 Open API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": ["운영시간·요금·교통상황은 방문 전에 확인하세요."],
    }
