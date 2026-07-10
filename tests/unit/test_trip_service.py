from kakao_heritage.services.trip_service import create_trip_plan


def test_trip_plan_respects_limits_and_deduplicates():
    heritage_items = [
        {
            "name": "불국사",
            "address": "경북 경주시",
            "latitude": 35.79,
            "longitude": 129.33,
            "designation_type": "사찰",
        },
        {
            "name": "석굴암",
            "address": "경북 경주시",
            "latitude": 35.80,
            "longitude": 129.33,
            "designation_type": "사찰",
        },
        {
            "name": "불국사",
            "address": "경북 경주시",
            "latitude": 35.79,
            "longitude": 129.33,
            "designation_type": "사찰",
        },
    ]
    plan = create_trip_plan(
        region="경주",
        start_location="경주",
        heritage_items=heritage_items,
        days=1,
        max_places_per_day=2,
    )
    assert plan["days"] == 1
    assert len(plan["itinerary"][0]["stops"]) <= 2
    assert (
        len({stop["heritage"]["name"] for stop in plan["itinerary"][0]["stops"]}) == 2
    )


def test_trip_plan_groups_museum_objects_as_one_visit():
    items = [
        {
            "name": "청자 사자형뚜껑 향로",
            "manager": "국립중앙박물관",
            "address": "서울 용산구",
            "latitude": 37.523,
            "longitude": 126.98,
        },
        {
            "name": "청자 어룡형 주전자",
            "manager": "국립중앙박물관",
            "address": "서울 용산구",
            "latitude": 37.523,
            "longitude": 126.98,
        },
    ]

    plan = create_trip_plan(region="서울", heritage_items=items)
    stop = plan["itinerary"][0]["stops"][0]

    assert len(plan["itinerary"][0]["stops"]) == 1
    assert stop["visit_place"] == "국립중앙박물관"
    assert stop["featured_heritage"] == [
        "청자 사자형뚜껑 향로",
        "청자 어룡형 주전자",
    ]
    assert "/link/map/" in stop["map_url"]


def test_trip_plan_supports_alternative_and_excluded_places():
    items = [
        {
            "name": f"문화유산 {index}",
            "latitude": 35.0 + index / 100,
            "longitude": 129.0,
        }
        for index in range(1, 7)
    ]

    first = create_trip_plan(
        region="경주", heritage_items=items, max_places_per_day=2, plan_variant=1
    )
    second = create_trip_plan(
        region="경주", heritage_items=items, max_places_per_day=2, plan_variant=2
    )
    excluded = create_trip_plan(
        region="경주",
        heritage_items=items,
        max_places_per_day=2,
        exclude_places=["문화유산 1"],
    )

    first_names = [stop["visit_place"] for stop in first["itinerary"][0]["stops"]]
    second_names = [stop["visit_place"] for stop in second["itinerary"][0]["stops"]]
    excluded_names = [stop["visit_place"] for stop in excluded["itinerary"][0]["stops"]]
    assert first_names != second_names
    assert "문화유산 1" not in excluded_names
    assert all(
        stop["travel_minutes_from_previous"] is None
        for stop in first["itinerary"][0]["stops"]
    )


def test_trip_plan_merges_same_visit_place_with_different_coordinates():
    items = [
        {
            "name": "평창 월정사 팔각 구층석탑",
            "manager": "월정사",
            "latitude": 37.78,
            "longitude": 128.55,
        },
        {
            "name": "평창 월정사 석조보살좌상",
            "manager": "월정사",
            "latitude": 37.79,
            "longitude": 128.56,
        },
    ]

    plan = create_trip_plan(region="오대산", heritage_items=items)
    stops = plan["itinerary"][0]["stops"]

    assert len(stops) == 1
    assert stops[0]["visit_place"] == "월정사"
    assert len(stops[0]["featured_heritage"]) == 2
