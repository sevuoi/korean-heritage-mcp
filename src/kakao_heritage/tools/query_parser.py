from __future__ import annotations

from typing import Any

from kakao_heritage.parsers.natural_query import parse_heritage_query


def parse_heritage_query_tool(query: str) -> dict[str, Any]:
    return {"success": True, "data": parse_heritage_query(query)}
