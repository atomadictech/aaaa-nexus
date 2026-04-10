# AutoGen Integration — AAAA Nexus

Use AAAA Nexus in AutoGen multi-agent conversations.

## Function Definitions

```python
import requests
from autogen import AssistantAgent, UserProxyAgent

API_BASE = "https://atomadic.tech"
API_KEY = "YOUR_KEY"


def check_hallucination(claim: str, context: str = "general") -> dict:
    """Verify a factual claim using the formally verified hallucination oracle."""
    resp = requests.post(
        f"{API_BASE}/v1/oracle/hallucination",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"claim": claim, "context": context},
    )
    return resp.json()


def register_agent(agent_id: str, capabilities: list) -> dict:
    """Register an agent in the AAAA Nexus swarm topology."""
    resp = requests.post(
        f"{API_BASE}/v1/agents/register",
        headers={"Content-Type": "application/json"},
        json={"agent_id": agent_id, "capabilities": capabilities},
    )
    return resp.json()


def get_topology() -> dict:
    """Query the live agent swarm topology."""
    resp = requests.get(f"{API_BASE}/v1/agents/topology")
    return resp.json()


def get_verified_random() -> dict:
    """Get a cryptographically verified random number."""
    resp = requests.get(f"{API_BASE}/v1/rng/quantum")
    return resp.json()
```

## AutoGen Agent Setup

```python
# Define the function map
function_map = {
    "check_hallucination": check_hallucination,
    "register_agent": register_agent,
    "get_topology": get_topology,
    "get_verified_random": get_verified_random,
}

# LLM config with function calling
llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": "..."}],
    "functions": [
        {
            "name": "check_hallucination",
            "description": "Verify a factual claim using formally verified oracle",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string", "description": "The claim to verify"},
                    "context": {"type": "string", "description": "Domain context"},
                },
                "required": ["claim"],
            },
        },
        {
            "name": "register_agent",
            "description": "Register agent in the AAAA Nexus swarm",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "capabilities": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["agent_id", "capabilities"],
            },
        },
        {
            "name": "get_topology",
            "description": "Query the live agent swarm topology",
            "parameters": {"type": "object", "properties": {}},
        },
        {
            "name": "get_verified_random",
            "description": "Get cryptographically verified random number",
            "parameters": {"type": "object", "properties": {}},
        },
    ],
}

# Create agents
assistant = AssistantAgent(
    name="safety_assistant",
    system_message=(
        "You are an AI safety assistant with access to AAAA Nexus tools. "
        "Always verify factual claims using check_hallucination before "
        "presenting them as facts."
    ),
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    function_map=function_map,
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Register our agent, check the swarm topology, and verify: 'Python was created in 1991'",
)
```

## Multi-Agent Topology Discovery

```python
# First register all your AutoGen agents
for agent_name in ["researcher", "coder", "reviewer"]:
    register_agent(
        agent_id=f"autogen-{agent_name}",
        capabilities=["autogen", agent_name],
    )

# Discover other agents in the swarm
topology = get_topology()
print(f"Swarm has {topology['agents']} registered agents")
```
