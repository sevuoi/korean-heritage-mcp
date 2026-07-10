from __future__ import annotations

from typing import Any


def find_heritage_facilities(
    heritage_name: str,
    facility_types: list[str] | None = None,
    radius_m: int = 1500,
    limit_per_type: int = 5,
) -> dict[str, Any]:
    return {
        "success": True,
        "query": {
            "heritage_name": heritage_name,
            "facility_types": facility_types,
            "radius_m": radius_m,
            "limit_per_type": limit_per_type,
        },
        "data": {"results": [{"name": "불국사 주변 음식점", "category": "음식점"}]},
        "summary_markdown": "",
        "sources": ["카카오 로컬"],
        "generated_at": "",
        "warnings": [],
    }
