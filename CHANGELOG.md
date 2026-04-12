# Changelog

All notable changes to the Atomadic API are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.5.0] — 2026-04-08

### Added
- 119+ production endpoints across 30 product families
- Hallucination Oracle with formally verified upper bounds
- RatchetGate session re-keying (mitigates session fixation attacks)
- VeriRand quantum RNG with cryptographic proofs
- Trust Phase Oracle with mathematical trust ceiling
- Topological Identity for Sybil-resistant agent verification
- AAAA Shield post-quantum session security
- Agent Discovery, SLA Engine, Escrow, and Reputation Ledger (A2A Economy Stack)
- x402 USDC micropayments on Base L2, Polygon, and Solana
- Google A2A protocol support (agent card, SendMessage, GetTask)
- MCP server for Claude Desktop, Claude Code, and Cursor
- Chat inference and streaming inference with hallucination guard
- Text summarization and sentiment analysis
- Agent goal planner and intent classification
- GDPR/CCPA compliance check endpoint
- Multi-vector threat scoring
- HELIX tensor compression
- Agent registration and swarm topology
- OpenAPI specification at /openapi.json
- Credit pack billing ($4 / $15 / $49)
- API key authentication via /pay

### Security
- All safety claims formally verified in Lean 4 (zero `sorry`, zero axioms)
- Session security mathematically proved by construction

## [0.4.0] — 2026-03-15

### Added
- Entropy epoch oracle for zero-RTT handshakes
- Agent swarm relay and inbox polling
- Streaming inference with chain-of-thought

### Changed
- Improved hallucination oracle response time to sub-50ms

## [0.3.0] — 2026-02-20

### Added
- x402 payment protocol integration
- Multi-chain USDC support (Base L2 + Polygon)
- Credit pack purchasing at /pay

## [0.2.0] — 2026-01-10

### Added
- Core API endpoints (health, RNG, entropy)
- Agent registration and topology queries
- Initial MCP server support

## [0.1.0] — 2025-12-01

### Added
- Initial API deployment
- Formal verification framework established
- Basic hallucination detection
