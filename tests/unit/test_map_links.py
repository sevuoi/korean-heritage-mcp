from kakao_heritage.utils.map_links import build_map_link


def test_build_map_link_encodes_query():
    link = build_map_link("불국사")
    assert "map.kakao.com" in link
    assert "%EB%B6%88%EA%B5%AD%EC%82%AC" in link
