---
name: Bug Report
about: Report an API endpoint behaving differently than documented
title: "[BUG] "
labels: bug
assignees: ''
---

**Endpoint**
Which endpoint is affected? (e.g., `POST /v1/oracle/hallucination`)

**Expected behavior**
What should happen according to the docs?

**Actual behavior**
What actually happens? Include the HTTP status code and response body.

**Steps to reproduce**
```bash
curl -X POST https://aaaa-nexus.atomadictech.workers.dev/... \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Authentication method**
- [ ] API Key
- [ ] x402 USDC
- [ ] None (free endpoint)

**Additional context**
Any other details, timestamps, or error messages.
