from kakao_heritage.services.distance_service import haversine_km


def test_haversine_km_returns_approximate_distance():
    seoul = (37.5665, 126.9780)
    busan = (35.1796, 129.0756)
    distance = haversine_km(seoul[0], seoul[1], busan[0], busan[1])
    assert 300 < distance < 450
