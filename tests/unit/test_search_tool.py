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


def test_visit_information_query_searches_only_heritage_name(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return [{"name": "창덕궁", "address": "서울 종로구"}]

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    result = search_heritage(query="창덕궁 개방시간, 입장료, 휴무일")

    assert captured["name"] == "창덕궁"
    assert result["success"] is True
    assert result["data"]["requested_visit_information"] == [
        "개방시간",
        "입장료",
        "휴무일",
    ]
    assert result["data"]["visit_information_status"] == (
        "official_live_confirmation_required"
    )
    assert "추측하지 말고" in result["warnings"][0]


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


def test_theme_sentence_query_searches_theme_term(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    result = search_heritage(query="서울 궁궐 무료 관람")

    assert result["success"] is True
    assert result["query"]["region"] == "서울"
    assert captured["name"] == "궁"


def test_theme_query_with_heritage_name_keeps_original_query(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    search_heritage(query="경복궁 궁궐")

    assert captured["name"] == "경복궁 궁궐"


def test_designation_sentence_query_filters_by_designation(monkeypatch):
    captured = {}

    def fake_list(self, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    result = search_heritage(query="부여 백제 시대 사적")

    assert result["success"] is True
    assert result["query"]["region"] == "부여"
    assert captured["name"] is None
    assert captured["designation_code"] is not None


def test_visit_info_for_unknown_heritage_fails_existence_check(monkeypatch):
    def fake_list(self, **kwargs):
        return []

    monkeypatch.setattr(HeritageApiClient, "get_list", fake_list)

    result = search_heritage(query="행복사 운영시간")

    assert result["success"] is False
    assert result["error"]["code"] == "HERITAGE_NOT_FOUND"
    assert "행복사" in result["error"]["message"]
