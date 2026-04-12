# Use Cases — Atomadic

## 1. Verify LLM Outputs Before Acting

**Problem:** Your agent makes decisions based on LLM outputs, but hallucinations can cause expensive mistakes — wrong trades, incorrect medical advice, false legal claims.

**Solution:** Pipe every critical output through the Hallucination Oracle before acting.

```bash
curl -X POST https://atomadic.tech/v1/oracle/hallucination \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Aspirin is safe to take with warfarin",
    "context": "medical-safety"
  }'
```

**Result:** Certified upper bound on hallucination probability — a formal proof, not a confidence score. Your agent only acts when the bound is below your threshold.

---

## 2. Secure Multi-Agent Sessions

**Problem:** MCP session tokens can be stolen via session fixation. Once stolen, an attacker controls the session indefinitely.

**Solution:** Wrap sessions in RatchetGate. Keys ratchet forward automatically — stolen tokens expire within a proved window.

```bash
# Register session
curl -X POST https://atomadic.tech/v1/ratchet/register \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "critical-session-001"}'

# Advance ratchet periodically
curl -X POST https://atomadic.tech/v1/ratchet/advance \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "critical-session-001"}'
```

**Result:** Even if a session token is compromised, the attacker's access is bounded by a mathematically proved window.

---

## 3. Build a Trustless Agent Marketplace

**Problem:** You want agents to buy and sell services from each other, but there's no trust — any agent could take payment and not deliver.

**Solution:** Combine Agent Escrow + Reputation Ledger + x402 payments. Payment is held in escrow until the buyer confirms delivery. Reputation scores are updated on-chain.

```python
import requests

API = "https://atomadic.tech"
KEY = {"X-API-Key": "YOUR_KEY", "Content-Type": "application/json"}

# Check seller's reputation before transacting
rep = requests.post(f"{API}/v1/agents/reputation",
    headers=KEY,
    json={"agent_id": "seller-agent-42"}
).json()

if rep["trust_score"] > 0.8:
    # Proceed with transaction via x402
    pass
```

**Result:** Autonomous agents trade services with mathematical trust guarantees, not blind faith.

---

## 4. Add Verified Randomness to Your Pipeline

**Problem:** Standard RNG can be predicted, replayed, or tampered with. For fair agent selection, lottery systems, or audit trails, you need provably random output.

**Solution:** Use VeriRand. Every random number comes with a cryptographic proof of fairness.

```bash
curl https://atomadic.tech/v1/rng/quantum
```

**Result:** Random output that anyone can independently verify was generated fairly.

---

## 5. Automate Regulatory Compliance

**Problem:** Your agent handles user data across jurisdictions. You need to check GDPR/CCPA compliance before every data operation, but compliance rules are complex and change frequently.

**Solution:** Gate every data operation through the Compliance Check endpoint.

```python
compliance = requests.post(f"{API}/v1/compliance/check",
    headers=KEY,
    json={
        "data_type": "user_pii",
        "jurisdiction": "EU",
        "operation": "transfer_to_us_server"
    }
).json()

if compliance["allowed"]:
    proceed_with_transfer()
else:
    log_compliance_block(compliance["reason"])
```

**Result:** Every data operation is gated by a formal compliance proof. Auditors get machine-verifiable evidence.

---

## 6. Discover and Route to Specialized Agents

**Problem:** Your orchestrator agent needs to find the best agent for a specific task, but there's no directory and no way to verify capabilities.

**Solution:** Use Agent Discovery + Topology to find agents, and Reputation to verify them.

```bash
# Register your agent
curl -X POST https://atomadic.tech/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "orchestrator-001",
    "capabilities": ["routing", "planning"]
  }'

# Discover available agents
curl https://atomadic.tech/v1/agents/topology
```

**Result:** A live, queryable topology of all registered agents with verified capabilities and trust scores.

---

## 7. Threat-Score Agent Interactions

**Problem:** Your agent receives requests from unknown agents. Some might be malicious — probing for vulnerabilities, attempting privilege escalation, or launching Sybil attacks.

**Solution:** Score every incoming interaction with the Threat Scoring endpoint before processing.

```bash
curl -X POST https://atomadic.tech/v1/threat/score \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "unknown-agent-xyz",
    "context": "requesting-admin-access"
  }'
```

**Result:** Multi-vector threat assessment (velocity, behavioral, intent) with formal bounds on false-negative rate.
