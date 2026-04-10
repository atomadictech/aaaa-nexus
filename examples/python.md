# Python Integration — AAAA Nexus API

## Using `requests`

```python
import requests
import os

API_BASE = "https://atomadic.tech"
API_KEY = os.environ.get("AAAA_NEXUS_API_KEY")


# --- Free Endpoints ---

# Health check
health = requests.get(f"{API_BASE}/health").json()
print(health)

# Entropy oracle
entropy = requests.get(f"{API_BASE}/v1/oracle/entropy").json()
print(entropy)

# Quantum RNG
rng = requests.get(f"{API_BASE}/v1/rng/quantum").json()
print(rng)

# Register agent
agent = requests.post(
    f"{API_BASE}/v1/agents/register",
    json={
        "agent_id": "py-agent-001",
        "capabilities": ["inference", "planning", "data-analysis"],
    },
).json()
print(agent)

# Agent topology
topology = requests.get(f"{API_BASE}/v1/agents/topology").json()
print(topology)


# --- Paid Endpoints (API Key) ---

headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

# Hallucination oracle
hall = requests.post(
    f"{API_BASE}/v1/oracle/hallucination",
    headers=headers,
    json={"claim": "Earth orbits the Sun", "context": "astronomy"},
).json()
print(hall)

# Threat scoring
threat = requests.post(
    f"{API_BASE}/v1/threat/score",
    headers=headers,
    json={"agent_id": "py-agent-001", "context": "data-pipeline"},
).json()
print(threat)

# Compliance check
compliance = requests.post(
    f"{API_BASE}/v1/compliance/check",
    headers=headers,
    json={
        "data_type": "user_pii",
        "jurisdiction": "EU",
        "operation": "process",
    },
).json()
print(compliance)

# Chat inference
inference = requests.post(
    f"{API_BASE}/v1/inference",
    headers=headers,
    json={
        "messages": [{"role": "user", "content": "What is formal verification?"}]
    },
).json()
print(inference)

# Text summarization
summary = requests.post(
    f"{API_BASE}/v1/text/summarize",
    headers=headers,
    json={
        "text": "Formal verification uses mathematical proofs to verify "
        "that software behaves correctly according to its specification."
    },
).json()
print(summary)
```

## Using `httpx` (Async)

```python
import httpx
import asyncio

API_BASE = "https://atomadic.tech"


async def main():
    async with httpx.AsyncClient(base_url=API_BASE) as client:
        # Parallel free calls
        health, entropy, rng = await asyncio.gather(
            client.get("/health"),
            client.get("/v1/oracle/entropy"),
            client.get("/v1/rng/quantum"),
        )
        print("Health:", health.json())
        print("Entropy:", entropy.json())
        print("RNG:", rng.json())


asyncio.run(main())
```

## A2A Protocol

```python
# Discover agent capabilities
agent_card = requests.get(f"{API_BASE}/.well-known/agent.json").json()
print("Agent:", agent_card)

# Send A2A message
a2a = requests.post(
    f"{API_BASE}/a2a",
    json={
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "Check health"}],
            }
        },
        "id": "1",
    },
).json()
print(a2a)
```
