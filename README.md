# AAAA Nexus — Formally Verified AI Safety Infrastructure

[![Live API](https://img.shields.io/badge/API-live-brightgreen)](https://aaaa-nexus.atomadictech.workers.dev)
[![Endpoints](https://img.shields.io/badge/endpoints-78%2B-blue)](https://aaaa-nexus.atomadictech.workers.dev/openapi.json)
[![Verification](https://img.shields.io/badge/proofs-formally%20verified-blueviolet)](#verify-our-claims)
[![MCP Server](https://img.shields.io/badge/MCP-compatible-orange)](https://aaaa-nexus.atomadictech.workers.dev/mcp)

**The only AI safety API where every guarantee is mathematically proved — not benchmarked, not tested, _proved_.**

Production-grade infrastructure for autonomous agents with built-in x402 USDC micropayments, Google A2A protocol support, and MCP server compatibility.

**Live:** https://aaaa-nexus.atomadictech.workers.dev

---

## The Problem

Autonomous agents operating without human oversight face six critical infrastructure gaps:

| Gap | Risk |
|-----|------|
| **Session hijacking** | Credential theft via MCP session fixation (CVE-2025-6514) |
| **Undetected hallucinations** | Agents act on fabricated information |
| **No agent accountability** | Rogue agents operate with zero traceability |
| **Unauditable randomness** | "Random" outputs that can be predicted or replayed |
| **Unbounded delegation** | Agents spawn infinite sub-agents without limits |
| **No economic framework** | No way for agents to pay each other for services |

## The Solution

AAAA Nexus provides **78+ API endpoints across 19 product families** — every safety claim backed by formal proofs in Lean 4.

### Core Products

| Product | What It Does |
|---------|-------------|
| **Hallucination Oracle** | Certified upper bound on hallucination probability |
| **RatchetGate** | Session re-keying that fixes CVE-2025-6514 |
| **VeriRand** | Cryptographically verified quantum randomness |
| **Trust Phase Oracle** | Mathematical trust scoring with proved ceiling |
| **Topological Identity** | Sybil-resistant agent verification |
| **AAAA Shield** | Post-quantum session security |
| **Agent Discovery** | A2A-compatible agent registry and topology |
| **SLA Engine** | Enforceable service-level agreements between agents |
| **Agent Escrow** | Trustless payment escrow for agent-to-agent work |
| **Reputation Ledger** | On-chain reputation tracking |

### Free Endpoints (No Payment Required)

```bash
# Service health
curl https://aaaa-nexus.atomadictech.workers.dev/health

# Entropy epoch oracle
curl https://aaaa-nexus.atomadictech.workers.dev/v1/oracle/entropy

# Quantum randomness with proof
curl https://aaaa-nexus.atomadictech.workers.dev/v1/rng/quantum

# Register your agent
curl -X POST https://aaaa-nexus.atomadictech.workers.dev/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent", "capabilities": ["inference"]}'

# View agent topology
curl https://aaaa-nexus.atomadictech.workers.dev/v1/agents/topology
```

### Paid Endpoints (x402 USDC or API Key)

Starting at **$0.002/call**. See [Pricing](./docs/PRICING.md) for full details.

```bash
# Hallucination check (requires payment)
curl -X POST https://aaaa-nexus.atomadictech.workers.dev/v1/oracle/hallucination \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"claim": "The capital of France is Paris", "context": "geography"}'
```

---

## Verify Our Claims

**Don't trust us. Verify.**

We include a proof verifier that calls the live API to independently confirm our formal verification claims. No source code is required — the proofs are verified against the production system.

```bash
# Run the full verification suite
./verify.sh

# Or verify individual claims
./verify.sh --check hallucination-bound
./verify.sh --check session-security
./verify.sh --check trust-ceiling
./verify.sh --check delegation-depth
```

The verifier checks:
- Formal proof certificates are valid and non-trivial (zero `sorry`, zero axioms)
- Safety bounds match advertised guarantees
- Cryptographic proofs on randomness outputs are independently verifiable
- Session security properties hold under adversarial conditions

See [`verify.sh`](./verify.sh) for the full verification script.

---

## MCP Server — Add to Claude / Cursor in 30 Seconds

```json
{
  "mcpServers": {
    "aaaa-nexus": {
      "url": "https://aaaa-nexus.atomadictech.workers.dev/mcp"
    }
  }
}
```

---

## x402 Payment Flow

No signup. No API keys. Agents pay autonomously with USDC:

```
1. Call any paid endpoint → HTTP 402 with payment details
2. Send USDC to treasury on Base L2
3. Retry with payment proof header
4. Get result
```

Supported chains: **Base L2**, **Polygon**, **Solana**

Or get an API key for bulk calls: https://aaaa-nexus.atomadictech.workers.dev/pay

---

## A2A Protocol

Fully compatible with Google A2A:

- **Agent card:** `/.well-known/agent.json`
- **A2A endpoint:** `/a2a`
- **Agent registry:** `/v1/agents/register` (free)
- **Swarm relay:** `/v1/swarm/relay` (paid)

---

## Integration Examples

See the [`examples/`](./examples/) directory for ready-to-use integrations:

- **[cURL](./examples/curl.md)** — Copy-paste commands for every endpoint
- **[TypeScript](./examples/typescript.md)** — SDK usage with x402 payments
- **[Python](./examples/python.md)** — Requests-based integration
- **[MCP](./examples/mcp.md)** — Claude Desktop / Cursor setup

---

## Documentation

- [Quick Start Guide](./docs/QUICK_START.md) — Up and running in 5 minutes
- [Pricing & Billing](./docs/PRICING.md) — Tiers, credit packs, x402 rates
- [Product Brief](./PRODUCT_BRIEF.md) — What we're building and why
- [Security Policy](./SECURITY.md) — Responsible disclosure
- [API Reference](https://aaaa-nexus.atomadictech.workers.dev/openapi.json) — Full OpenAPI spec

---

## Quick Links

| Resource | URL |
|----------|-----|
| **Live API** | https://aaaa-nexus.atomadictech.workers.dev |
| **OpenAPI Spec** | https://aaaa-nexus.atomadictech.workers.dev/openapi.json |
| **MCP Server** | https://aaaa-nexus.atomadictech.workers.dev/mcp |
| **A2A Agent Card** | https://aaaa-nexus.atomadictech.workers.dev/.well-known/agent.json |
| **Get API Key** | https://aaaa-nexus.atomadictech.workers.dev/pay |
| **Status** | https://aaaa-nexus.atomadictech.workers.dev/health |

---

## Contact

- **Email:** atomadic@proton.me
- **API:** https://aaaa-nexus.atomadictech.workers.dev

---

## License

Documentation, examples, and the verification script in this repository are provided under **CC BY-ND 4.0**.

The underlying API implementation, algorithms, formal proofs, and infrastructure are **proprietary**. This repository contains no source code — only marketing materials, integration examples, and a proof verification client.

© 2026 Atomadic Tech. All rights reserved.
