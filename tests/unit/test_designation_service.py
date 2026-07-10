from kakao_heritage.services.designation_service import normalize_designation_type


def test_normalize_designation_type():
    assert normalize_designation_type("국보") == "국보"
    assert normalize_designation_type("국가민속문화재") == "국가민속문화유산"
    assert normalize_designation_type("문화재") == "문화재"
