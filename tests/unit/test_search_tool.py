from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.tools.search import search_heritage


def test_search_requires_a_condition():
    result = search_heritage()

    assert result["success"] is False
    assert result["error"]["code"] == "SEARCH_CONDITION_REQUIRED"


def test_search_rejects_unknown_designation_type():
    result = search_heritage(designation_type="아무종목")

    assert result["success"] is False
    assert result["error"]["code"] == "UNSUPPORTED_DESIGNATION_TYPE"


def test_generic_recommendation_asks_for_context():
    result = search_heritage(query="추천")

    assert result["success"] is False
    assert result["error"]["code"] == "RECOMMENDATION_CONTEXT_REQUIRED"


def test_regional_recommendation_does_not_search_recommendation_as_name(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    result = search_heritage(query="경주 문화유산 추천")

    assert result["success"] is True
    assert result["query"]["region"] == "경주"
    assert captured["name"] is None


def test_real_heritage_name_containing_recommendation_word_is_preserved(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    search_heritage(query="추천대")

    assert captured["name"] == "추천대"


def test_region_filter_uses_address_not_heritage_name(monkeypatch):
    monkeypatch.setattr(
        HeritageApiClient,
        "get_list",
        lambda self, **kwargs: [
            {
                "name": "조선왕조실록 오대산사고본",
                "address": "서울 종로구",
                "city": "서울",
                "district": "종로구",
                "latitude": 37.57,
                "longitude": 126.98,
            },
            {
                "name": "평창 월정사 팔각 구층석탑",
                "address": "강원특별자치도 평창군",
                "city": "강원특별자치도",
                "district": "평창군",
                "latitude": 37.78,
                "longitude": 128.55,
            },
        ],
    )

    result = search_heritage(region="오대산")
    names = [item["name"] for item in result["data"]["results"]]

    assert names == ["평창 월정사 팔각 구층석탑"]
