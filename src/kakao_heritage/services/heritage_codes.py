from __future__ import annotations

DESIGNATION_CODES = {
    "국보": "11",
    "보물": "12",
    "사적": "13",
    "명승": "15",
    "천연기념물": "16",
    "국가무형유산": "17",
    "국가민속문화유산": "18",
    "국가등록문화유산": "79",
}

CITY_CODES = {
    "서울": "11",
    "서울특별시": "11",
    "부산": "21",
    "부산광역시": "21",
    "대구": "22",
    "대구광역시": "22",
    "인천": "23",
    "인천광역시": "23",
    "광주": "24",
    "광주광역시": "24",
    "대전": "25",
    "대전광역시": "25",
    "울산": "26",
    "울산광역시": "26",
    "세종": "45",
    "세종특별자치시": "45",
    "경기": "31",
    "경기도": "31",
    "강원": "51",
    "강원특별자치도": "51",
    "충북": "33",
    "충청북도": "33",
    "충남": "34",
    "충청남도": "34",
    "전북": "35",
    "전북특별자치도": "35",
    "경북": "37",
    "경상북도": "37",
    "경남": "38",
    "경상남도": "38",
    "제주": "50",
    "제주특별자치도": "50",
    "전남": "52",
    "전라남도": "52",
}

MUNICIPALITY_PARENT_CODES = {
    "경주": "37",
    "경주시": "37",
    "부여": "34",
    "부여군": "34",
    "공주": "34",
    "공주시": "34",
}


def designation_code(value: str | None) -> str | None:
    if not value:
        return None
    return DESIGNATION_CODES.get(value.strip())


def city_code(value: str | None) -> str | None:
    if not value:
        return None
    text = value.strip()
    if text in MUNICIPALITY_PARENT_CODES:
        return MUNICIPALITY_PARENT_CODES[text]
    if text in CITY_CODES:
        return CITY_CODES[text]
    return next((code for name, code in CITY_CODES.items() if name in text), None)
