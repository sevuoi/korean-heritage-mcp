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

The public MCP surface delegates place resolution, directions, and facility
search to a map tool. Nearby heritage accepts latitude, longitude, and region
context from that tool, so a Kakao key is not required. `KAKAO_REST_API_KEY` is
only an optional server-side fallback for direct place-name resolution and must
never be committed to Git.
