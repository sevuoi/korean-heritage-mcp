# K-Heritage Guide MCP

K-Heritage Guide(한국유산길잡이) is a remote MCP server for discovering Korean
national heritage, resolving designation numbers, and creating heritage-focused
trip plans. Official National Heritage Administration data is the primary source;
Kakao Local is used only as optional location context.

## Quick start

```bash
cd korean-heritage-mcp
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m kakao_heritage
```

## Features

- Search nearby heritage sites by coordinates or place names
- Look up heritage by designation type and number
- Generate simple trip plans for regions like Gyeongju and Seoul
- Use official heritage data as the primary source and Kakao Local as a supplementary source
- Parse National Heritage Administration XML responses for heritage place information

## PlayMCP compatibility

- Streamable HTTP endpoint at `/mcp`
- Eight read-only, non-destructive, idempotent tools
- Explicit PlayMCP tool annotations and English tool descriptions
- Tool and server names do not include reserved platform branding
