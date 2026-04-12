# MCP Server Setup — Atomadic

Connect Atomadic as an MCP server to any compatible client.

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "atomadic": {
      "url": "https://atomadic.tech/mcp"
    }
  }
}
```

Restart Claude Desktop. Atomadic tools will appear in the tools menu.

## Claude Code

Add to `~/.claude/claude_code_config.json`:

```json
{
  "mcpServers": {
    "atomadic": {
      "url": "https://atomadic.tech/mcp"
    }
  }
}
```

## Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "atomadic": {
      "url": "https://atomadic.tech/mcp"
    }
  }
}
```

## Available MCP Tools

Once connected, these tools are available:

| Tool | Description |
|------|-------------|
| `health` | Service health and version |
| `metrics` | API usage metrics |
| `oracle_entropy` | Entropy epoch oracle |
| `oracle_hallucination` | Hallucination detection with formal proof |
| `ratchetgate_session` | Query session status |
| `ratchetgate_register` | Register new secure session |
| `ratchetgate_advance` | Advance session ratchet |
| `inference` | Chat completions with hallucination guard |
| `inference_stream` | Streaming inference with chain-of-thought |

## Verify MCP Server

```bash
# Check MCP endpoint is responsive
curl https://atomadic.tech/mcp
```
