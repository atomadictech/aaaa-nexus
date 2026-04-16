# TypeScript Integration — AAAA Nexus

Two approaches: **SDK** (recommended) or **direct HTTP**.

---

## Option 1: Official SDK (Recommended)

```bash
npm install aaaa-nexus-sdk
```

Full type coverage, automatic x402 payment handling, zero boilerplate.

### Free endpoints (no auth)

```typescript
import { NexusClient } from 'aaaa-nexus-sdk';

const nexus = new NexusClient();

const rng     = await nexus.rng.quantum();
const health  = await nexus.health();
const entropy = await nexus.oracle.entropy();

// Register agent in A2A registry
await nexus.agents.register({
  agent_id: 'ts-agent-001',
  capabilities: ['inference', 'planning'],
});

// View swarm topology
const topology = await nexus.agents.topology();
```

### With API key

```typescript
import { NexusClient } from 'aaaa-nexus-sdk';

const nexus = new NexusClient({ apiKey: process.env.NEXUS_API_KEY });

// Hallucination oracle
const hall = await nexus.oracle.hallucination({
  claim: 'The speed of light is 299,792,458 m/s',
  context: 'physics',
});
console.log(hall.hallucination_bound); // e.g. 0.003
console.log(hall.verdict);             // "likely_accurate"
console.log(hall.verified);            // true

// Threat scoring
const threat = await nexus.security.threatScore({
  payload: { query: "SELECT * FROM users WHERE '1'='1'" },
  agent_id: 'ts-agent-001',
});

// RatchetGate — CVE-2025-6514 mitigation
const session = await nexus.ratchet.register({
  session_id: crypto.randomUUID(),
  agent_id: 'ts-agent-001',
});
await nexus.ratchet.advance({
  session_id: session.session_id,
  key_id: session.key_id,
});

// Chat inference with hallucination guard
const response = await nexus.inference.chat({
  messages: [{ role: 'user', content: 'Explain formal verification' }],
  hallucination_guard: true,
});

// EU AI Act compliance check
const compliance = await nexus.compliance.euAiAct({
  system_id: 'my-model-prod',
  risk_category: 'high_risk',
  intended_purpose: 'credit_scoring',
});

// DeFi — LP optimization
const lp = await nexus.defi.optimize({
  protocol: 'uniswap_v3',
  position: { token_a: 'ETH', token_b: 'USDC', amount_usd: 50_000 },
  risk_tolerance: 'medium',
});
```

### x402 autonomous payments

```typescript
import { NexusClient } from 'aaaa-nexus-sdk';

const nexus = new NexusClient({
  x402: {
    getProof: async (challenge) => {
      // challenge = { amount, amountUsd, treasury, chainId, token, endpoint }
      const txHash = await myWallet.sendUsdc({
        to: challenge.treasury,
        amount: challenge.amount,   // micro-USDC
        chainId: challenge.chainId, // 8453 = Base L2
      });
      return txHash;
    },
  },
});

// SDK automatically: call → 402 → getProof() → retry with X-Payment header
const score = await nexus.trust.score({ agent_id: 'did:key:z6Mk...' });
```

### Error handling

```typescript
import { NexusClient, NexusError } from 'aaaa-nexus-sdk';

try {
  const result = await nexus.oracle.hallucination({ claim: '...' });
} catch (err) {
  if (err instanceof NexusError) {
    console.error(err.status);  // 429
    console.error(err.code);    // "rate_limit_exceeded"
    console.error(err.message); // "Trial limit reached — add API key or use x402"
  }
}
```

### Streaming inference

```typescript
const stream = await nexus.inference.stream({
  messages: [{ role: 'user', content: 'Write a haiku about formal proofs' }],
});

const reader = stream.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```

---

## Option 2: Direct HTTP (No SDK)

If you prefer raw fetch without installing anything:

```typescript
const API_BASE = "https://atomadic.tech";
const API_KEY  = process.env.NEXUS_API_KEY!;

async function nexus<T>(path: string, body?: object): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`, {
    method: body ? "POST" : "GET",
    headers: {
      "Content-Type": "application/json",
      ...(API_KEY ? { "X-API-Key": API_KEY } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!resp.ok) throw new Error(`${resp.status} ${await resp.text()}`);
  return resp.json();
}

// Free
const rng = await nexus<{ random: number }>("/v1/rng/quantum");

// Paid
const threat = await nexus("/v1/threat/score", {
  payload: { query: "user input here" },
  agent_id: "ts-agent-001",
});
```

---

## MCP Client Integration

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const transport = new StreamableHTTPClientTransport(
  new URL("https://atomadic.tech/mcp")
);
const client = new Client({ name: "my-app", version: "1.0.0" });
await client.connect(transport);

const tools = await client.listTools();
console.log("Available tools:", tools.tools.map(t => t.name));

const result = await client.callTool({ name: "health", arguments: {} });
```

---

## A2A Protocol Integration

```typescript
import { NexusClient } from 'aaaa-nexus-sdk';

const nexus = new NexusClient();

// Discover agent capabilities
const card = await nexus.a2a.agentCard();
console.log("Skills:", card.skills.map(s => s.id));

// Send A2A message
const response = await nexus.a2a.send({
  jsonrpc: "2.0",
  method: "message/send",
  params: {
    message: {
      role: "user",
      parts: [{ type: "text", text: "Check system health" }],
    },
  },
  id: "1",
});
```

---

## Resources

| Resource | Link |
|----------|------|
| SDK on npm | [npmjs.com/package/aaaa-nexus-sdk](https://www.npmjs.com/package/aaaa-nexus-sdk) |
| API reference | [API_REFERENCE.md](../API_REFERENCE.md) |
| Pricing | [docs/PRICING.md](../docs/PRICING.md) |
| Get API key | https://atomadic.tech/pay |
