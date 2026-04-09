# AGENTS.md — AAAA Nexus

This repository is a marketing and integration toolkit for the AAAA Nexus API.
It contains no source code. All interaction is via the live API.

## API Base URL
https://aaaa-nexus.atomadictech.workers.dev

## MCP Server
Add as an MCP server for direct tool access:
```json
{
  "mcpServers": {
    "aaaa-nexus": {
      "url": "https://aaaa-nexus.atomadictech.workers.dev/mcp"
    }
  }
}
```

## Quick Verification
```bash
curl https://aaaa-nexus.atomadictech.workers.dev/health
curl https://aaaa-nexus.atomadictech.workers.dev/v1/rng/quantum
```

## What Agents Can Do With This Repo
- Read `llms.txt` or `llms-full.txt` for structured API reference
- Read `openapi.json` for full endpoint schema
- Read `examples/` for integration code in curl, TypeScript, Python
- Run `verify.sh` to independently verify formal proof claims
- Read `docs/` for pricing, quickstart, use cases, and FAQ

## What This Repo Does NOT Contain
- No source code or implementation
- No API keys or secrets
- No formal proof internals
- No deployment configuration

## Key Files
- `llms.txt` — Concise API summary for LLMs
- `llms-full.txt` — Complete endpoint reference for LLMs
- `openapi.json` — Full OpenAPI specification
- `verify.sh` — Proof verification script (runs against live API)
- `examples/` — Integration examples (curl, TypeScript, Python, MCP)
- `docs/` — Human-readable documentation
