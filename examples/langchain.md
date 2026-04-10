# LangChain Integration — AAAA Nexus

Use AAAA Nexus endpoints as LangChain tools in your agent chains.

## Hallucination Oracle Tool

```python
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
import requests

API_BASE = "https://atomadic.tech"
API_KEY = "YOUR_KEY"


def check_hallucination(claim: str, context: str = "general") -> str:
    """Check if a claim is a hallucination using formally verified oracle."""
    resp = requests.post(
        f"{API_BASE}/v1/oracle/hallucination",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"claim": claim, "context": context},
    )
    return resp.json()


hallucination_tool = StructuredTool.from_function(
    func=check_hallucination,
    name="hallucination_oracle",
    description=(
        "Verify if a factual claim is a hallucination. "
        "Returns a formally proved upper bound on hallucination probability. "
        "Use this before acting on critical factual claims."
    ),
)
```

## VeriRand Tool

```python
def get_verified_random() -> str:
    """Get a cryptographically verified random number."""
    resp = requests.get(f"{API_BASE}/v1/rng/quantum")
    return resp.json()


verirand_tool = StructuredTool.from_function(
    func=get_verified_random,
    name="verirand",
    description=(
        "Generate a cryptographically verified random number. "
        "Each output includes a proof of fairness."
    ),
)
```

## Threat Scoring Tool

```python
def score_threat(agent_id: str, context: str = "general") -> str:
    """Score the threat level of an agent interaction."""
    resp = requests.post(
        f"{API_BASE}/v1/threat/score",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"agent_id": agent_id, "context": context},
    )
    return resp.json()


threat_tool = StructuredTool.from_function(
    func=score_threat,
    name="threat_scorer",
    description=(
        "Assess the threat level of an agent or interaction. "
        "Returns multi-vector threat score with formal bounds."
    ),
)
```

## Using in an Agent Chain

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
tools = [hallucination_tool, verirand_tool, threat_tool]

# Create agent with AAAA Nexus tools
agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({
    "input": "Is it true that water boils at 100°C at sea level? Verify this claim."
})
```

## LangChain + MCP (Alternative)

If you're using LangChain with MCP support, you can connect directly:

```python
# Add AAAA Nexus as MCP server in your LangChain MCP config
# All tools become available automatically
```
