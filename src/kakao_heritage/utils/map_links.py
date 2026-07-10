from __future__ import annotations

from urllib.parse import quote


def build_map_link(query: str, base_url: str | None = None) -> str:
    base = base_url or "https://map.kakao.com/link/search/"
    return f"{base}{quote(query)}"
