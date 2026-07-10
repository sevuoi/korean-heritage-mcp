# API Sources

- National Heritage Administration: official heritage metadata and designation information
- National Heritage Administration heritage place data is provided as XML, and the project parses it with xmltodict
- Kakao Local API: supplementary location, address, coordinate, and facility lookup
- Official heritage information is treated as primary; Kakao results are used only for supplementary context

## National Heritage Administration XML API

- List: `https://www.khs.go.kr/cha/SearchKindOpenapiList.do`
- Detail: `https://www.khs.go.kr/cha/SearchKindOpenapiDt.do`
- Active records are requested with `ccbaCncl=N`
- Detail identifiers: `ccbaKdcd`, `ccbaAsno`, `ccbaCtcd`

## Kakao Local API

Set `KAKAO_REST_API_KEY` in the PlayMCP server environment. It is required for
place resolution, coordinate-to-region lookup, nearby heritage, and facility
search. The key is a server secret and must not be committed to Git.
