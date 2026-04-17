# AAAA Nexus — API Reference

**Base URL:** `https://atomadic.tech`
**Version:** v0.5.1
**Live endpoint count:** 119 across 30 product families

All responses are JSON. All requests accept `Content-Type: application/json`.

## Authentication

| Method | Header | When to Use |
|--------|--------|-------------|
| **None** | — | Free endpoints (no auth needed) |
| **API Key** | `X-API-Key: an_YOUR_KEY` | Bulk calls — buy at `/pay` |
| **x402 USDC** | `X-Payment: <proof>` | Autonomous agent payments on Base L2 |
| **Owner Token** | `X-Admin-Token: <token>` | Admin endpoints only |

**Free trial:** Every paid endpoint allows 3 free calls/day per IP with no credentials. Responses are identical to production — 2s rate-limit delay applied.

---

## Section 1: Payment & Billing

### POST /v1/payments/stripe/session

Creates a Stripe Checkout session for purchasing credit packs or prompt packs.

**Auth:** None required

**Request:**

```bash
curl -X POST https://atomadic.tech/v1/payments/stripe/session \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_1TLa6...",
    "email": "you@example.com",
    "success_url": "https://yoursite.com/thank-you",
    "cancel_url": "https://yoursite.com/pricing"
  }'
```

Or with inline pricing (no price_id needed):

```bash
curl -X POST https://atomadic.tech/v1/payments/stripe/session \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "API Credits — Standard (2500 calls)",
    "price_cents": 1500,
    "email": "you@example.com"
  }'
```

**Response:**

```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_live_...",
  "session_id": "cs_live_...",
  "expires_at": 1776135000
}
```

**Error cases:**

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | `missing_price` | Provide `price_id` or `product_name + price_cents` |
| 400 | `invalid_email` | Email field required |
| 500 | `stripe_error` | Upstream Stripe error |

**Status:** LIVE

---

### GET /v1/payments/stripe/prices

Returns all active Stripe prices — credit packs, prompt packs, and model downloads.

**Auth:** None required

```bash
curl https://atomadic.tech/v1/payments/stripe/prices | jq '.prices[] | {id, nickname, unit_amount}'
```

**Response structure:**

```json
{
  "prices": [
    {
      "id": "price_1TLa6...",
      "nickname": "API Credits — Starter (500 calls)",
      "unit_amount": 800,
      "currency": "usd",
      "type": "one_time",
      "metadata": { "product_type": "api_credits", "calls": "500" }
    }
  ]
}
```

**Status:** LIVE

---

### POST /v1/pay/verify

Verifies a completed Stripe payment and returns the issued API key.

**Auth:** None required (Stripe session ID used as verification)

```bash
curl -X POST https://atomadic.tech/v1/pay/verify \
  -H "Content-Type: application/json" \
  -d '{ "session_id": "cs_live_..." }'
```

**Response:**

```json
{
  "api_key": "an_...",
  "calls_remaining": 2500,
  "product": "API Credits — Standard",
  "valid_until": null
}
```

**Status:** LIVE

---

### POST /v1/webhooks/stripe

Stripe webhook receiver — fulfills orders and triggers API key delivery by email. **Do not call this directly.** This endpoint is called by Stripe after successful payment.

**Auth:** Stripe webhook signature (auto-verified)

**Status:** LIVE — internal

---

### GET /v1/admin/webhook-log

Returns recent webhook processing log entries.

**Auth:** Owner token required (`X-Admin-Token`)

```bash
curl https://atomadic.tech/v1/admin/webhook-log \
  -H "X-Admin-Token: YOUR_OWNER_TOKEN"
```

**Status:** LIVE — admin only

---

## Section 2: Free Infrastructure

All endpoints in this section require **no authentication** and have **no rate limit** (beyond standard abuse protection).

---

### GET /health

System health check. Returns current status, version, epoch, and HELIX subsystem state.

```bash
curl https://atomadic.tech/health
```

**Response:**

```json
{
  "build": "2026-04-08",
  "epoch": 17413063,
  "helix": {
    "anti_hallucination": true,
    "ecc_status": true,
    "integrity_parity": true,
    "model": "llama-3.1-8b-instruct",
    "provider": "Cloudflare Workers AI"
  },
  "next_epoch_in_s": 61,
  "status": "ok",
  "version": "0.5.0"
}
```

**Fields:**
- `status`: `"ok"` | `"degraded"` | `"down"`
- `epoch`: monotonically increasing epoch counter (~102s windows)
- `next_epoch_in_s`: seconds until next epoch (circuit breaker re-evaluation window)
- `helix.ecc_status`: error-correction subsystem active

**Status:** LIVE

---

### GET /v1/oracle/entropy

Returns the current entropy epoch with nonce seed. Used to verify that randomness is epoch-bounded.

```bash
curl https://atomadic.tech/v1/oracle/entropy
```

**Response:**

```json
{
  "client_ip": "2001:...",
  "epoch": 17413063,
  "epoch_end_s": 1776132528,
  "epoch_start_s": 1776132426,
  "nonce_seed_hex": "83b2090100000000",
  "now_unix": 1776132472,
  "product": "DCM-ENT",
  "time_to_next_s": 56,
  "window_s": 102
}
```

**Status:** LIVE

---

### GET /v1/rng/quantum

Returns a cryptographically generated random value.

```bash
curl https://atomadic.tech/v1/rng/quantum
```

**Response:**

```json
{
  "format": "hex",
  "product": "DCM-1001",
  "random": 1725672031,
  "version": "0.5.0"
}
```

**Status:** LIVE

---

### GET /v1/rng/verify

Verifies the current epoch's random value is valid.

```bash
curl https://atomadic.tech/v1/rng/verify
```

**Response:**

```json
{
  "product": "DCM-1001",
  "valid": true,
  "version": "0.5.0"
}
```

**Status:** LIVE

---

### GET /v1/trust/decay

Returns the current trust ceiling value.

```bash
curl https://atomadic.tech/v1/trust/decay
```

**Response:**

```json
{
  "product": "DCM-1003",
  "trust_ceiling": 1.0,
  "version": "0.5.0"
}
```

**Status:** LIVE

---

### GET /v1/identity/sybil-check

Performs a Sybil-resistance check on the calling IP.

```bash
curl https://atomadic.tech/v1/identity/sybil-check
```

**Response:**

```json
{
  "product": "IDT-209",
  "sybil_risk": "low",
  "version": "0.5.0"
}
```

**sybil_risk values:** `"low"` | `"medium"` | `"high"`

**Status:** LIVE

---

### GET /v1/auth/zero-trust

Zero-trust attestation endpoint.

```bash
curl https://atomadic.tech/v1/auth/zero-trust
```

**Note:** Returns 500 if called without a valid session context. Designed for use within authenticated agent sessions.

**Status:** LIVE (session-context required)

---

### GET /v1/metrics

Returns platform-wide metrics: endpoint count, pricing, uptime target.

```bash
curl https://atomadic.tech/v1/metrics
```

**Response:**

```json
{
  "endpoints": 119,
  "epoch": 1776132480,
  "platform": "AAAA-Nexus",
  "pricing": {
    "currency": "USDC",
    "inference": "$0.025",
    "min_call": "$0.002",
    "model": "pay-per-call",
    "network": "base"
  },
  "product_families": 30,
  "uptime_target": "99.9%",
  "version": "0.5.1"
}
```

**Status:** LIVE

---

### GET /v1/embed

Returns the HELIX compression service manifest with algorithm details and available compressed models.

```bash
curl https://atomadic.tech/v1/embed | jq '{service, tiers: .tiers | keys}'
```

**Status:** LIVE — see full response at `https://atomadic.tech/v1/embed`

---

### GET /v1/bitnet/models

Returns the catalog of available BitNet and HELIX compressed models.

```bash
curl https://atomadic.tech/v1/bitnet/models | jq '.models[] | {id, params_b, status}'
```

**Response (excerpt):**

```json
{
  "product": "BIT-102",
  "total": 7,
  "models": [
    { "id": "bitnet-b1.58-2B-4T",        "params_b": 2.4,  "status": "available" },
    { "id": "llama3-8B-1.58-100B",        "params_b": 8.0,  "status": "available" },
    { "id": "helix-llama3.2-1b-fidelity", "params_b": 1.2,  "status": "available" },
    { "id": "helix-qwen2.5-7b-balanced",  "params_b": 7.6,  "status": "available" },
    { "id": "helix-phi3.5-mini-fidelity", "params_b": 3.8,  "status": "available" }
  ]
}
```

**Status:** LIVE

---

### GET /v1/agents/register (POST)

Register an agent with the A2A-compatible agent registry.

```bash
curl -X POST https://atomadic.tech/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent-001", "capabilities": ["inference", "search"]}'
```

**Status:** LIVE

---

### GET /v1/agents/topology

Returns the current agent swarm topology.

```bash
curl https://atomadic.tech/v1/agents/topology
```

**Response:**

```json
{
  "agent_count": 0,
  "topology": [],
  "version": "0.5.0"
}
```

**Status:** LIVE

---

### GET /.well-known/agent.json

Google A2A agent card — describes all capabilities for A2A protocol discovery.

```bash
curl https://atomadic.tech/.well-known/agent.json | jq '{name, version, skills: [.skills[].id]}'
```

**Status:** LIVE — 27 skills listed

---

### GET /openapi.json

OpenAPI 3.0 spec (stub — full spec served via live endpoint).

```bash
curl https://atomadic.tech/openapi.json
```

**Status:** LIVE

---

## Section 3: Premium Endpoints (API Key or x402 USDC)

These endpoints require either:
- `X-API-Key: an_YOUR_KEY` — for bulk usage (buy at `/pay`)
- x402 USDC payment on Base L2 — for autonomous agent usage

Free trial: 3 calls/day per IP with no auth (2s delay).

---

### POST /v1/compress

HELIX geometric model compression — submits a model for lossless lattice-based vector quantization with ECC-guarded integrity.

```bash
curl -X POST https://atomadic.tech/v1/compress \
  -H "X-API-Key: an_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model_id": "meta-llama/Llama-3.2-1B-Instruct", "tier": "fidelity"}'
```

**Auth:** API key or x402 | **Status:** LIVE

---

### POST /v1/threat/score

Scores a payload for security threats using triality consensus.

```bash
curl -X POST https://atomadic.tech/v1/threat/score \
  -H "X-API-Key: an_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"payload": {"query": "...", "context": "..."}, "agent_id": "agent-001"}'
```

**Auth:** API key or x402 | **Status:** LIVE

---

### POST /v1/compliance/check

EU AI Act / NIST RMF compliance check with machine-verifiable proof certificate.

```bash
curl -X POST https://atomadic.tech/v1/compliance/check \
  -H "X-API-Key: an_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent_card": {...}, "framework": "eu-ai-act"}'
```

**frameworks:** `"eu-ai-act"` | `"nist-rmf"` | `"iso-42001"`

**Auth:** API key or x402 | **Status:** LIVE

---

### POST /v1/oracle/hallucination

Returns a certified upper bound on hallucination probability for an LLM claim.

```bash
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "X-API-Key: an_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"claim": "The Eiffel Tower is in Paris", "context": "geography-qa"}'
```

**Auth:** API key or x402 (returns HTTP 402 without auth) | **Status:** LIVE

---

### POST /v1/ratchet/register and related

RatchetGate session security — 47-epoch safe-prime ratchet for MCP CVE-2025-6514 mitigation.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/ratchet/register` | POST | Register a new ratchet session |
| `/v1/ratchet/advance` | POST | Advance to next epoch |
| `/v1/ratchet/probe` | GET | Health probe for session |
| `/v1/ratchet/status` | GET | Session status |

**Auth:** API key or x402 | **Status:** LIVE

---

### Forge Marketplace

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/forge/leaderboard` | GET | None | Browse model leaderboard |
| `/v1/forge/quarantine` | GET | None | View quarantined models |
| `/v1/forge/verify` | POST | API key | Verify a model submission |
| `/v1/forge/delta/submit` | POST | API key | Submit a model delta |
| `/v1/forge/badge/{model}` | GET | None | Get model quality badge |

**Status:** LIVE

---

### Agent Management

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/swarm/inbox` | GET/POST | API key | Agent swarm messaging |
| `/v1/identity/verify` | POST | API key/x402 | Topological identity verification |
| `/v1/delegation/validate` | POST | API key/x402 | UCAN delegation chain validation |
| `/v1/escrow/create` | POST | API key/x402 | Create agent-to-agent escrow |
| `/v1/reputation/record` | POST | API key/x402 | Record agent interaction |
| `/v1/sla/register` | POST | API key/x402 | Register an SLA |

**Auth:** API key or x402 | **Status:** LIVE

---

### Inference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/inference` | POST | API key/x402 | LLM inference via Llama 3.1 8B |
| `/v1/text/summarize` | POST | API key/x402 | Text summarization |
| `/v1/text/sentiment` | POST | API key/x402 | Sentiment analysis |
| `/v1/text/ner` | POST | API key/x402 | Named entity recognition |
| `/v1/text/translate` | POST | API key/x402 | Translation |

**Status:** LIVE

---

### DeFi Suite (9 endpoints)

| Endpoint | Description |
|----------|-------------|
| `/v1/defi/oracle/verify` | Oracle price verification |
| `/v1/defi/liquidation/check` | Liquidation threshold check |
| `/v1/defi/bridge/proof` | Cross-chain bridge proof |
| `/v1/defi/vrf/gaming` | VRF for gaming/NFT minting |
| `/v1/defi/lp/optimize` | LP position optimization |
| `/v1/defi/risk/score` | Protocol risk scoring |
| `/v1/defi/contract/audit` | Smart contract audit |
| `/v1/defi/yield/optimize` | Yield optimization |
| `/v1/defi/mev/shield` | MEV protection check |

**Auth:** API key or x402 | **Status:** LIVE

---

### Compliance Suite (12 endpoints)

| Endpoint | Description |
|----------|-------------|
| `/v1/compliance/fairness` | Fairness proof certificate |
| `/v1/compliance/explainability` | Explainability certificate |
| `/v1/compliance/lineage` | Data lineage chain |
| `/v1/compliance/drift` | Model drift monitoring |
| `/v1/compliance/incident` | Incident logging |
| `/v1/compliance/audit` | Audit trail export |
| `/v1/compliance/bridge/proof` | Cross-system compliance bridge |
| `/v1/compliance/oversight` | Human oversight log |
| `/v1/compliance/liquid-shield` | Liquid transparency shield |
| `/v1/compliance/contract/verify` | Contract verification |
| `/v1/compliance/explain/cert` | Explanation certificate |
| `/v1/compliance/check` | Full compliance gate |

**Auth:** API key or x402 | **Status:** LIVE

---

## Section 4: Admin & Monitoring

All admin endpoints require an owner token (`X-Admin-Token`).

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/admin/auth` | POST | Admin authentication |
| `/v1/admin/keys` | GET | List all issued API keys |
| `/v1/admin/revenue` | GET | Revenue summary |
| `/v1/admin/payments` | GET | Payment history |
| `/v1/admin/stripe/bootstrap` | POST | Bootstrap Stripe price catalog |
| `/v1/admin/webhook-log` | GET | Webhook processing log |
| `/v1/portal/key/status` | GET | Key status check |
| `/v1/marketing/dlq` | GET | Marketing dead-letter queue |

---

## Error Reference

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `400` | Bad request — check request body |
| `401` | API key required |
| `402` | Payment required — x402 USDC flow |
| `403` | Forbidden — insufficient permissions |
| `404` | Unknown endpoint (non-/v1/ path) |
| `429` | Rate limited — free trial exhausted (3/day) |
| `500` | Server error |
| `503` | Circuit breaker open — degraded subsystem |

---

## Discovery Endpoints

| URL | Purpose |
|-----|---------|
| `/.well-known/agent.json` | Google A2A agent card |
| `/.well-known/agent-card.json` | Alternative A2A card path |
| `/.well-known/ai-plugin.json` | OpenAI plugin manifest |
| `/.well-known/mcp.json` | MCP server card |
| `/.well-known/pricing.json` | Machine-readable pricing |
| `/.well-known/oauth-protected-resource` | OAuth resource metadata |
| `/openapi.json` | OpenAPI 3.0 spec |
| `/mcp` | MCP endpoint |
| `/robots.txt` | Crawler policy |
| `/sitemap.xml` | Sitemap |
| `/llms.txt` | AI-readable API summary |

---

*API Reference — AAAA Nexus v0.5.0 — April 2026*
*All endpoints verified against `https://atomadic.tech`*
