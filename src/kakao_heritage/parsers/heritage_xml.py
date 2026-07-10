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


def _root(parsed: Any) -> dict[str, Any] | None:
    if not isinstance(parsed, dict):
        return None
    root = parsed.get("result") or parsed.get("response")
    return root if isinstance(root, dict) else None


def _float_or_none(value: str | None) -> float | None:
    if not value:
        return None
    number = float(value)
    return number if number else None


def _designation_number(management_number: str | None) -> int | None:
    if not management_number:
        return None
    digits = "".join(
        character for character in management_number if character.isdigit()
    )
    if not digits:
        return None
    # The official API uses a 13-digit management number. Its first six digits
    # are the public designation number (for example 0000240000000 -> 24).
    return int(digits[:6] if len(digits) >= 13 else digits)


def _identifier(data: dict[str, Any]) -> HeritageIdentifier:
    designation_code = _read_first(data, "ccbaKdcd")
    management_number = _read_first(data, "ccbaAsno")
    city_code = _read_first(data, "ccbaCtcd")
    heritage_id = "-".join(
        (designation_code or "", management_number or "", city_code or "")
    )
    return HeritageIdentifier(
        designation_code=designation_code,
        designation_type=_read_first(data, "ccmaName", "ccbaCncl") or "",
        designation_number=_designation_number(management_number),
        management_number=management_number,
        city_code=city_code,
        heritage_id=heritage_id,
    )


def parse_heritage_list_xml(xml_text: str) -> list[HeritageItem]:
    root = _root(xmltodict.parse(xml_text))
    items = root.get("item") if root else None
    if not items:
        return []
    if isinstance(items, dict):
        items = [items]

    result: list[HeritageItem] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        identifier = _identifier(item)
        city = _read_first(item, "ccbaCtcdNm")
        district = _read_first(item, "ccsiName", "ccbaCtcdNm3")
        address = " ".join(part for part in (city, district) if part) or None
        result.append(
            HeritageItem(
                heritage_id=identifier.heritage_id,
                name=_read_first(item, "ccbaMnm1", "ccceName") or "",
                designation_type=identifier.designation_type,
                designation_number=identifier.designation_number,
                former_name=_read_first(item, "ccbaMnm2"),
                address=address,
                city=city,
                district=district,
                manager=_read_first(item, "ccbaAdmin"),
                latitude=_float_or_none(_read_first(item, "latitude")),
                longitude=_float_or_none(_read_first(item, "longitude")),
                source_name="국가유산청",
                raw_identifiers=identifier,
            )
        )
    return result


def parse_heritage_detail_xml(xml_text: str) -> HeritageItem | None:
    root = _root(xmltodict.parse(xml_text))
    if not root:
        return None
    item = root.get("item")
    if not isinstance(item, dict):
        return None

    # Identifiers and coordinates are root-level in the official detail XML.
    combined = {**item, **{key: value for key, value in root.items() if key != "item"}}
    identifier = _identifier(combined)
    return HeritageItem(
        heritage_id=identifier.heritage_id,
        name=_read_first(item, "ccbaMnm1", "ccceName") or "",
        designation_type=_read_first(item, "ccmaName") or identifier.designation_type,
        designation_number=identifier.designation_number,
        former_name=_read_first(item, "ccbaMnm2"),
        period=_read_first(item, "ccceName"),
        designated_date=_read_first(item, "ccbaAsdt"),
        address=_read_first(item, "ccbaLcad"),
        city=_read_first(item, "ccbaCtcdNm"),
        district=_read_first(item, "ccsiName"),
        owner=_read_first(item, "ccbaPoss"),
        manager=_read_first(item, "ccbaAdmin"),
        latitude=_float_or_none(_read_first(root, "latitude")),
        longitude=_float_or_none(_read_first(root, "longitude")),
        summary=_read_first(item, "content"),
        description=_read_first(item, "content"),
        image_url=_read_first(item, "imageUrl"),
        source_name="국가유산청",
        raw_identifiers=identifier,
    )
