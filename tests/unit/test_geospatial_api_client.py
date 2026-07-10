import pytest
import respx

from kakao_heritage.clients.heritage_geospatial_api import HeritageGeospatialApiClient


@pytest.mark.asyncio
@respx.mock
async def test_wms_preview_builds_request_url():
    route = respx.get("https://gis-heritage.go.kr/checkKey.do").respond(
        status_code=200,
        json={"ok": True},
    )

    client = HeritageGeospatialApiClient()
    result = await client.get_wms_preview(layer="TB_MUSQ_MID")

    assert route.called
    assert result["status_code"] == 200
    assert "checkKey.do" in result["url"]
