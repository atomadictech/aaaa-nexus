# Changelog

All notable changes to the AAAA Nexus API are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [1.0.0] — 2026-04-16

### Added
- **Official TypeScript SDK** — `aaaa-nexus-sdk@1.0.0` published to npm
  - Full type coverage for all 102 endpoints
  - Automatic x402 USDC payment handling (402 → pay → retry, zero boilerplate)
  - CJS + ESM dual-module output with TypeScript declarations
  - `NexusClient` with named resource namespaces: `oracle`, `trust`, `ratchet`, `security`, `identity`, `agents`, `escrow`, `reputation`, `sla`, `a2a`, `defi`, `vrf`, `compliance`, `drift`, `text`, `rng`, `payments`, `inference`
  - Install: `npm install aaaa-nexus-sdk`
  - Docs: [npmjs.com/package/aaaa-nexus-sdk](https://www.npmjs.com/package/aaaa-nexus-sdk)

## [0.5.1] — 2026-04-12

### Added
- **DeFi Suite** — 9 formally verified DeFi endpoints:
  - `/v1/defi/optimize` — LP parameter optimization (DFP-100-OptimalTick theorem)
  - `/v1/defi/risk-score` — Formally bounded risk scoring (DFI-101, max drawdown ≤12.5%)
  - `/v1/defi/oracle-verify` — Oracle manipulation detection (OGD-100-ManipulationBound)
  - `/v1/defi/liquidation-check` — Pre-liquidation health check (LQS-100-LiquidationBound)
  - `/v1/defi/bridge-verify` — Cross-chain bridge integrity (BRP-100-BridgeIntegrity)
  - `/v1/defi/contract-audit` — Smart contract audit certificate (CVR-100-AuditBound)
  - `/v1/defi/yield-optimize` — Optimal yield allocation (YLD-100-YieldConvergence)
  - `/v1/vrf/draw` — On-chain verifiable randomness for gaming/lotteries (VRF-100)
  - `/v1/vrf/verify-draw` — Player-verifiable draw proof retrieval (VRF-101)
- **Compliance Suite** — 12 formally verified compliance endpoints:
  - `/v1/compliance/check` — Multi-framework check (EU AI Act + NIST RMF + ISO 42001)
  - `/v1/compliance/eu-ai-act` — EU AI Act conformity certificate (Annex IV auto-generated)
  - `/v1/compliance/fairness` — Formal bias bounds (FNS-100-FairnessBound)
  - `/v1/compliance/explain` — Explainability certificate (XPL-100-ExplainBound)
  - `/v1/compliance/lineage` — Data provenance chain (LIN-100-ChainIntegrity)
  - `/v1/compliance/oversight` — Human oversight event log (EU AI Act Art. 14)
  - `/v1/compliance/oversight/history` — Oversight audit log query
  - `/v1/compliance/incident` — AI incident reporting (EU AI Act Art. 73)
  - `/v1/compliance/incidents` — Incident registry query
  - `/v1/compliance/transparency` — Auto-generated transparency report (Art. 13)
  - `/v1/drift/check` — DriftGuard PSI monitoring (DRG-100-DriftBound, ≤0.20 at 95% CI)
  - `/v1/drift/certificate` — Signed PDF drift certificate for regulatory submissions
- **Trust Oracle** — `/v1/trust/score` and `/v1/trust/history` (TCM-100-BoundedMonotonicity)
- **Dynamic x402 percentage pricing** — DeFi fees now scale with transaction value (no cap):
  - VRF draw: $0.01 + 0.5% of pot_value_usd
  - Oracle verify: $0.04 + 0.1% of tvl_at_risk
  - LP optimize: $0.08 + 0.2% of position size
  - Liquidation check: $0.04 + 1% of net equity
- **Free trial expanded** to ALL paid endpoints — 3 calls/IP/day, 2s abuse-prevention delay
- **Mobile navigation** — slide-in drawer, overlay, hamburger↔X animation, Escape key dismiss
- **/defi and /compliance pages** — full product pages with usage guides for all endpoints

### Changed
- Credit pack starter tier: $4 → $8 (500 calls)
- Dynamic fee computation has zero infrastructure overhead — challenge-time pricing, no additional services required

### Fixed
- `/defi` and `/compliance` routes returning 404 (routing configuration corrected)
- Bridge verify returning 500 on GET requests
- Infrastructure reliability improvements

## [0.5.0] — 2026-04-08

### Added
- 102 production endpoints across 25 product families
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
