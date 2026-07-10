import pytest

from kakao_heritage.parsers.natural_query import parse_heritage_query


@pytest.mark.parametrize(
    ("query", "expected_intent", "expected_type", "expected_number", "expected_region"),
    [
        ("국보 10호", "designation_lookup", "국보", 10, None),
        ("국보 제10호에 대해 알려줘", "designation_lookup", "국보", 10, None),
        ("국보10호", "designation_lookup", "국보", 10, None),
        ("보물 1호 위치", "designation_lookup", "보물", 1, None),
        ("경주 갈 건데 문화유산 여행정보", "trip_planning", None, None, "경주"),
        ("지금 있는 곳 근처 문화유산", "nearby_search", None, None, None),
    ],
)
def test_parse_heritage_query(
    query, expected_intent, expected_type, expected_number, expected_region
):
    result = parse_heritage_query(query)
    assert result["intent"] == expected_intent
    assert result["designation_type"] == expected_type
    assert result["designation_number"] == expected_number
    assert result["region"] == expected_region


def test_trip_query_extracts_region_period_and_theme():
    result = parse_heritage_query(
        "서울에서 조선 시대 궁궐을 둘러보는 하루 여행 코스를 만들어줘"
    )

    assert result["intent"] == "trip_planning"
    assert result["region"] == "서울"
    assert result["period"] == "조선"
    assert result["theme"] == "궁궐"
