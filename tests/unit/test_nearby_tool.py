from kakao_heritage.clients.heritage_api import HeritageApiClient
from kakao_heritage.clients.kakao_local_api import KakaoLocalApiClient
from kakao_heritage.config import settings
from kakao_heritage.tools.nearby import find_nearby_heritage


def test_nearby_uses_map_coordinates_without_kakao_key(monkeypatch):
    monkeypatch.setattr(settings, "kakao_rest_api_key", None)
    monkeypatch.setattr(
        HeritageApiClient,
        "get_list",
        lambda self, **kwargs: [
            {
                "name": "서울 숭례문",
                "designation_type": "국보",
                "latitude": 37.559975,
                "longitude": 126.975313,
            }
        ],
    )

    result = find_nearby_heritage(
        latitude=37.5663,
        longitude=126.9779,
        location="서울시청",
        region="서울",
        radius_km=10,
    )

    assert result["success"] is True
    assert result["data"]["search_mode"] == "distance"
    assert result["data"]["results"][0]["heritage"]["name"] == "서울 숭례문"


def test_nearby_returns_explicit_map_context_error(monkeypatch):
    monkeypatch.setattr(settings, "kakao_rest_api_key", None)

    result = find_nearby_heritage(location="연희동")

    assert result["success"] is False
    assert result["error"]["code"] == "MAP_CONTEXT_REQUIRED"


def test_nearby_does_not_present_region_results_as_radius_results(monkeypatch):
    monkeypatch.setattr(settings, "kakao_rest_api_key", None)
    monkeypatch.setattr(
        HeritageApiClient,
        "get_list",
        lambda self, **kwargs: [{"name": "서울 숭례문"}],
    )

    result = find_nearby_heritage(location="서울역", region="서울", radius_km=5)

    assert result["success"] is False
    assert result["error"]["code"] == "MAP_COORDINATES_REQUIRED"


def test_nearby_accepts_kakao_map_place_url(monkeypatch):
    monkeypatch.setattr(settings, "kakao_rest_api_key", None)
    monkeypatch.setattr(
        KakaoLocalApiClient,
        "resolve_place_url",
        lambda self, url: {
            "place_name": "서울역",
            "address_name": "서울 중구 한강대로 405",
            "x": "126.9707",
            "y": "37.5540",
        },
    )
    monkeypatch.setattr(
        HeritageApiClient,
        "get_list",
        lambda self, **kwargs: [
            {
                "name": "서울 숭례문",
                "latitude": 37.559975,
                "longitude": 126.975313,
            }
        ],
    )
    result = find_nearby_heritage(
        location="서울역",
        map_place_url="http://place.map.kakao.com/9113903",
        radius_km=5,
    )
    assert result["success"] is True
    assert result["query"]["latitude"] == 37.554
    assert "카카오맵 공개 장소 페이지" in result["sources"]
