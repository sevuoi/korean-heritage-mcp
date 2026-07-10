from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.services.designation_service import normalize_designation_type
from kakao_heritage.services.heritage_codes import designation_code


def get_heritage_detail(
    name: str | None = None,
    heritage_id: str | None = None,
    designation_type: str | None = None,
    designation_number: int | None = None,
) -> dict[str, Any]:
    client = HeritageApiClient()
    try:
        summary = None
        if heritage_id:
            selected_id = heritage_id
        elif name:
            summary = client.search_first(name)
            selected_id = str(summary.get("heritage_id")) if summary else ""
        elif designation_type and designation_number is not None:
            code = designation_code(normalize_designation_type(designation_type))
            summary = (
                client.find_by_designation(code, designation_number) if code else None
            )
            selected_id = str(summary.get("heritage_id")) if summary else ""
        else:
            selected_id = ""
        detail = client.get_detail(selected_id) if selected_id else None
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
    if not detail:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "조건에 맞는 국가유산 상세 정보를 찾지 못했습니다.",
                "recoverable": True,
                "required_input": ["name, heritage_id 또는 지정 종목과 번호"],
            },
        }
    return {
        "success": True,
        "query": {
            "name": name,
            "heritage_id": heritage_id,
            "designation_type": designation_type,
            "designation_number": designation_number,
        },
        "data": {"heritage": detail},
        "sources": ["국가유산청 국가유산 정보 Open API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": [],
    }
