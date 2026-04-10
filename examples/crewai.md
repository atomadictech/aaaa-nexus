# CrewAI Integration — AAAA Nexus

Build CrewAI agents backed by formally verified safety tools.

## Fact-Checker Agent

```python
from crewai import Agent, Task, Crew
from crewai.tools import tool
import requests

API_BASE = "https://atomadic.tech"
API_KEY = "YOUR_KEY"


@tool("Hallucination Oracle")
def hallucination_oracle(claim: str, context: str = "general") -> str:
    """Check if a factual claim is a hallucination using a formally verified oracle.
    Returns a mathematically proved upper bound on hallucination probability."""
    resp = requests.post(
        f"{API_BASE}/v1/oracle/hallucination",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"claim": claim, "context": context},
    )
    return str(resp.json())


@tool("Threat Scanner")
def threat_scanner(agent_id: str, context: str = "general") -> str:
    """Score the threat level of an agent or data source.
    Returns multi-vector threat assessment with formal bounds."""
    resp = requests.post(
        f"{API_BASE}/v1/threat/score",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"agent_id": agent_id, "context": context},
    )
    return str(resp.json())


# Create a fact-checking agent
fact_checker = Agent(
    role="Fact Checker",
    goal="Verify all factual claims before they reach the user",
    backstory=(
        "You are a meticulous fact-checker backed by a formally verified "
        "hallucination oracle. You never let unverified claims through."
    ),
    tools=[hallucination_oracle],
    verbose=True,
)

# Create a security agent
security_agent = Agent(
    role="Security Analyst",
    goal="Assess threats from unknown agents and data sources",
    backstory=(
        "You are a security analyst with access to formally verified "
        "threat scoring. You evaluate every interaction before proceeding."
    ),
    tools=[threat_scanner],
    verbose=True,
)

# Define tasks
verify_task = Task(
    description="Verify the following claims: {claims}",
    expected_output="Verification report with hallucination bounds for each claim",
    agent=fact_checker,
)

# Run the crew
crew = Crew(
    agents=[fact_checker, security_agent],
    tasks=[verify_task],
    verbose=True,
)

result = crew.kickoff(inputs={
    "claims": "1. The Earth is 4.5 billion years old. 2. Humans have 206 bones."
})
print(result)
```
