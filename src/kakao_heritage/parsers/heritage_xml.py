from __future__ import annotations

from typing import Any

import xmltodict

from kakao_heritage.models.common import HeritageIdentifier, HeritageItem


def _read_first(data: dict[str, Any] | None, *keys: str) -> str | None:
    if not data:
        return None
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, str) and first.strip():
                return first.strip()
    return None


def parse_heritage_list_xml(xml_text: str) -> list[HeritageItem]:
    parsed = xmltodict.parse(xml_text)
    root = parsed.get("response") if isinstance(parsed, dict) else None
    items = root.get("item") if isinstance(root, dict) else None
    if not items:
        return []
    if isinstance(items, dict):
        items = [items]
    result: list[HeritageItem] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        identifier = HeritageIdentifier(
            designation_code=_read_first(item, "ccbaKdcd"),
            designation_type=_read_first(item, "ccbaCncl") or "",
            designation_number=int(_read_first(item, "ccbaAsno") or 0)
            if _read_first(item, "ccbaAsno")
            else None,
            city_code=_read_first(item, "ccbaCtcd"),
            heritage_id=f"{_read_first(item, 'ccbaKdcd') or ''}-{_read_first(item, 'ccbaAsno') or ''}-{_read_first(item, 'ccbaCtcd') or ''}",
        )
        result.append(
            HeritageItem(
                heritage_id=identifier.heritage_id,
                name=_read_first(item, "ccmaName", "ccceName") or "",
                designation_type=identifier.designation_type,
                designation_number=identifier.designation_number,
                former_name=_read_first(item, "ccbaMnm1"),
                period=_read_first(item, "ccbaDscr"),
                designated_date=None,
                address=_read_first(item, "ccbaLcad", "ccbaPoss"),
                city=_read_first(item, "ccbaCtcdNm"),
                district=_read_first(item, "ccbaCtcdNm3"),
                latitude=float(_read_first(item, "latitude") or 0)
                if _read_first(item, "latitude")
                else None,
                longitude=float(_read_first(item, "longitude") or 0)
                if _read_first(item, "longitude")
                else None,
                summary=_read_first(item, "ccbaDscr"),
                description=_read_first(item, "ccbaDscr"),
                source_name="국가유산청",
                raw_identifiers=identifier,
            )
        )
    return result


def parse_heritage_detail_xml(xml_text: str) -> HeritageItem | None:
    parsed = xmltodict.parse(xml_text)
    root = parsed.get("response") if isinstance(parsed, dict) else None
    item = root.get("item") if isinstance(root, dict) else None
    if not item or not isinstance(item, dict):
        return None
    identifier = HeritageIdentifier(
        designation_code=_read_first(item, "ccbaKdcd"),
        designation_type=_read_first(item, "ccbaCncl") or "",
        designation_number=int(_read_first(item, "ccbaAsno") or 0)
        if _read_first(item, "ccbaAsno")
        else None,
        city_code=_read_first(item, "ccbaCtcd"),
        heritage_id=f"{_read_first(item, 'ccbaKdcd') or ''}-{_read_first(item, 'ccbaAsno') or ''}-{_read_first(item, 'ccbaCtcd') or ''}",
    )
    return HeritageItem(
        heritage_id=identifier.heritage_id,
        name=_read_first(item, "ccmaName", "ccceName") or "",
        designation_type=identifier.designation_type,
        designation_number=identifier.designation_number,
        former_name=_read_first(item, "ccbaMnm1"),
        period=_read_first(item, "ccbaDscr"),
        designated_date=None,
        address=_read_first(item, "ccbaLcad", "ccbaPoss"),
        city=_read_first(item, "ccbaCtcdNm"),
        district=_read_first(item, "ccbaCtcdNm3"),
        latitude=float(_read_first(item, "latitude") or 0)
        if _read_first(item, "latitude")
        else None,
        longitude=float(_read_first(item, "longitude") or 0)
        if _read_first(item, "longitude")
        else None,
        summary=_read_first(item, "ccbaDscr"),
        description=_read_first(item, "ccbaDscr"),
        source_name="국가유산청",
        raw_identifiers=identifier,
    )
