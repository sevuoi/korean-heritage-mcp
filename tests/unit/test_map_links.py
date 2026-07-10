from kakao_heritage.utils.map_links import build_map_link


def test_build_map_link_encodes_query():
    link = build_map_link("불국사")
    assert "map.kakao.com" in link
    assert "%EB%B6%88%EA%B5%AD%EC%82%AC" in link


def test_build_map_link_prefers_coordinates():
    link = build_map_link("국립중앙박물관", 37.523, 126.98, "서울 용산구")

    assert "/link/map/" in link
    assert "37.523,126.98" in link
