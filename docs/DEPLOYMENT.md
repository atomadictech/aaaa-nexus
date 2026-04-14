# AAAA Nexus — Deployment Guide

This guide covers configuration, health verification, and monitoring for AAAA Nexus deployments. Implementation internals are proprietary and not covered here.

---

## Prerequisites

You will need accounts and credentials for the following services before deploying:

| Service | Purpose | Required |
|---------|---------|----------|
| **Stripe** | Payment processing (cards, Apple Pay, Google Pay) | Yes (payments) |
| **Resend** | Transactional email (API key delivery) | Yes (payments) |
| **Base L2 RPC** | USDC on-chain verification | Yes (x402) |
| **USDC treasury wallet** | Receive x402 payments | Yes (x402) |

---

## Required Secrets

Configure the following environment variables / secrets before deployment:

### Stripe

| Variable | Description | Example |
|----------|-------------|---------|
| `STRIPE_SECRET_KEY` | Stripe secret key (live mode) | `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret from Stripe Dashboard | `whsec_...` |

**Setup steps:**
1. Create a Stripe account at https://stripe.com
2. Go to Developers → API Keys → copy your live secret key
3. Go to Developers → Webhooks → Add endpoint: `https://YOUR_DOMAIN/v1/webhooks/stripe`
4. Subscribe to events: `checkout.session.completed`, `payment_intent.succeeded`
5. Copy the signing secret

### Resend (Email)

| Variable | Description | Example |
|----------|-------------|---------|
| `RESEND_API_KEY` | Resend API key | `re_...` |
| `RESEND_FROM_EMAIL` | Verified sender address | `keys@yourdomain.com` |

**Setup steps:**
1. Create a Resend account at https://resend.com
2. Verify your sending domain (add DNS records)
3. Create an API key with send permissions

### x402 / Base L2

| Variable | Description | Example |
|----------|-------------|---------|
| `BASE_RPC_URL` | Base L2 RPC endpoint | `https://mainnet.base.org` |
| `TREASURY_ADDRESS` | USDC recipient address on Base | `0x...` |
| `USDC_CONTRACT` | USDC contract on Base L2 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

### Admin

| Variable | Description |
|----------|-------------|
| `ADMIN_TOKEN` | Owner token for `/v1/admin/*` endpoints |
| `OWNER_EMAIL` | Email for admin notifications |

---

## Stripe Price Catalog Bootstrap

After deploying with Stripe credentials, initialize your price catalog:

```bash
# Bootstrap credit pack prices in Stripe
curl -X POST https://YOUR_DOMAIN/v1/admin/stripe/bootstrap \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN"
```

This creates the following products in your Stripe account:

| Product | Price | Metadata |
|---------|-------|----------|
| API Credits — Starter | $8 (500 calls) | `product_type: api_credits` |
| API Credits — Standard | $15 (2,500 calls) | `product_type: api_credits` |
| API Credits — Pro | $49 (10,000 calls) | `product_type: api_credits` |

Verify prices were created:

```bash
curl https://YOUR_DOMAIN/v1/payments/stripe/prices | jq '.prices[] | {nickname, unit_amount}'
```

---

## Health Check Procedure

Run this sequence after every deployment to verify all systems are operational:

### 1. Basic health

```bash
curl https://YOUR_DOMAIN/health | jq .
```

Expected:
```json
{
  "status": "ok",
  "version": "0.5.0",
  "epoch": ...,
  "helix": {
    "anti_hallucination": true,
    "ecc_status": true,
    "integrity_parity": true
  }
}
```

Failure indicators:
- `status` is not `"ok"` → check subsystem logs
- `helix.ecc_status: false` → ECC subsystem degraded
- `helix.anti_hallucination: false` → Hallucination guard offline

### 2. Free endpoint smoke test

```bash
# RNG
curl https://YOUR_DOMAIN/v1/rng/quantum | jq .

# Verify
curl https://YOUR_DOMAIN/v1/rng/verify | jq '.valid'

# Entropy oracle
curl https://YOUR_DOMAIN/v1/oracle/entropy | jq '{epoch, window_s}'

# Metrics
curl https://YOUR_DOMAIN/v1/metrics | jq '{endpoints, product_families}'
```

### 3. Payment gate verification

```bash
# Verify payment gate is active (should return 402 or 401)
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' \
  -X POST https://YOUR_DOMAIN/v1/oracle/hallucination \
  -H "Content-Type: application/json" \
  -d '{"claim":"test","context":"health-check"}')

echo "Payment gate: HTTP $HTTP_CODE (expected: 402 or 401)"
```

### 4. Admin panel verification

```bash
# Verify admin endpoints are accessible
curl https://YOUR_DOMAIN/v1/admin/keys \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN" | jq length

curl https://YOUR_DOMAIN/v1/admin/revenue \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN" | jq .
```

### 5. Stripe webhook verification

Check that the webhook endpoint is reachable from Stripe:

```bash
# Go to Stripe Dashboard → Developers → Webhooks → your endpoint
# Click "Send test event" → checkout.session.completed
# Then check the webhook log:
curl https://YOUR_DOMAIN/v1/admin/webhook-log \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN" | jq '.[0]'
```

### 6. A2A discovery verification

```bash
curl https://YOUR_DOMAIN/.well-known/agent.json | jq '{name, version, skills: [.skills[] | .id]}'
```

---

## Automated Verification

Run the full verification suite from the repository:

```bash
git clone https://github.com/atomadictech/aaaa-nexus.git
cd aaaa-nexus

# Override base URL to test your deployment
API_BASE="https://YOUR_DOMAIN" ./verify.sh

# Run with verbose output
API_BASE="https://YOUR_DOMAIN" ./verify.sh --verbose
```

All checks must pass before considering a deployment healthy.

---

## Monitoring Setup

### Key metrics to monitor

| Metric | Endpoint | Alert condition |
|--------|----------|-----------------|
| API health | `GET /health` | `status != "ok"` |
| ECC status | `GET /health` | `helix.ecc_status == false` |
| Epoch progression | `GET /health` | `epoch` stops incrementing |
| Webhook delivery | `GET /v1/admin/webhook-log` | Failed entries accumulate |
| Payment DLQ | `GET /v1/marketing/dlq` | Queue depth > 0 |

### Recommended monitoring checks (cron)

```bash
#!/usr/bin/env bash
# Add to cron: */5 * * * * /path/to/monitor.sh

API="https://YOUR_DOMAIN"
ADMIN_TOKEN="YOUR_ADMIN_TOKEN"

STATUS=$(curl -sf --max-time 5 "$API/health" | jq -r '.status // "unreachable"')

if [ "$STATUS" != "ok" ]; then
  echo "ALERT: API status is $STATUS at $(date)" | mail -s "AAAA Nexus Alert" ops@yourdomain.com
fi

# Check webhook DLQ
DLQ_DEPTH=$(curl -sf --max-time 5 "$API/v1/marketing/dlq" \
  -H "X-Admin-Token: $ADMIN_TOKEN" | jq 'length // 0')

if [ "$DLQ_DEPTH" -gt 0 ]; then
  echo "ALERT: $DLQ_DEPTH items in webhook DLQ" | mail -s "DLQ Alert" ops@yourdomain.com
fi
```

### Epoch-based circuit breaker

The system uses ~102-second epoch windows for circuit breaker state transitions. The `next_epoch_in_s` field in `/health` tells you the maximum recovery latency:

```bash
NEXT=$(curl -sf https://YOUR_DOMAIN/health | jq -r '.next_epoch_in_s')
echo "Circuit breaker re-evaluates in ${NEXT}s (max 102s)"
```

If a subsystem degrades, it will recover within one epoch of the underlying issue being resolved.

---

## Webhook Failure Recovery

If Stripe webhooks fail to deliver (network issues, deployment downtime), use the admin webhook log and Stripe's retry mechanism:

### Check failed webhooks

```bash
curl https://YOUR_DOMAIN/v1/admin/webhook-log \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN" | jq '.[] | select(.status == "failed")'
```

### Replay from Stripe Dashboard

1. Go to Stripe Dashboard → Developers → Webhooks → your endpoint
2. Click on a failed event
3. Click "Resend" to replay it

### Check marketing DLQ

```bash
curl https://YOUR_DOMAIN/v1/marketing/dlq \
  -H "X-Admin-Token: YOUR_ADMIN_TOKEN" | jq .
```

Items in the DLQ are failed fulfillment attempts. Each entry includes the original Stripe event for manual review.

---

## Post-Deployment Checklist

- [ ] `GET /health` returns `status: "ok"`
- [ ] `GET /v1/metrics` returns expected endpoint count
- [ ] `GET /v1/rng/quantum` returns a value
- [ ] `POST /v1/oracle/hallucination` (no auth) returns HTTP 402
- [ ] `GET /v1/payments/stripe/prices` returns credit pack prices
- [ ] Test Stripe checkout flow end-to-end
- [ ] Confirm API key email delivery works
- [ ] `GET /v1/admin/webhook-log` accessible with admin token
- [ ] `GET /.well-known/agent.json` returns agent card
- [ ] `./verify.sh` passes all checks

---

## Security Recommendations

- Rotate `ADMIN_TOKEN` on a regular schedule
- Set webhook signing secret in Stripe — never accept unsigned webhooks
- Use HTTPS exclusively — all endpoints enforce TLS
- Review `/v1/admin/webhook-log` weekly for anomalies
- Monitor DLQ depth daily — non-zero depth requires investigation

---

*Deployment Guide — AAAA Nexus v0.5.0 — April 2026*
