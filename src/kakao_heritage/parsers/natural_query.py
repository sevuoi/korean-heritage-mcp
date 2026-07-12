from __future__ import annotations

import re
from typing import Any

REGIONS = (
    "서울",
    "부산",
    "대구",
    "인천",
    "광주",
    "대전",
    "울산",
    "세종",
    "경기",
    "강원",
    "충북",
    "충남",
    "전북",
    "전남",
    "경북",
    "경남",
    "제주",
    "경주",
    "부여",
    "공주",
)
PERIODS = ("선사", "삼국", "고구려", "백제", "신라", "통일신라", "고려", "조선", "근대")
DESIGNATION_TYPES = (
    "국보",
    "보물",
    "사적",
    "명승",
    "천연기념물",
    "국가민속문화유산",
    "국가무형유산",
)


def _first_match(text: str, values: tuple[str, ...]) -> str | None:
    return next((value for value in values if value in text), None)


def _base(intent: str, text: str) -> dict[str, Any]:
    theme = next(
        (
            value
            for value in ("궁궐", "불교", "성곽", "왕릉", "서원", "사찰")
            if value in text
        ),
        None,
    )
    # "역사적인 장소"의 '사적' 오탐 방지
    designation_text = text.replace("역사적", "")
    return {
        "intent": intent,
        "designation_type": _first_match(designation_text, DESIGNATION_TYPES),
        "designation_number": None,
        "region": _first_match(text, REGIONS),
        "period": _first_match(text, PERIODS),
        "theme": theme,
    }


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
        return _base("nearby_search", text)

    if re.search(r"여행|계획|코스|일정", text):
        return _base("trip_planning", text)

    if re.search(r"주차장|음식점|카페|관광시설", text):
        return _base("facility_search", text)

    if _first_match(text, REGIONS):
        return _base("regional_search", text)

    return _base("name_search", text)
