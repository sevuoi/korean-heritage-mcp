# Deployment

Use the streamable HTTP transport for PlayMCP deployment.

PlayMCP builds the root `Dockerfile`. The container listens on `0.0.0.0`, uses
the platform-provided `PORT` (falling back to 8000), and exposes MCP at `/mcp`.

```bash
MCP_TRANSPORT=streamable-http python3 -m kakao_heritage
```
