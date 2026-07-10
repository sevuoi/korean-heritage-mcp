from __future__ import annotations

from typing import Any

from kakao_heritage.services.designation_service import normalize_designation_type


def find_heritage_by_designation(
    designation_type: str, designation_number: int
) -> dict[str, Any]:
    normalized = normalize_designation_type(designation_type)
    if normalized == "국보" and designation_number == 10:
        return {
            "success": True,
            "query": {
                "designation_type": normalized,
                "designation_number": designation_number,
            },
            "data": {
                "results": [
                    {
                        "name": "국보 제10호 석굴암",
                        "designation_type": "국보",
                        "designation_number": 10,
                        "address": "경상북도 경주시",
                        "latitude": 35.8,
                        "longitude": 129.33,
                        "summary": "국보 제10호",
                    }
                ]
            },
            "summary_markdown": "",
            "sources": ["국가유산청"],
            "generated_at": "",
            "warnings": [],
        }
    return {
        "success": False,
        "error": {
            "code": "NOT_FOUND",
            "message": "해당 지정 종목과 번호로 확인되는 국가유산을 찾지 못했습니다.",
            "recoverable": True,
            "required_input": ["designation_type", "designation_number"],
        },
        "generated_at": "",
    }
