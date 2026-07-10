from kakao_heritage.tools.search import search_heritage


def test_search_requires_a_condition():
    result = search_heritage()

    assert result["success"] is False
    assert result["error"]["code"] == "SEARCH_CONDITION_REQUIRED"


def test_search_rejects_unknown_designation_type():
    result = search_heritage(designation_type="아무종목")

    assert result["success"] is False
    assert result["error"]["code"] == "UNSUPPORTED_DESIGNATION_TYPE"
