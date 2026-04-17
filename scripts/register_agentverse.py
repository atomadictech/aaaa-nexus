#!/usr/bin/env python3
"""
Register AAAA-Nexus on Agentverse (Fetch.ai agent marketplace).

Usage:
  export AGENTVERSE_KEY=<your-key>
  export AGENT_SEED_PHRASE=<your-seed>
  python scripts/register_agentverse.py
"""
import os
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)

register_chat_agent(
    "AAAA-Nexus",
    "https://atomadic.tech/.well-known/agent.json",
    active=True,
    credentials=RegistrationRequestCredentials(
        agentverse_api_key=os.environ["AGENTVERSE_KEY"],
        agent_seed_phrase=os.environ["AGENT_SEED_PHRASE"],
    ),
)
