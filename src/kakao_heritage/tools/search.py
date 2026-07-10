from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

import httpx

from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.services.designation_service import normalize_designation_type
from kakao_heritage.services.distance_service import haversine_km
from kakao_heritage.services.heritage_codes import (
    city_code,
    designation_code,
    region_center,
    region_heritage_terms,
    region_search_terms,
)


def _compact_result(item: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "heritage_id",
        "name",
        "designation_type",
        "designation_number",
        "period",
        "address",
        "city",
        "district",
        "manager",
        "latitude",
        "longitude",
        "image_url",
    )
    result = {key: item.get(key) for key in keys if item.get(key) is not None}
    description = str(item.get("description") or "").strip()
    if description:
        result["description_summary"] = description[:300]
    return result


def search_heritage(
    query: str | None = None,
    region: str | None = None,
    designation_type: str | None = None,
    period: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    if not any((query, region, designation_type, period)):
        return {
            "success": False,
            "error": {
                "code": "SEARCH_CONDITION_REQUIRED",
                "message": "이름, 지역, 시대 또는 지정종목 중 하나를 입력해 주세요.",
                "recoverable": True,
                "required_input": ["query, region, designation_type 또는 period"],
            },
        }
    limit = max(1, min(limit, 20))
    normalized_type = normalize_designation_type(designation_type)
    normalized_code = designation_code(normalized_type)
    if designation_type and not normalized_code:
        return {
            "success": False,
            "error": {
                "code": "UNSUPPORTED_DESIGNATION_TYPE",
                "message": f"지원하지 않는 지정 종목입니다: {designation_type}",
                "recoverable": True,
                "required_input": ["국보, 보물, 사적 등 올바른 지정종목"],
            },
        }
    try:
        results = HeritageApiClient().get_list(
            name=query,
            designation_code=normalized_code,
            city_code=city_code(region),
            page_unit=1000 if region else limit,
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
    if region:
        terms = tuple(term.replace(" ", "") for term in region_search_terms(region))
        results = [
            item
            for item in results
            if any(
                term
                in " ".join(
                    str(item.get(key) or "") for key in ("city", "district", "address")
                ).replace(" ", "")
                for term in terms
            )
        ]
        center = region_center(region)
        if center:
            center_latitude, center_longitude, radius_km = center
            results = [
                item
                for item in results
                if item.get("latitude") is not None
                and item.get("longitude") is not None
                and haversine_km(
                    center_latitude,
                    center_longitude,
                    float(item["latitude"]),
                    float(item["longitude"]),
                )
                <= radius_km
            ]
        heritage_terms = region_heritage_terms(region)
        if heritage_terms:
            results = [
                item
                for item in results
                if any(term in str(item.get("name") or "") for term in heritage_terms)
            ]
    if period:
        try:
            candidates = results[: min(max(limit * 3, 10), 30)]
            with ThreadPoolExecutor(max_workers=min(10, len(candidates) or 1)) as pool:
                details = list(
                    pool.map(
                        lambda item: HeritageApiClient().get_detail(
                            str(item.get("heritage_id") or "")
                        ),
                        candidates,
                    )
                )
        except httpx.HTTPError:
            return {
                "success": False,
                "error": {
                    "code": "HERITAGE_API_UNAVAILABLE",
                    "message": "시대별 상세 정보를 조회하는 중 국가유산청 API 연결에 실패했습니다.",
                    "recoverable": True,
                    "required_input": [],
                },
            }
        results = [
            detail
            for detail in details
            if detail and period in str(detail.get("period") or "")
        ]
    results = [_compact_result(item) for item in results[:limit]]
    warnings = [] if results else ["조건에 맞는 국가유산을 찾지 못했습니다."]
    return {
        "success": True,
        "query": {
            "query": query,
            "region": region,
            "designation_type": normalized_type,
            "period": period,
            "limit": limit,
        },
        "data": {"results": results},
        "sources": ["국가유산청 국가유산 정보 Open API"],
        "generated_at": datetime.now(UTC).isoformat(),
        "warnings": warnings,
    }
