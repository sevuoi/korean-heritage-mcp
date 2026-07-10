from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.services.designation_service import normalize_designation_type
from kakao_heritage.services.heritage_codes import designation_code
from kakao_heritage.services.trip_service import visit_place_for
from kakao_heritage.utils.map_links import build_map_link


def find_heritage_by_designation(
    designation_type: str, designation_number: int
) -> dict[str, Any]:
    normalized = normalize_designation_type(designation_type)
    code = designation_code(normalized)
    if not code:
        return {
            "success": False,
            "error": {
                "code": "UNSUPPORTED_DESIGNATION_TYPE",
                "message": f"지원하지 않는 지정 종목입니다: {designation_type}",
                "recoverable": True,
                "required_input": ["올바른 designation_type"],
            },
        }
    try:
        summary = HeritageApiClient().find_by_designation(code, designation_number)
        detail = (
            HeritageApiClient().get_detail(str(summary["heritage_id"]))
            if summary
            else None
        )
    except httpx.HTTPError:
        return {
            "success": False,
            "error": {
                "code": "HERITAGE_API_UNAVAILABLE",
                "message": "국가유산청 API에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.",
                "recoverable": True,
                "required_input": [],
            },
        }
    if not summary:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "해당 지정 종목과 번호로 확인되는 국가유산을 찾지 못했습니다.",
                "recoverable": True,
                "required_input": ["designation_type", "designation_number"],
            },
        }
    result = detail or summary
    result["visit_place"] = visit_place_for(result)
    result["map_url"] = build_map_link(
        result["visit_place"],
        latitude=result.get("latitude"),
        longitude=result.get("longitude"),
        address=result.get("address"),
    )
    return {
        "success": True,
        "query": {
            "designation_type": normalized,
            "designation_number": designation_number,
        },
        "data": {"results": [result]},
        "sources": ["국가유산청 국가유산 정보 Open API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": [],
    }
