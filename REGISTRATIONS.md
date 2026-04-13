# AAAA Nexus — Registry & Listing Tracker

Track of everywhere AAAA Nexus is registered, submitted, or listed.
Update this file whenever a new registration is made or a status changes.

Last updated: 2026-04-12

---

## Own Infrastructure

| Asset | URL | Status | Notes |
|-------|-----|--------|-------|
| Live API | https://atomadic.tech | ✅ Live | Cloudflare Workers, v0.5.1 |
| GitHub Repo | https://github.com/atomadictech/aaaa-nexus | ✅ Public | Primary marketing/docs repo |
| OpenAPI Spec | https://atomadic.tech/openapi.json | ✅ Live | Machine-readable endpoint catalog |
| A2A Agent Card | https://atomadic.tech/.well-known/agent.json | ✅ Live | Google A2A protocol |
| MCP Endpoint | https://atomadic.tech/mcp | ✅ Live | Claude Desktop, Claude Code, Cursor |
| llms.txt | https://atomadic.tech/llms.txt | ✅ Live | LLM-readable API summary |
| Sitemap | https://atomadic.tech/sitemap.xml | ✅ Live | Crawler discovery |
| robots.txt | https://atomadic.tech/robots.txt | ✅ Live | Allows all crawlers |

---

## Agent / AI Protocol Registries

| Registry | URL | Status | Submitted | Notes |
|----------|-----|--------|-----------|-------|
| Google A2A Protocol | https://google.github.io/A2A | ✅ Self-hosted | 2026-04-08 | agent.json at /.well-known/agent.json |
| MCP Server Directory | https://modelcontextprotocol.io | ⏳ Pending | — | Submit via PR to MCP registry |
| Smithery.ai | https://smithery.ai | ⏳ Pending | — | MCP server marketplace |
| Glama.ai | https://glama.ai | ⏳ Pending | — | MCP + agent discovery |

---

## API Marketplaces

| Registry | URL | Status | Submitted | Notes |
|----------|-----|--------|-----------|-------|
| RapidAPI | https://rapidapi.com | ⏳ Pending | — | Largest API marketplace |
| APIs.guru | https://apis.guru | ⏳ Pending | — | OpenAPI directory — submit via PR |
| PublicAPIs.dev | https://publicapis.dev | ⏳ Pending | — | Submit via GitHub PR |
| Any-API | https://any-api.com | ⏳ Pending | — | Free API directory |
| Postman API Network | https://www.postman.com/explore | ⏳ Pending | — | Needs Postman collection |

---

## AI / Agent Frameworks (Integration Listings)

| Platform | URL | Status | Notes |
|----------|-----|--------|-------|
| LangChain Hub | https://smith.langchain.com | ⏳ Pending | List as tool integration |
| AutoGen | https://microsoft.github.io/autogen | ⏳ Pending | Example integration PR |
| CrewAI Tools | https://docs.crewai.com | ⏳ Pending | Custom tool listing |
| Composio | https://composio.dev | ⏳ Pending | API connector submission |
| Toolhouse | https://toolhouse.ai | ⏳ Pending | Tool registration |

---

## DeFi / Web3 Registries

| Registry | URL | Status | Notes |
|----------|-----|--------|-------|
| DeFiLlama | https://defillama.com | ⏳ Pending | List as DeFi oracle/tool |
| DeBank | https://debank.com | ⏳ Pending | Protocol listing |
| x402.org | https://x402.org | ⏳ Pending | x402 payment protocol directory |

---

## AI Safety / Compliance Directories

| Registry | URL | Status | Notes |
|----------|-----|--------|-------|
| EU AI Act Registry | https://huggingface.co/eu-ai-act | ⏳ Pending | EU compliance tooling directory |
| AI Safety Index | — | ⏳ Pending | Research/submit opportunities |
| NIST AI RMF Resource Center | https://airc.nist.gov | ⏳ Pending | Tool listing for AI governance |

---

## Developer Communities

| Platform | URL | Status | Notes |
|----------|-----|--------|-------|
| Hacker News (Show HN) | https://news.ycombinator.com | ⏳ Pending | Show HN post for launch |
| Product Hunt | https://producthunt.com | ⏳ Pending | Product launch |
| dev.to | https://dev.to | ⏳ Pending | Technical article / integration guide |
| Reddit r/MachineLearning | https://reddit.com/r/MachineLearning | ⏳ Pending | Launch post |
| Reddit r/ethereum | https://reddit.com/r/ethereum | ⏳ Pending | DeFi suite announcement |

---

## How to Update This File

When registering somewhere new:
1. Add a row with ⏳ Pending and the date submitted
2. Update to ✅ Live once confirmed active
3. Add notes on any API keys, account usernames, or special config needed (store secrets in vault, not here)
