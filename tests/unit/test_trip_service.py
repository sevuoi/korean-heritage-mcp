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
