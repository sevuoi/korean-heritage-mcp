from __future__ import annotations

from typing import Any


def get_heritage_detail(
    name: str | None = None,
    heritage_id: str | None = None,
    designation_type: str | None = None,
    designation_number: int | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "query": {
            "name": name,
            "heritage_id": heritage_id,
            "designation_type": designation_type,
            "designation_number": designation_number,
        },
        "data": {
            "heritage": {
                "name": name or "불국사",
                "designation_type": designation_type or "사적",
                "designation_number": designation_number or 1,
                "address": "경상북도 경주시",
                "latitude": 35.792,
                "longitude": 129.331,
            }
        },
        "summary_markdown": "",
        "sources": ["국가유산청"],
        "generated_at": "",
        "warnings": [],
    }
