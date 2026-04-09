# Glossary — AAAA Nexus

## A2A Protocol
Agent-to-Agent protocol (created by Google) enabling direct communication between autonomous agents. Includes agent cards for capability discovery and standardized message passing.

## Agent Card
A JSON manifest at `/.well-known/agent.json` describing an agent's capabilities, supported protocols, and contact endpoints. Part of the A2A standard.

## Byzantine Fault
A failure mode where a component in a distributed system behaves arbitrarily — including maliciously. Formally verified systems can provably resist Byzantine agents.

## Epoch
A time-bounded window used by the entropy oracle. Each epoch provides fresh entropy data. Used for zero-RTT handshakes and session synchronization.

## Formal Verification
The use of mathematical proofs, checked by a computer, to guarantee that a system satisfies its specification under all possible inputs and conditions. Unlike testing, which checks specific cases, formal verification covers the entire state space.

## HELIX Compression
AAAA Nexus's tensor compression system, achieving up to 83% size reduction while preserving data integrity.

## Lean 4
A programming language and interactive theorem prover used to write machine-checked mathematical proofs. AAAA Nexus uses Lean 4 to formally verify all safety claims.

## MCP (Model Context Protocol)
A protocol for connecting AI models to external tools and data sources. AAAA Nexus provides an MCP server that exposes its tools to Claude, Cursor, and other MCP-compatible clients.

## Ratchet (Cryptographic)
A cryptographic mechanism where keys advance forward irreversibly. Once a session key ratchets forward, previous keys cannot be recovered — providing forward secrecy.

## RatchetGate
AAAA Nexus's session re-keying protocol. Uses a cryptographic ratchet with a formally proved re-key window to prevent session fixation and replay attacks.

## `sorry`
In Lean 4, `sorry` is a placeholder for an incomplete proof. A proof with zero `sorry` means every claim is fully machine-checked.

## Sybil Attack
An attack where a single entity creates many fake identities to gain disproportionate influence. AAAA Nexus's Topological Identity system uses formally proved depth limits to resist Sybil attacks.

## VeriRand
AAAA Nexus's verified randomness service. Produces quantum-sourced random numbers with cryptographic proofs of fairness and non-tampering.

## x402
An HTTP-native micropayment protocol using the HTTP 402 (Payment Required) status code. Enables autonomous machine-to-machine payments without accounts, API keys, or human intervention.

## USDC
USD Coin — a stablecoin pegged 1:1 to the US dollar. Used by AAAA Nexus for x402 payments on Base L2, Polygon, and Solana.

## Zero-RTT Handshake
A connection establishment method that requires zero round-trips before data exchange. The entropy oracle enables this by providing shared epoch data.
