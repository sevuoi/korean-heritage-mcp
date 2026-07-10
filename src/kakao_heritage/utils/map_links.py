from __future__ import annotations

from urllib.parse import quote


def build_map_link(
    name: str,
    latitude: float | None = None,
    longitude: float | None = None,
    address: str | None = None,
    base_url: str | None = None,
) -> str:
    if latitude is not None and longitude is not None:
        label = quote(name, safe="")
        return f"https://map.kakao.com/link/map/{label},{latitude},{longitude}"
    query = " ".join(part for part in (address, name) if part).strip()
    base = base_url or "https://map.kakao.com/link/search/"
    return f"{base}{quote(query)}"
