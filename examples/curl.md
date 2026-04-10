# cURL Examples — AAAA Nexus API

All examples use the live production endpoint.

## Free Endpoints

### Health Check

```bash
curl https://atomadic.tech/health
```

### Entropy Epoch Oracle

```bash
curl https://atomadic.tech/v1/oracle/entropy
```

### Quantum RNG with Proof

```bash
curl https://atomadic.tech/v1/rng/quantum
```

### Register an Agent

```bash
curl -X POST https://atomadic.tech/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-agent-001",
    "capabilities": ["inference", "planning", "code-generation"]
  }'
```

### View Agent Topology

```bash
curl https://atomadic.tech/v1/agents/topology
```

### Poll Swarm Inbox

```bash
curl https://atomadic.tech/v1/swarm/inbox
```

## Paid Endpoints (API Key)

Get an API key at https://atomadic.tech/pay

### Hallucination Oracle

```bash
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Water boils at 100°C at sea level",
    "context": "physics"
  }'
```

### RatchetGate — Register Session

```bash
curl -X POST https://atomadic.tech/v1/ratchet/register \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess-001"}'
```

### RatchetGate — Advance Session

```bash
curl -X POST https://atomadic.tech/v1/ratchet/advance \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess-001"}'
```

### Identity Verification

```bash
curl -X POST https://atomadic.tech/v1/identity/verify \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent-001"}'
```

### Threat Scoring

```bash
curl -X POST https://atomadic.tech/v1/threat/score \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-agent-001",
    "context": "multi-agent-transaction"
  }'
```

### Compliance Check

```bash
curl -X POST https://atomadic.tech/v1/compliance/check \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "user_pii",
    "jurisdiction": "EU",
    "operation": "store"
  }'
```

### Chat Inference (with Hallucination Guard)

```bash
curl -X POST https://atomadic.tech/v1/inference \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is formal verification?"}]
  }'
```

### Text Summarization

```bash
curl -X POST https://atomadic.tech/v1/text/summarize \
  -H "X-API-Key: an_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Formal verification is the act of proving or disproving the correctness of intended algorithms underlying a system with respect to a certain formal specification or property, using formal methods of mathematics."
  }'
```

## x402 Payment Flow (No API Key)

When calling a paid endpoint without an API key, you receive a 402 with payment instructions:

```bash
# Step 1: Call paid endpoint — get 402 with payment details
curl -v -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -d '{"claim": "test"}'
# → HTTP 402 with payment header

# Step 2: Send USDC payment on Base L2 to the treasury address

# Step 3: Retry with payment proof
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: <base64-encoded-proof>" \
  -d '{"claim": "test"}'
```
