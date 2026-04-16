# Atomadic Tech — Blockchain Anchor Plan
## Step 1 of the Sovereign Stack IP Protection Strategy

**Date:** 2026-04-16  
**Purpose:** Cryptographically timestamp all Atomadic IP on Base L2 as immutable prior-art evidence.

---

## Why We're Doing This

A SHA-256 hash of our entire IP archive, broadcast as a Base L2 transaction, creates a timestamped, immutable, publicly verifiable record that:

- We possessed this IP as of this exact date
- The archive has not been modified since (any change = different hash)
- No centralized authority can revoke or dispute it

This is Step 1 of the Sovereign Stack — executed before patent filing, arXiv publication, or blog cascade.

---

## What Goes Into the Archive

### Tier 1 — Core IP (highest priority)
| Asset | Path | Description |
|-------|------|-------------|
| MHED-TOE V22 Codex | `!mhed-codex/MHED_TOE_CODEX_V22_OMNIS.json` | 53 core + 40 emergent constants, 8 pillars |
| MHED-TOE V20 Codex | `!mhed-codex/MHED_TOE_CODEX_V20_SOVEREIGN.json` | Historical record, prior-art chain |
| Lean4 Formal Proofs | `!mhed-codex/proofs/AethelNexus/` | 32 files, 538+ theorems, 0 sorry |
| Rust Constants | `!mhed-codex/constants/aethel_constants_full.rs` | All constants in Rust |
| 0xSeed Kernel | `!0xSeed/kernel_rs/src/` | RatchetGate, x402 gateway, invariants |
| GENESIS.md | `!0xSeed/GENESIS.md` | UEP v10.0 bootstrap declaration, April 8 2026 |

### Tier 2 — Strong Prior Art
| Asset | Path | Description |
|-------|------|-------------|
| AAAA-Nexus public docs | `!aaaa-nexus-github/` | API docs, proofs of correctness, BSL license |
| SDK source | `!aaaa-nexus-sdk/src/` | TypeScript SDK implementation |
| ASS-ADE source + docs | `!ass-ade/src/` + `docs/` | Agent framework, protocol spec |

### Tier 3 — UEP Prior Art
| Asset | Path | Description |
|-------|------|-------------|
| UEP v10 core | `!atomadic-uep/` (source only) | EDEE, reward engine, MHED math engine |
| UEP IDE | `!uep_ide/codex/` + `tests/` | Proof synthesis, sovereign invariant tests |

### Narrative Document
- `IP_NARRATIVE.md` — World Firsts declaration (included in archive root)

---

## How to Run

```bash
# On WSL or Git Bash on Windows:
bash /c/!aaaa-nexus-github/scripts/build-ip-archive.sh

# Or specify a custom output directory:
bash /c/!aaaa-nexus-github/scripts/build-ip-archive.sh /tmp/my-archive
```

The script will:
1. Copy all source files (excluding `node_modules`, `target`, `venv`, `.git`, build artifacts)
2. Generate `MANIFEST.txt` with individual SHA-256 hashes for every file
3. Create `atomadic-ip-anchor-<date>.tar.gz`
4. Print the **final SHA-256 hash** — this is what you broadcast to Base L2

---

## Broadcasting to Base L2

After running the script, you'll see output like:
```
SHA-256: abc123...def456
```

### Option A: Using Foundry cast (recommended)
```bash
# Install: curl -L https://foundry.paradigm.xyz | bash
cast send 0x000000000000000000000000000000000000dead \
  --value 0 \
  --data 0x<ARCHIVE_HASH_HEX> \
  --rpc-url https://mainnet.base.org \
  --private-key YOUR_PRIVATE_KEY
```

### Option B: Using MetaMask (no CLI needed)
1. Open MetaMask → Send
2. To: `0x000000000000000000000000000000000000dead` (burn address — public, permanent)
3. Amount: 0 ETH
4. Add hex data: `0x` + your SHA-256 hash
5. Confirm on Base network (chain ID 8453)
6. Cost: ~$0.01 in ETH gas

### Option C: Using the AAAA-Nexus x402 infrastructure
The treasury wallet `0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9` can relay the anchor transaction — contact atomadic@proton.me to coordinate.

---

## After Broadcasting

Save the transaction receipt:

```
# BLOCKCHAIN_ANCHOR.txt (save this file alongside the archive)
Archive: atomadic-ip-anchor-2026-04-16.tar.gz
SHA-256: <hash>
Chain: Base L2 (chain ID 8453)
Tx Hash: <tx_hash>
Block: <block_number>
Timestamp: <unix_timestamp>
Explorer: https://basescan.org/tx/<tx_hash>
```

---

## Sovereign Stack Status

| Step | Description | Status |
|------|-------------|--------|
| **Step 1** | SHA-256 anchor → Base L2 | ⏳ Ready to run |
| **Step 2** | USPTO provisional patent + CIPO/USPTO trademarks | ⏳ Needs legal counsel |
| **Step 3** | BSL 1.1 license in public repo | ✅ Complete (2026-04-16) |
| **Step 4** | arXiv whitepaper (MHED-TOE + UEP prior art) | ⏳ Ready to draft |
| **Step 5** | Blog cascade (5-part launch) | 🔒 After Steps 1-3 |

---

## Security Notes

- The archive itself is **not published** — only the hash goes on-chain
- The hash proves you possessed the content at this date without revealing it
- Keep the `.tar.gz` in cold storage (offline drive + encrypted backup)
- The `MANIFEST.txt` inside the archive lets anyone verify individual files without unpacking everything
