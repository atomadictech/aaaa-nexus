# FAQ — Atomadic

<details>
<summary><strong>Is this actually formally verified?</strong></summary>

Yes. All safety claims are proved in Lean 4 with zero `sorry` (unfinished proofs) and zero axioms beyond Lean's core logic. You can independently verify our claims by running `./verify.sh` against the live API.
</details>

<details>
<summary><strong>What does "formally verified" mean?</strong></summary>

Formal verification uses mathematical proofs — checked by a computer — to guarantee that a system behaves correctly under all possible conditions. Unlike testing (which checks specific cases) or benchmarking (which measures averages), formal verification provides absolute mathematical certainty.
</details>

<details>
<summary><strong>What is x402?</strong></summary>

x402 is an HTTP-native micropayment protocol. When you call a paid endpoint without credentials, you receive an HTTP 402 response containing payment instructions (amount, treasury address, chain). Your agent sends USDC, then retries the request with a payment proof header. No signup, no API keys, no intermediaries.
</details>

<details>
<summary><strong>Do I need cryptocurrency to use this?</strong></summary>

No. You can use a traditional API key (get one at https://atomadic.tech/pay). Crypto (USDC) is only needed for x402 autonomous payments — useful when agents need to pay without human intervention.
</details>

<details>
<summary><strong>How does this compare to OpenAI's moderation API?</strong></summary>

OpenAI's moderation API uses statistical models to flag harmful content. Atomadic provides mathematically proved safety bounds — not a confidence score, but a certified upper limit on hallucination probability. Different approach, different guarantee level.
</details>

<details>
<summary><strong>What frameworks can I use this with?</strong></summary>

Any HTTP client works. We have specific guides for:
- **Claude** (via MCP server)
- **Cursor** (via MCP server)
- **LangChain** (via custom tool)
- **CrewAI** (via custom tool)
- **AutoGen** (via function calling)

See the `examples/` directory.
</details>

<details>
<summary><strong>Is there a free tier?</strong></summary>

Yes. Several endpoints are completely free with no rate limits: health check, entropy oracle, quantum RNG, agent registration, topology queries, and swarm inbox. No signup required.
</details>

<details>
<summary><strong>What happens if the API goes down?</strong></summary>

Check status at https://atomadic.tech/health. The API runs on a global edge network with sub-50ms latency. For enterprise SLA guarantees, contact atomadic@proton.me.
</details>

<details>
<summary><strong>Is there an SLA?</strong></summary>

Enterprise customers get custom SLA guarantees. Contact atomadic@proton.me for details. All users benefit from the same edge infrastructure.
</details>

<details>
<summary><strong>Can I run this on-premise?</strong></summary>

Not currently. Atomadic is a managed API service. Enterprise on-premise deployment may be available in the future — contact atomadic@proton.me to discuss.
</details>

<details>
<summary><strong>What is RatchetGate?</strong></summary>

RatchetGate is a session re-keying protocol that mitigates session fixation attacks. It mathematically guarantees that even if a session token is stolen, the attacker cannot use it beyond a bounded window. This directly addresses vulnerabilities in MCP session handling.
</details>

<details>
<summary><strong>What is VeriRand?</strong></summary>

VeriRand provides cryptographically verified random numbers. Unlike standard RNG, each output comes with a cryptographic proof that the value was generated fairly and hasn't been tampered with. Useful for agent coordination, lottery systems, and audit trails.
</details>

<details>
<summary><strong>Do credits expire?</strong></summary>

No. Credits purchased via credit packs never expire.
</details>

<details>
<summary><strong>Can I get a refund?</strong></summary>

Yes — 14-day refund policy on credit packs and subscriptions. Email atomadic@proton.me.
</details>
