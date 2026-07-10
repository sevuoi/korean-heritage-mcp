from __future__ import annotations

import re
from typing import Any


def parse_heritage_query(query: str) -> dict[str, Any]:
    text = (query or "").strip()
    if not text:
        return {
            "intent": "name_search",
            "designation_type": None,
            "designation_number": None,
            "region": None,
            "period": None,
            "theme": None,
        }

    if re.search(
        r"국보\s*제?\s*\d+호?|보물\s*제?\s*\d+호?|사적\s*제?\s*\d+호?|천연기념물\s*제?\s*\d+호?|국가민속문화유산\s*제?\s*\d+호?",
        text,
    ):
        match = re.search(
            r"(국보|보물|사적|천연기념물|국가민속문화유산)\s*제?\s*(\d+)\s*호?", text
        )
        designation_type = match.group(1) if match else None
        designation_number = int(match.group(2)) if match and match.group(2) else None
        return {
            "intent": "designation_lookup",
            "designation_type": designation_type,
            "designation_number": designation_number,
            "region": None,
            "period": None,
            "theme": None,
        }

    if re.search(r"현재 위치|근처|주변|내 주변", text):
        return {
            "intent": "nearby_search",
            "designation_type": None,
            "designation_number": None,
            "region": None,
            "period": None,
            "theme": None,
        }

    if re.search(r"여행|계획|코스|일정", text):
        region_match = re.search(r"([가-힣]+)\s*(?:갈 건데|여행|문화유산|유적)", text)
        region = region_match.group(1) if region_match else None
        return {
            "intent": "trip_planning",
            "designation_type": None,
            "designation_number": None,
            "region": region,
            "period": None,
            "theme": None,
        }

    if re.search(r"주차장|음식점|카페|관광시설", text):
        return {
            "intent": "facility_search",
            "designation_type": None,
            "designation_number": None,
            "region": None,
            "period": None,
            "theme": None,
        }

    if re.search(r"경주|서울|부여|공주|제주", text):
        region_match = re.search(r"([가-힣]+)", text)
        return {
            "intent": "regional_search",
            "designation_type": None,
            "designation_number": None,
            "region": region_match.group(1) if region_match else None,
            "period": None,
            "theme": None,
        }

    return {
        "intent": "name_search",
        "designation_type": None,
        "designation_number": None,
        "region": None,
        "period": None,
        "theme": None,
    }
