# TypeScript Integration — AAAA Nexus API

## Direct HTTP (No SDK)

```typescript
const API_BASE = "https://aaaa-nexus.atomadictech.workers.dev";

// Health check
const health = await fetch(`${API_BASE}/health`).then(r => r.json());
console.log(health);

// Entropy oracle (free)
const entropy = await fetch(`${API_BASE}/v1/oracle/entropy`).then(r => r.json());
console.log(entropy);

// Quantum RNG (free)
const rng = await fetch(`${API_BASE}/v1/rng/quantum`).then(r => r.json());
console.log(rng);

// Register agent (free)
const agent = await fetch(`${API_BASE}/v1/agents/register`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    agent_id: "ts-agent-001",
    capabilities: ["inference", "planning"],
  }),
}).then(r => r.json());
console.log(agent);
```

## With API Key

```typescript
const API_KEY = process.env.AAAA_NEXUS_API_KEY!;

async function nexusPost(path: string, body: object) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

// Hallucination oracle
const hallCheck = await nexusPost("/v1/oracle/hallucination", {
  claim: "The speed of light is 299,792,458 m/s",
  context: "physics",
});
console.log(hallCheck);

// Threat scoring
const threat = await nexusPost("/v1/threat/score", {
  agent_id: "ts-agent-001",
  context: "financial-transaction",
});
console.log(threat);

// Chat inference with hallucination guard
const inference = await nexusPost("/v1/inference", {
  messages: [{ role: "user", content: "Explain formal verification" }],
});
console.log(inference);
```

## MCP Client Integration

```typescript
// For Claude Desktop or Cursor, add to your MCP config:
// {
//   "mcpServers": {
//     "aaaa-nexus": {
//       "url": "https://aaaa-nexus.atomadictech.workers.dev/mcp"
//     }
//   }
// }

// For programmatic MCP access:
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const transport = new StreamableHTTPClientTransport(
  new URL("https://aaaa-nexus.atomadictech.workers.dev/mcp")
);

const client = new Client({ name: "my-app", version: "1.0.0" });
await client.connect(transport);

const tools = await client.listTools();
console.log("Available tools:", tools.tools.map(t => t.name));

// Call a tool
const result = await client.callTool({
  name: "health",
  arguments: {},
});
console.log(result);
```

## A2A Protocol Integration

```typescript
// Discover the agent
const agentCard = await fetch(
  `${API_BASE}/.well-known/agent.json`
).then(r => r.json());
console.log("Agent capabilities:", agentCard);

// Send A2A message
const a2aResult = await fetch(`${API_BASE}/a2a`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    method: "message/send",
    params: {
      message: {
        role: "user",
        parts: [{ type: "text", text: "Check system health" }],
      },
    },
    id: "1",
  }),
}).then(r => r.json());
console.log(a2aResult);
```
