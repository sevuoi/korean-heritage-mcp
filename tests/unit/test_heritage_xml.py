from kakao_heritage.parsers.heritage_xml import (
    parse_heritage_detail_xml,
    parse_heritage_list_xml,
)


def test_official_list_structure_and_management_number():
    xml = """<result><item>
      <ccmaName>국보</ccmaName><ccbaMnm1>경주 석굴암 석굴</ccbaMnm1>
      <ccbaKdcd>11</ccbaKdcd><ccbaAsno>0000240000000</ccbaAsno>
      <ccbaCtcd>37</ccbaCtcd><ccbaCtcdNm>경상북도</ccbaCtcdNm>
      <ccsiName>경주시</ccsiName><longitude>129.349242</longitude>
      <latitude>35.794852</latitude>
    </item></result>"""

    item = parse_heritage_list_xml(xml)[0]

    assert item.name == "경주 석굴암 석굴"
    assert item.designation_type == "국보"
    assert item.designation_number == 24
    assert item.heritage_id == "11-0000240000000-37"


def test_official_detail_structure_uses_root_identifiers():
    xml = """<result>
      <ccbaKdcd>11</ccbaKdcd><ccbaAsno>0000240000000</ccbaAsno>
      <ccbaCtcd>37</ccbaCtcd><longitude>129.349242</longitude>
      <latitude>35.794852</latitude><item><ccmaName>국보</ccmaName>
      <ccbaMnm1>경주 석굴암 석굴</ccbaMnm1><ccceName>통일신라시대</ccceName>
      <ccbaLcad>경상북도 경주시</ccbaLcad><content>석굴암 설명</content>
      </item></result>"""

    item = parse_heritage_detail_xml(xml)

    assert item is not None
    assert item.designation_number == 24
    assert item.period == "통일신라시대"
    assert item.description == "석굴암 설명"
