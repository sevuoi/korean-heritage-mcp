from __future__ import annotations

from typing import Any

import httpx


class HeritageGeospatialApiClient:
    """Client for the National Heritage geospatial Open API.

    The service provides WMS/WFS endpoints for heritage spatial information.
    The documentation at https://gis-heritage.go.kr/helpAPI.do is used as the basis.
    """

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=15)

    async def get_wms_preview(self, layer: str = "TB_MUSQ_MID") -> dict[str, Any]:
        url = "https://gis-heritage.go.kr/checkKey.do"
        params = {
            "domain": "https://gis-heritage.go.kr/",
            "service": "WMS",
            "version": "1.3.0",
            "request": "GetMap",
            "LAYERS": layer,
            "styles": "default",
            "bbox": "950651.45841435,1950576.2559198,956462.06276295,1953030.7695818",
            "width": "781",
            "height": "541",
            "format": "image/png",
            "crs": "EPSG:9020203",
            "exceptions": "INIMAGE",
        }
        async with self._client as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return {"url": str(response.url), "status_code": response.status_code}
