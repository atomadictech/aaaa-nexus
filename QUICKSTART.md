# AAAA Nexus — Quickstart Guide

Add formally verified AI safety infrastructure to your agent in **5 minutes**.

**Base URL:** `https://atomadic.tech`
**No signup required** for free endpoints and free trials.

---

## Example 1: Free Call (No Auth, No Signup)

The fastest way to see the API in action:

```bash
# Get a cryptographically generated random number
curl https://atomadic.tech/v1/rng/quantum
```

```json
{
  "format": "hex",
  "product": "DCM-1001",
  "random": 1725672031,
  "version": "0.5.0"
}
```

More free endpoints — all respond instantly:

```bash
# System health + subsystem state
curl https://atomadic.tech/health | jq .

# Entropy oracle (proves epoch-bounded randomness)
curl https://atomadic.tech/v1/oracle/entropy | jq .

# Sybil resistance check on your IP
curl https://atomadic.tech/v1/identity/sybil-check

# Trust ceiling (bounded by formal proof)
curl https://atomadic.tech/v1/trust/decay

# Live platform metrics
curl https://atomadic.tech/v1/metrics | jq '{endpoints, product_families}'

# Browse available AI models
curl https://atomadic.tech/v1/bitnet/models | jq '.models[] | {id, params_b, status}'

# Register your agent in the A2A registry
curl -X POST https://atomadic.tech/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent-001", "capabilities": ["inference", "search"]}'
```

---

## Example 2: Free Trial on Paid Endpoints

Every paid endpoint gives you **3 free calls per day** — no API key, no payment. Responses are identical to paid calls (2-second delay applied).

```bash
# Try the hallucination oracle — first 3 calls are free
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -d '{"claim": "Water boils at 100°C at sea level", "context": "chemistry-qa"}'

# Try threat scoring
curl -X POST https://atomadic.tech/v1/threat/score \
  -H "Content-Type: application/json" \
  -d '{"payload": {"query": "SELECT * FROM users"}, "agent_id": "test-agent"}'

# Try compliance check
curl -X POST https://atomadic.tech/v1/compliance/check \
  -H "Content-Type: application/json" \
  -d '{"framework": "eu-ai-act", "agent_card": {"name": "my-agent", "capabilities": ["inference"]}}'
```

After 3 calls, you'll receive `HTTP 429`. To continue: buy credits or use x402 USDC.

---

## Example 3: Buy Credits and Use an API Key

### Step 1 — Browse available prices

```bash
curl https://atomadic.tech/v1/payments/stripe/prices | \
  jq '.prices[] | select(.metadata.product_type == "api_credits") | {nickname, unit_amount}'
```

Example output:

```json
{ "nickname": "API Credits — Starter (500 calls)",   "unit_amount": 800  }
{ "nickname": "API Credits — Standard (2500 calls)", "unit_amount": 1500 }
{ "nickname": "API Credits — Pro (10000 calls)",     "unit_amount": 4900 }
```

### Step 2 — Create a checkout session

```bash
# Get the price_id from the prices endpoint, then:
SESSION=$(curl -s -X POST https://atomadic.tech/v1/payments/stripe/session \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_1TLa6...",
    "email": "you@example.com"
  }')

echo $SESSION | jq -r '.checkout_url'
# → https://checkout.stripe.com/c/pay/cs_live_...
```

### Step 3 — Complete payment

Open the `checkout_url` in a browser. Pay with card, Apple Pay, or Google Pay.

### Step 4 — Receive your API key by email

After payment, your API key (`an_...`) is delivered to your email via Resend. It typically arrives within 30 seconds.

### Step 5 — Use the API key

```bash
export NEXUS_API_KEY="an_YOUR_KEY_HERE"

# Hallucination oracle — no trial delay, no rate limit on your credits
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "X-API-Key: $NEXUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"claim": "GPT-4 was released in 2022", "context": "ai-history"}'

# HELIX model compression
curl -X POST https://atomadic.tech/v1/compress \
  -H "X-API-Key: $NEXUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model_id": "meta-llama/Llama-3.2-1B-Instruct", "tier": "fidelity"}'

# Threat scoring
curl -X POST https://atomadic.tech/v1/threat/score \
  -H "X-API-Key: $NEXUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"payload": {"user_input": "..."}, "agent_id": "my-agent-001"}'
```

---

## Example 4: MCP Server Integration

Add AAAA Nexus as an MCP resource in **30 seconds**. Works with Claude Desktop, Claude Code, Cursor, and any MCP-compatible client.

### Claude Desktop / Claude Code

Add to `~/.claude/claude_desktop_config.json` (or your MCP config file):

```json
{
  "mcpServers": {
    "aaaa-nexus": {
      "url": "https://atomadic.tech/mcp"
    }
  }
}
```

Restart your client. You now have access to all 27 AAAA Nexus skills directly in your AI assistant.

### Verify MCP connectivity

```bash
# Check MCP server card
curl https://atomadic.tech/.well-known/mcp.json | jq .

# Or check the A2A agent card for full skills list
curl https://atomadic.tech/.well-known/agent.json | jq '[.skills[] | .id]'
```

### Example MCP skills available

Once connected, your agent can call:
- `quantum-rng` — Generate cryptographically secure random bytes
- `threat-score` — Score any payload for security threats
- `ratchetgate` — Secure MCP sessions against CVE-2025-6514
- `hallucination-oracle` — Get a certified hallucination bound
- `compliance` — EU AI Act and NIST RMF compliance checks
- `escrow` — Create trustless agent-to-agent payment escrow
- `reputation` — Look up agent trust scores
- `pre-action-auth` — Authorize tool calls before execution
- `consensus-broker` — Multi-agent voting and consensus

---

## Example 5: x402 USDC Payment (Autonomous Agents)

For agents that need to pay autonomously — no Stripe, no email, no API key management.

### High-level flow

```
1. Call any paid endpoint → HTTP 402 + payment details
2. Send USDC to treasury  → on Base L2 (chain 8453)
3. Retry with payment proof → Get result (zero latency penalty)
```

### Step 1 — Trigger the 402

```bash
# Call without auth — receives 402 with payment instructions
curl -v -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -d '{"claim": "test", "context": "x402-demo"}' 2>&1 | grep -A 20 "< HTTP"
```

Expected 402 response headers include:

```
X-Payment-Amount: 2000          # micro-USDC (= $0.002)
X-Payment-Chain:  8453          # Base L2
X-Payment-Token:  0x833589...   # USDC contract on Base
X-Payment-To:     0x...         # Treasury address
```

### Step 2 — Send USDC on Base L2

Using your wallet or agent's on-chain capabilities:

```
Network:  Base L2 (chain ID 8453)
Token:    USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)
Amount:   as specified in X-Payment-Amount header
To:       as specified in X-Payment-To header
```

### Step 3 — Retry with payment proof

```bash
# Include the transaction hash as payment proof
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -H "X-Payment: 0xYOUR_TX_HASH" \
  -d '{"claim": "test", "context": "x402-demo"}'
```

### Python example (agent integration)

```python
import requests

API = "https://atomadic.tech"

def call_with_x402(endpoint: str, body: dict, payment_proof: str) -> dict:
    """Call a paid endpoint with x402 USDC payment proof."""
    resp = requests.post(
        f"{API}{endpoint}",
        json=body,
        headers={
            "Content-Type": "application/json",
            "X-Payment": payment_proof,
        }
    )
    resp.raise_for_status()
    return resp.json()

# Usage
result = call_with_x402(
    "/v1/oracle/hallucination",
    {"claim": "The capital of France is Paris", "context": "geography"},
    "0xYOUR_USDC_TX_HASH"
)
print(result)
```

---

## Example 6: Python SDK (Requests)

```python
import requests

API = "https://atomadic.tech"
API_KEY = "an_YOUR_KEY_HERE"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

# Check health
health = requests.get(f"{API}/health").json()
print(f"Status: {health['status']}, Epoch: {health['epoch']}")

# Get a random value
rng = requests.get(f"{API}/v1/rng/quantum").json()
print(f"Random: {rng['random']}")

# Score a threat
threat = requests.post(
    f"{API}/v1/threat/score",
    headers=HEADERS,
    json={"payload": {"query": "DROP TABLE users"}, "agent_id": "security-agent"}
).json()
print(f"Threat score: {threat}")

# Compliance check
compliance = requests.post(
    f"{API}/v1/compliance/check",
    headers=HEADERS,
    json={"framework": "eu-ai-act", "agent_card": {"name": "my-bot", "capabilities": ["inference"]}}
).json()
print(f"Compliance: {compliance}")
```

---

## Example 7: TypeScript / Node.js

```typescript
const API = "https://atomadic.tech";
const API_KEY = process.env.NEXUS_API_KEY!;

const headers = {
  "X-API-Key": API_KEY,
  "Content-Type": "application/json",
};

async function nexus<T>(path: string, body?: object): Promise<T> {
  const resp = await fetch(`${API}${path}`, {
    method: body ? "POST" : "GET",
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!resp.ok) throw new Error(`${resp.status} ${await resp.text()}`);
  return resp.json();
}

// Usage
const health = await nexus<{ status: string; epoch: number }>("/health");
console.log(`Epoch: ${health.epoch}`);

const rng = await nexus<{ random: number }>("/v1/rng/quantum");
console.log(`Random: ${rng.random}`);

const threat = await nexus("/v1/threat/score", {
  payload: { query: "user input here" },
  agent_id: "ts-agent-001",
});
console.log("Threat:", threat);
```

---

## Free Trial Limits

| Limit | Value |
|-------|-------|
| Free calls per endpoint per day | 3 |
| Scope | Per IP address |
| Delay on trial calls | 2 seconds |
| Delay on paid calls | 0 seconds |
| Auth required for trial | None |

After 3 trial calls on an endpoint, you receive `HTTP 429`. Reset happens at midnight UTC.

---

## Next Steps

| Resource | Link |
|----------|------|
| Full API reference | [API_REFERENCE.md](./API_REFERENCE.md) |
| Blackbox proof verification | [PROOF_OF_CORRECTNESS.md](./PROOF_OF_CORRECTNESS.md) |
| Pricing details | [docs/PRICING.md](./docs/PRICING.md) |
| Run automated verification | `./verify.sh` |
| Get an API key | https://atomadic.tech/pay |
| A2A agent card | https://atomadic.tech/.well-known/agent.json |
| MCP server | https://atomadic.tech/mcp |

---

*Quickstart — AAAA Nexus v0.5.0 — April 2026*
*All curl examples verified against production at `https://atomadic.tech`*
