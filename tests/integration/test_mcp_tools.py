from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient
from kakao_heritage.config import settings
from kakao_heritage.tools.designation import find_heritage_by_designation
from kakao_heritage.tools.detail import get_heritage_detail
from kakao_heritage.tools.facilities import find_heritage_facilities
from kakao_heritage.tools.location import resolve_location
from kakao_heritage.tools.nearby import find_nearby_heritage
from kakao_heritage.tools.query_parser import parse_heritage_query_tool
from kakao_heritage.tools.search import search_heritage
from kakao_heritage.tools.trip import plan_heritage_trip


HERITAGE = {
    "heritage_id": "11-0000240000000-37",
    "name": "경주 석굴암 석굴",
    "designation_type": "국보",
    "designation_number": 24,
    "address": "경상북도 경주시",
    "city": "경상북도",
    "district": "경주시",
    "latitude": 35.794852,
    "longitude": 129.349242,
    "description": "통일신라의 석굴 사원",
}


def test_all_tools_return_common_structure(monkeypatch):
    monkeypatch.setattr(settings, "kakao_rest_api_key", "test-key")
    monkeypatch.setattr(
        HeritageApiClient,
        "get_list",
        lambda self, **kwargs: [HERITAGE],
    )
    monkeypatch.setattr(
        HeritageApiClient,
        "find_by_designation",
        lambda self, code, number: HERITAGE if number == 24 else None,
    )
    monkeypatch.setattr(
        HeritageApiClient, "get_detail", lambda self, heritage_id: HERITAGE
    )
    monkeypatch.setattr(HeritageApiClient, "search_first", lambda self, name: HERITAGE)
    monkeypatch.setattr(
        KakaoLocalApiClient,
        "geocode",
        lambda self, query: {
            "place_name": query,
            "address_name": "서울특별시 중구",
            "x": "126.978",
            "y": "37.5665",
        },
    )
    monkeypatch.setattr(
        KakaoLocalApiClient,
        "region_from_coordinates",
        lambda self, longitude, latitude: {"region_1depth_name": "서울특별시"},
    )
    monkeypatch.setattr(
        KakaoLocalApiClient,
        "search_keyword",
        lambda self, query, **kwargs: [
            {
                "place_name": f"테스트 {query}",
                "category_name": query,
                "address_name": "경상북도 경주시",
                "x": "129.35",
                "y": "35.79",
                "distance": "100",
            }
        ],
    )

    nearby = find_nearby_heritage(
        latitude=35.79, longitude=129.35, location="석굴암", radius_km=5
    )
    assert nearby["success"] is True

    designation = find_heritage_by_designation("국보", 24)
    assert designation["success"] is True

    detail = get_heritage_detail(name="석굴암")
    assert detail["success"] is True

    trip = plan_heritage_trip(region="경주")
    assert trip["success"] is True

    facilities = find_heritage_facilities("석굴암")
    assert facilities["success"] is True

    location = resolve_location("서울역")
    assert location["success"] is True
    assert location["data"]["location"]["latitude"] == 37.5665

    query = parse_heritage_query_tool("국보 24호")
    assert query["success"] is True

    search = search_heritage(query="석굴암")
    assert search["success"] is True
