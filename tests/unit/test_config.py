from kakao_heritage.config import Settings


def test_platform_port_environment_variable(monkeypatch):
    monkeypatch.delenv("MCP_PORT", raising=False)
    monkeypatch.setenv("PORT", "9123")

    assert Settings(_env_file=None).mcp_port == 9123


def test_mcp_port_takes_precedence(monkeypatch):
    monkeypatch.setenv("PORT", "9123")
    monkeypatch.setenv("MCP_PORT", "8123")

    assert Settings(_env_file=None).mcp_port == 8123
