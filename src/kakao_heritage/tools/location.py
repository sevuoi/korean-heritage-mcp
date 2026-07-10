from __future__ import annotations

from typing import Any


def resolve_location(location: str) -> dict[str, Any]:
    return {
        "success": True,
        "query": {"location": location},
        "data": {
            "location": {
                "name": location,
                "address": None,
                "latitude": 35.79,
                "longitude": 129.33,
                "source": "placeholder",
            }
        },
        "summary_markdown": "",
        "sources": ["카카오 로컬"],
        "generated_at": "",
        "warnings": [],
    }
