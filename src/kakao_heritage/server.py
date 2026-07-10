from __future__ import annotations

from fastmcp import FastMCP

from kakao_heritage.config import settings
from kakao_heritage.tools.designation import find_heritage_by_designation
from kakao_heritage.tools.detail import get_heritage_detail
from kakao_heritage.tools.nearby import find_nearby_heritage
from kakao_heritage.tools.query_parser import parse_heritage_query_tool
from kakao_heritage.tools.search import search_heritage
from kakao_heritage.tools.trip import plan_heritage_trip

mcp = FastMCP(
    "K-Heritage Guide",
    instructions=(
        "K-Heritage Guide(한국유산길잡이) discovers Korean national heritage, "
        "provides designation details, and creates heritage-focused trip plans."
    ),
)


def _read_only_annotations(
    title: str, *, open_world: bool = True
) -> dict[str, bool | str]:
    return {
        "title": title,
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": open_world,
        "idempotentHint": True,
    }


@mcp.tool(
    title="Find nearby Korean heritage",
    description=(
        "Finds national heritage sites with K-Heritage Guide(한국유산길잡이). "
        "For exact distance ordering, first use a map tool to resolve the place, "
        "then pass latitude, longitude, and region. If only a region is available, "
        "returns a regional fallback without claiming exact distances."
    ),
    annotations=_read_only_annotations("Find nearby Korean heritage"),
)
def find_nearby_heritage_tool(
    latitude: float | None = None,
    longitude: float | None = None,
    location: str | None = None,
    region: str | None = None,
    radius_km: float = 10.0,
    designation_types: list[str] | None = None,
    period: str | None = None,
    limit: int = 10,
) -> dict:
    """지도 도구가 확인한 좌표와 지역을 기준으로 주변 국가유산을 찾습니다.

    언제 사용하는지: 현재 위치 주변 문화유산 검색이 필요할 때.
    언제 사용하지 않는지: 정확한 지정번호 검색이나 여행계획 생성이 필요할 때.
    필수 입력: latitude/longitude 또는 region 중 하나.
    선택 입력: location, radius_km, designation_types, period, limit.
    반환 내용: 기준 위치, 검색 반경, 거리순 문화유산 목록, 카카오맵 링크, 출처.
    오류 상황: 좌표가 불완전하거나 위치가 비어 있으면 LOCATION_REQUIRED를 반환합니다.
    """
    return find_nearby_heritage(
        latitude,
        longitude,
        location,
        region,
        radius_km,
        designation_types,
        period,
        limit,
    )


@mcp.tool(
    title="Search Korean heritage",
    description=(
        "Searches Korean national heritage by name, region, period, designation, "
        "or theme with K-Heritage Guide(한국유산길잡이)."
    ),
    annotations=_read_only_annotations("Search Korean heritage"),
)
def search_heritage_tool(
    query: str | None = None,
    region: str | None = None,
    designation_type: str | None = None,
    period: str | None = None,
    limit: int = 10,
) -> dict:
    """이름, 지역, 시대, 종목, 주제로 문화유산을 검색합니다. 경주 신라 문화유산, 서울 조선 궁궐, 불교 문화유산 같은 요청에 사용합니다.

    언제 사용하는지: 일반적인 문화유산 이름/지역/주제 검색이 필요할 때.
    언제 사용하지 않는지: 지정번호로 정확히 찾을 때.
    필수 입력: query 또는 region 중 하나.
    선택 입력: designation_type, period, limit.
    반환 내용: 검색 결과 목록과 요약.
    오류 상황: 입력이 모두 없으면 빈 결과 구조를 반환합니다.
    """
    return search_heritage(query, region, designation_type, period, limit)


@mcp.tool(
    title="Find heritage by designation",
    description=(
        "Finds an exact Korean national heritage record by designation type and "
        "number with K-Heritage Guide(한국유산길잡이)."
    ),
    annotations=_read_only_annotations("Find heritage by designation"),
)
def find_heritage_by_designation_tool(
    designation_type: str, designation_number: int
) -> dict:
    """국보 10호, 보물 1호, 사적 제35호처럼 지정 종목과 번호로 정확히 검색합니다.

    언제 사용하는지: 지정번호 기반 조회가 필요할 때.
    언제 사용하지 않는지: 일반 텍스트 검색이나 주변 검색이 필요할 때.
    필수 입력: designation_type, designation_number.
    선택 입력: 없음.
    반환 내용: 공식 명칭, 종목, 지정번호, 주소, 좌표, 설명.
    오류 상황: 결과가 없으면 NOT_FOUND를 반환합니다.
    """
    return find_heritage_by_designation(designation_type, designation_number)


@mcp.tool(
    title="Get Korean heritage details",
    description=(
        "Retrieves detailed information for a Korean national heritage item with "
        "K-Heritage Guide(한국유산길잡이)."
    ),
    annotations=_read_only_annotations("Get Korean heritage details"),
)
def get_heritage_detail_tool(
    name: str | None = None,
    heritage_id: str | None = None,
    designation_type: str | None = None,
    designation_number: int | None = None,
) -> dict:
    """특정 문화유산의 상세 정보를 조회합니다. 이름, heritage_id, 지정번호 중 하나로 조회할 수 있습니다.

    언제 사용하는지: 특정 문화유산의 상세 정보를 보고 싶을 때.
    언제 사용하지 않는지: 주변 검색이나 여행 계획 생성이 필요할 때.
    필수 입력: name, heritage_id, designation_type/number 중 하나.
    선택 입력: 나머지 식별 정보.
    반환 내용: 상세 정보와 출처.
    오류 상황: 식별자가 없으면 빈 결과 구조를 반환합니다.
    """
    return get_heritage_detail(name, heritage_id, designation_type, designation_number)


@mcp.tool(
    title="Plan a Korean heritage trip",
    description=(
        "Creates a region-based Korean heritage itinerary with K-Heritage "
        "Guide(한국유산길잡이). For a different itinerary, increment plan_variant "
        "or pass previous visit places in exclude_places."
    ),
    annotations=_read_only_annotations("Plan a Korean heritage trip"),
)
def plan_heritage_trip_tool(
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
    exclude_places: list[str] | None = None,
    plan_variant: int = 1,
) -> dict:
    """특정 지역의 문화유산 정보와 여행 일정을 함께 작성합니다. 경주, 서울, 부여 같은 지역 입력에 사용합니다.

    언제 사용하는지: 지역별 문화유산 여행 계획이 필요할 때.
    언제 사용하지 않는지: 단순 검색만 필요할 때.
    필수 입력: region.
    선택 입력: start_location, days, transport, themes, companions, pace, include_food, include_parking, max_places_per_day, exclude_places, plan_variant.
    반환 내용: 지역 개요, 추천 유산, 하루별 일정, 주차/음식 정보, 확인 필요 사항.
    오류 상황: 지역명이 비어 있으면 빈 결과 구조를 반환합니다.
    """
    return plan_heritage_trip(
        region,
        start_location,
        days,
        transport,
        themes,
        companions,
        pace,
        include_food,
        include_parking,
        max_places_per_day,
        exclude_places,
        plan_variant,
    )


@mcp.tool(
    title="Parse a heritage request",
    description=(
        "Parses a Korean natural-language heritage request into structured intent "
        "and parameters for K-Heritage Guide(한국유산길잡이)."
    ),
    annotations=_read_only_annotations("Parse a heritage request", open_world=False),
)
def parse_heritage_query_tool_wrapper(query: str) -> dict:
    """자연어 문화유산 요청을 구조화합니다. PlayMCP 호출 정확도 향상과 디버깅에 사용합니다.

    언제 사용하는지: 사용자의 자연어 요청을 구조화하고 싶을 때.
    언제 사용하지 않는지: 이미 구조화된 입력이 있는 경우.
    필수 입력: query.
    선택 입력: 없음.
    반환 내용: 의도와 파라미터.
    오류 상황: 텍스트가 비면 기본 name_search를 반환합니다.
    """
    return parse_heritage_query_tool(query)


def main(transport: str | None = None) -> None:
    chosen_transport = transport or settings.mcp_transport
    if chosen_transport == "streamable-http":
        mcp.run(
            transport="streamable-http",
            host=settings.mcp_host,
            port=settings.mcp_port,
            path=settings.mcp_path,
        )
    else:
        mcp.run(transport="stdio")
