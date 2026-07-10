from __future__ import annotations

from typing import Any

from kakao_heritage.services.trip_service import create_trip_plan


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
    heritage_items = [
        {
            "name": "불국사",
            "address": "경북 경주시",
            "latitude": 35.79,
            "longitude": 129.33,
            "designation_type": "사찰",
        },
        {
            "name": "석굴암",
            "address": "경북 경주시",
            "latitude": 35.8,
            "longitude": 129.33,
            "designation_type": "사찰",
        },
        {
            "name": "첨성대",
            "address": "경북 경주시",
            "latitude": 35.83,
            "longitude": 129.21,
            "designation_type": "유적",
        },
    ]
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
        },
        "data": plan,
        "summary_markdown": "",
        "sources": ["국가유산청"],
        "generated_at": "",
        "warnings": ["운영시간·요금 확인 필요"],
    }
