import pytest

from kakao_heritage.server import mcp


@pytest.mark.asyncio
async def test_all_tools_include_playmcp_metadata():
    tools = await mcp.list_tools()

    assert len(tools) == 6
    assert {tool.name for tool in tools}.isdisjoint(
        {"resolve_location_tool", "find_heritage_facilities_tool"}
    )
    trip_tool = next(tool for tool in tools if tool.name == "plan_heritage_trip_tool")
    assert "exclude_places" in trip_tool.parameters["properties"]
    assert "plan_variant" in trip_tool.parameters["properties"]
    for tool in tools:
        assert "kakao" not in tool.name.lower()
        assert tool.title
        assert tool.description
        assert "K-Heritage Guide(한국유산길잡이)" in tool.description
        assert tool.annotations is not None
        assert tool.annotations.title
        assert tool.annotations.readOnlyHint is True
        assert tool.annotations.destructiveHint is False
        assert tool.annotations.openWorldHint is not None
        assert tool.annotations.idempotentHint is True
