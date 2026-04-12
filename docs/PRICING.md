# Pricing & Billing — Atomadic

Transparent, pay-as-you-go pricing. Generous free tier. No hidden fees.

## Free Tier

No signup required for free endpoints:

| Endpoint | Cost | Rate Limit |
|----------|------|------------|
| Health check | Free | Unlimited |
| Entropy oracle | Free | Unlimited |
| Quantum RNG | Free | Unlimited |
| Agent registration | Free | Unlimited |
| Agent topology | Free | Unlimited |
| Swarm inbox | Free | Unlimited |

## Per-Call Pricing (Paid Endpoints)

Pay only for what you use — via API key credits or x402 USDC.

| Endpoint | Price |
|----------|-------|
| Hallucination Oracle | $0.002 |
| RatchetGate Register | $0.002 |
| RatchetGate Advance | $0.002 |
| Threat Scoring | $0.003 |
| Compliance Check | $0.005 |
| Intent Classification | $0.005 |
| Sentiment Analysis | $0.005 |
| Text Summarization | $0.010 |
| Agent Reputation | $0.010 |
| Chat Inference | $0.015 |
| Agent Planner | $0.015 |
| Identity Verification | $0.020 |
| Streaming Inference | $0.025 |

## Credit Packs

Buy credits once. Use across all endpoints. Credits never expire.

| Pack | Cost | Calls | Per Call |
|------|------|-------|----------|
| **Starter** | $4 | 500 | $0.008 |
| **Value** | $15 | 2,000 | $0.0075 |
| **Bulk** | $49 | 7,500 | $0.0065 |

Purchase at: https://atomadic.tech/pay

## x402 Autonomous Payments

No signup. No API key. Agents pay directly with USDC.

**How it works:**
1. Call any paid endpoint without credentials
2. Receive HTTP 402 with payment details (amount, treasury address, chain)
3. Send USDC on Base L2 / Polygon / Solana
4. Retry request with payment proof header
5. Get result

**Advantages:**
- Zero signup friction
- Agents pay autonomously
- Same per-call prices as credit packs
- No rate limits — pay for what you use

## Supported Payment Chains

| Chain | Notes |
|-------|-------|
| **Base L2** | Recommended — lowest fees |
| **Polygon** | Supported |
| **Solana** | Supported |

## FAQ

**Do credits expire?** No.

**Can I get a refund?** 14-day refund policy. Email atomadic@proton.me.

**Is there an enterprise tier?** Yes — custom limits, SLAs, dedicated support. Contact atomadic@proton.me.

**What happens when credits run out?** Paid endpoints return 402. Free endpoints continue working.
