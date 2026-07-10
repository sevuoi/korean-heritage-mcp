import httpx

from kakao_heritage.clients.kakao_local_api import (
    KakaoLocalApiClient,
    parse_kakao_place_html,
)


def test_parse_kakao_place_html_extracts_coordinates_and_address():
    page = """
    <meta name="twitter:title" content="서울역">
    <meta name="twitter:description" content="서울 중구 한강대로 405">
    <meta name="twitter:image" content="https://map.example/staticmap?m=126.9707%2C37.5540">
    """
    assert parse_kakao_place_html(page) == {
        "place_name": "서울역",
        "address_name": "서울 중구 한강대로 405",
        "x": "126.9707",
        "y": "37.5540",
    }


def test_resolve_place_url_rejects_non_kakao_url():
    def handler(request):  # pragma: no cover
        raise AssertionError(request.url)

    client = KakaoLocalApiClient(httpx.Client(transport=httpx.MockTransport(handler)))
    assert client.resolve_place_url("https://example.com/9113903") is None
