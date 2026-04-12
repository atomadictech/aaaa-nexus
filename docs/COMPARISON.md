# How Atomadic Compares

## Verification Method

| Approach | Atomadic | Benchmark-Based Tools | Heuristic Guardrails |
|----------|-----------|----------------------|---------------------|
| **Safety guarantee** | Mathematical proof | Statistical confidence | Rule-based heuristic |
| **Coverage** | All possible inputs | Sampled test cases | Known patterns only |
| **False negatives** | Formally bounded | Unknown | Unknown |
| **Proof artifact** | Machine-checked (Lean 4) | None | None |
| **Can be wrong?** | No (within proved scope) | Yes | Yes |

## Feature Comparison

| Feature | Atomadic | Typical Safety API | Generic LLM API |
|---------|-----------|-------------------|-----------------|
| **Formal verification** | Yes | No | No |
| **Hallucination detection** | Proved upper bound | Confidence score | None |
| **Session security** | RatchetGate (proved) | Token-based | Token-based |
| **Agent identity** | Sybil-resistant (proved) | API key only | API key only |
| **Payment model** | x402 autonomous + API key | Subscription | Subscription |
| **MCP support** | Native | Varies | Varies |
| **A2A protocol** | Native (Google A2A) | No | No |
| **Agent registry** | Built-in | No | No |
| **Delegation limits** | Formally bounded | None | None |
| **Compliance gates** | Formal proof | Checklist | None |

## Payment Model

| Model | Atomadic | Traditional APIs |
|-------|-----------|-----------------|
| **No-signup option** | Yes (x402) | No |
| **Agent-autonomous payments** | Yes | No |
| **Pay-per-call** | Yes ($0.002+) | Varies |
| **Credit packs** | Yes ($4/$15/$49) | Varies |
| **Free tier** | Yes (several endpoints) | Varies |
| **Crypto payments** | USDC on 3 chains | No |

## Protocol Support

| Protocol | Atomadic | Others |
|----------|-----------|--------|
| **REST** | Yes | Yes |
| **MCP** | Native server | Plugin/adapter |
| **Google A2A** | Native | Rare |
| **x402** | Native | No |
| **OpenAPI** | Full spec served | Varies |

## When to Use Atomadic

- You need **mathematical certainty**, not statistical confidence
- Your agents operate **autonomously** and need to pay for services without humans
- You're building **multi-agent systems** that need identity, trust, and coordination
- You need **compliance proofs** that auditors can verify
- You want **one API** for safety, payments, identity, and communication
