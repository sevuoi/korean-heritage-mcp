from __future__ import annotations

from typing import Any


def search_heritage(
    query: str | None = None,
    region: str | None = None,
    designation_type: str | None = None,
    period: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    return {
        "success": True,
        "query": {
            "query": query,
            "region": region,
            "designation_type": designation_type,
            "period": period,
            "limit": limit,
        },
        "data": {
            "results": [
                {
                    "name": "불국사",
                    "address": "경상북도 경주시",
                    "designation_type": "사적",
                }
            ]
        },
        "summary_markdown": "",
        "sources": ["국가유산청"],
        "generated_at": "",
        "warnings": [],
    }
