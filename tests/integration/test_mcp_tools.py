from kakao_heritage.tools.designation import find_heritage_by_designation
from kakao_heritage.tools.detail import get_heritage_detail
from kakao_heritage.tools.facilities import find_heritage_facilities
from kakao_heritage.tools.location import resolve_location
from kakao_heritage.tools.nearby import find_nearby_heritage
from kakao_heritage.tools.query_parser import parse_heritage_query_tool
from kakao_heritage.tools.search import search_heritage
from kakao_heritage.tools.trip import plan_heritage_trip


def test_all_tools_return_common_structure():
    nearby = find_nearby_heritage(
        latitude=37.56, longitude=126.97, location="서울역", radius_km=5
    )
    assert nearby["success"] is True

    designation = find_heritage_by_designation("국보", 10)
    assert designation["success"] is True

    detail = get_heritage_detail(name="불국사")
    assert detail["success"] is True

    trip = plan_heritage_trip(region="경주")
    assert trip["success"] is True

    facilities = find_heritage_facilities("불국사")
    assert facilities["success"] is True

    location = resolve_location("서울역")
    assert location["success"] is True

    query = parse_heritage_query_tool("국보 10호")
    assert query["success"] is True

    search = search_heritage(query="경주")
    assert search["success"] is True
