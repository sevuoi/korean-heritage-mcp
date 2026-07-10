import json
import requests
import xmltodict
import pandas as pd


def generate_map_html(df, output_html="heritage_map.html"):
    try:
        valid_df = df.copy()
        valid_df["longitude"] = pd.to_numeric(valid_df["longitude"], errors="coerce")
        valid_df["latitude"] = pd.to_numeric(valid_df["latitude"], errors="coerce")
        valid_df = valid_df.dropna(subset=["longitude", "latitude"])

        if valid_df.empty:
            print("지도에 표시할 좌표가 없습니다.")
            return

        markers = []
        for _, row in valid_df.iterrows():
            title = str(row.get("ccbaMnm1", "")).strip() or "문화유산"
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            markers.append(
                {
                    "name": title,
                    "lat": lat,
                    "lng": lon,
                    "kakao_url": f"https://map.kakao.com/link/map/{lat},{lon}",
                }
            )

        center_lat = valid_df["latitude"].mean()
        center_lng = valid_df["longitude"].mean()
        marker_data = json.dumps(markers, ensure_ascii=False)

        html = """<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"utf-8\">
  <title>문화유산 지도</title>
  <link rel=\"stylesheet\" href=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.css\" />
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; }}
    #map {{ height: 100vh; width: 100%; }}
    .leaflet-popup-content a {{ color: #2563eb; text-decoration: none; }}
  </style>
</head>
<body>
  <div id=\"map\"></div>
  <script src=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.js\"></script>
  <script>
    const markers = {marker_data};
    const map = L.map('map').setView([{center_lat}, {center_lng}], 12);

    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);

    markers.forEach((item) => {{
      const marker = L.marker([item.lat, item.lng]).addTo(map);
      marker.bindPopup(`
        <b>${{item.name}}</b><br>
        위도: ${{item.lat}}<br>
        경도: ${{item.lng}}<br>
        <a href=\"${{item.kakao_url}}\" target=\"_blank\">카카오맵에서 열기</a>
      `);
    }});
  </script>
</body>
</html>
""".format(marker_data=marker_data, center_lat=center_lat, center_lng=center_lng)

        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"지도 파일 생성: {output_html}")
    except Exception as e:
        print(f"지도 생성 오류: {e}")


def fetch_heritage_data(
    url, output_filename="heritage_list.csv", output_html="heritage_map.html"
):
    try:
        # 1. API 호출
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        # 2. XML 데이터를 딕셔너리로 변환
        data_dict = xmltodict.parse(response.content)

        # 3. 데이터 리스트 추출
        items = data_dict.get("result", {}).get("item", [])

        if not items:
            print("데이터를 찾을 수 없습니다.")
            return

        # 4. 데이터프레임 변환
        df = pd.DataFrame(items)

        # 5. CSV 파일로 저장
        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"성공: {output_filename} 파일이 저장되었습니다.")

        # 6. 지도 HTML 생성
        generate_map_html(df, output_html)

        # 7. 주요 컬럼 결과 출력
        print("\n[가져온 데이터 미리보기]")
        print(df[["sn", "ccbaMnm1", "longitude", "latitude"]].head())

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    api_url = "http://www.khs.go.kr/cha/SearchKindOpenapiList.do?pageUnit=20&ccbaCncl=N&ccbaKdcd=11&ccbaCtcd=11"
    fetch_heritage_data(api_url)
