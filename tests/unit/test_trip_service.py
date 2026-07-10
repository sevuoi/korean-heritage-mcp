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
