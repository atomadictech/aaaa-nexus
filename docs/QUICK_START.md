# Quick Start Guide — AAAA Nexus

Get up and running in 5 minutes.

## Prerequisites

- **curl** (for HTTP examples) or **Node.js 18+** / **Python 3.8+** for SDK examples
- **API Key** (get free at https://aaaa-nexus.atomadictech.workers.dev/pay) or **USDC wallet on Base L2**

## Step 1: Verify the API is Live

```bash
curl https://aaaa-nexus.atomadictech.workers.dev/health
```

Expected:
```json
{
  "status": "ok",
  "version": "...",
  "timestamp": "..."
}
```

## Step 2: Try Free Endpoints

### Entropy Epoch Oracle

```bash
curl https://aaaa-nexus.atomadictech.workers.dev/v1/oracle/entropy
```

### Quantum RNG with Cryptographic Proof

```bash
curl https://aaaa-nexus.atomadictech.workers.dev/v1/rng/quantum
```

### Register an Agent (Free)

```bash
curl -X POST https://aaaa-nexus.atomadictech.workers.dev/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-first-agent",
    "capabilities": ["inference", "planning"]
  }'
```

### View Agent Topology

```bash
curl https://aaaa-nexus.atomadictech.workers.dev/v1/agents/topology
```

## Step 3: Get an API Key (Optional)

For paid endpoints, get a key at:

https://aaaa-nexus.atomadictech.workers.dev/pay

Then use it in requests:

```bash
curl -X POST https://aaaa-nexus.atomadictech.workers.dev/v1/oracle/hallucination \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"claim": "The capital of France is Paris", "context": "geography"}'
```

## Step 4: Or Pay Autonomously with x402

No signup required. Any USDC wallet on Base L2 works:

```
1. Call paid endpoint → HTTP 402 with payment details
2. Send USDC to treasury on Base L2
3. Retry with payment proof header
4. Get result
```

## Step 5: Add as MCP Server

Add AAAA Nexus to Claude Desktop, Claude Code, or Cursor:

```json
{
  "mcpServers": {
    "aaaa-nexus": {
      "url": "https://aaaa-nexus.atomadictech.workers.dev/mcp"
    }
  }
}
```

## Step 6: Run the Proof Verifier

Independently verify our formal verification claims:

```bash
git clone https://github.com/atomadictech/aaaa-nexus.git
cd aaaa-nexus
chmod +x verify.sh
./verify.sh
```

## Next Steps

- [Full cURL examples](../examples/curl.md)
- [TypeScript integration](../examples/typescript.md)
- [Python integration](../examples/python.md)
- [MCP setup](../examples/mcp.md)
- [Pricing & Billing](./PRICING.md)
- [OpenAPI Spec](https://aaaa-nexus.atomadictech.workers.dev/openapi.json)

## Troubleshooting

| Error | Meaning | Fix |
|-------|---------|-----|
| `402` | Payment required | Get an API key or pay with x402 |
| `429` | Rate limited | Upgrade tier or wait |
| `401` | Invalid API key | Check key at /pay |
| `502` | Temporary outage | Check /health |

## Need Help?

Email atomadic@proton.me
