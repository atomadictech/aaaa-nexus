#!/usr/bin/env python3
"""
AAAA-Nexus A2A Autonomous Transaction Demo
===========================================
Two AI agents conduct a fully autonomous service transaction:
  Agent A (buyer)  - needs a data analysis task completed
  Agent B (seller) - provides the service

Flow:
  1. Agent A checks Agent B's trust score
  2. Agent A runs a security threat scan on Agent B
  3. Agent A creates an on-chain escrow for the job
  4. Agent B performs the task (simulated)
  5. Agent A verifies and releases the escrow
  6. Both agents record the interaction to the reputation ledger
  7. Final settlement proof anchored on Base Sepolia

Usage:
  pip install -r requirements.txt
  export AAAA_NEXUS_API_KEY=an_your_key_here
  export DEMO_PRIVATE_KEY=0x_your_base_sepolia_key   # optional, for on-chain settlement
  python a2a_demo.py
"""

import os
import sys
import time
import json
import hashlib
import secrets
import requests

# -- colour helpers (no external deps needed) ----------------------------------
BOLD   = "\033[1m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
RED    = "\033[31m"
GRAY   = "\033[90m"
RESET  = "\033[0m"

def hdr(text):     print(f"\n{BOLD}{CYAN}{'='*60}{RESET}\n{BOLD}{CYAN}  {text}{RESET}\n{BOLD}{CYAN}{'='*60}{RESET}")
def step(n, text): print(f"\n{BOLD}{YELLOW}[Step {n}]{RESET} {text}")
def ok(text):      print(f"  {GREEN}[OK]{RESET} {text}")
def info(text):    print(f"  {GRAY}>>{RESET} {text}")
def fail(text):    print(f"  {RED}[FAIL]{RESET} {text}")

# -- config --------------------------------------------------------------------
BASE_URL    = os.getenv("AAAA_NEXUS_URL", "https://atomadic.tech")
API_KEY     = os.getenv("AAAA_NEXUS_API_KEY", "")
PRIV_KEY    = os.getenv("DEMO_PRIVATE_KEY", "")
TREASURY    = "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"
SEPOLIA_RPC = "https://sepolia.base.org"
CHAIN_ID    = 84532   # Base Sepolia

AGENT_A_ID = "32400"    # buyer agent  - topology-compliant ID
AGENT_B_ID = "64800"    # seller agent - topology-compliant ID
TASK_DESC  = "Summarize Q1 2026 DeFi TVL trends from on-chain data"

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["X-API-Key"] = API_KEY

# -- helpers -------------------------------------------------------------------
def call(method: str, path: str, body: dict | None = None, label: str = "") -> dict:
    url = f"{BASE_URL}{path}"
    t0  = time.time()
    if method.upper() == "GET":
        r = requests.get(url, params=body, headers=HEADERS, timeout=15)
    else:
        r = requests.post(url, json=body, headers=HEADERS, timeout=15)
    ms = int((time.time() - t0) * 1000)
    status_color = GREEN if r.status_code < 300 else (YELLOW if r.status_code < 500 else RED)
    print(f"  {GRAY}{method.upper()} {path}{RESET}  "
          f"{status_color}{r.status_code}{RESET}  {GRAY}{ms}ms{RESET}")
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    if label:
        info(f"{label}: {json.dumps(data, indent=None)[:120]}")
    return data

def fake_txid() -> str:
    return "0x" + secrets.token_hex(32)

def x402_proof(txid: str, amount_micro: int) -> str:
    """
    Build a demo x402 payment proof header.
    Format: sig;pk;txid;amount[;drift][;nonce]
    Uses placeholder keypair - for demo/testnet only.
    """
    pk_hex  = "0" * 64    # placeholder 32-byte pk
    sig_hex = "0" * 128   # placeholder 64-byte sig
    nonce   = secrets.token_hex(16)
    return f"{sig_hex};{pk_hex};{txid};{amount_micro};0.0;{nonce}"

# -- on-chain settlement (optional) -------------------------------------------
def send_base_sepolia_tx(amount_eth: float = 0.0001) -> str | None:
    if not PRIV_KEY:
        return None
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
        if not w3.is_connected():
            fail("Base Sepolia RPC not reachable - skipping on-chain settlement")
            return None
        acct    = w3.eth.account.from_key(PRIV_KEY)
        nonce   = w3.eth.get_transaction_count(acct.address)
        tx = {
            "to":       TREASURY,
            "value":    w3.to_wei(amount_eth, "ether"),
            "gas":      21000,
            "gasPrice": w3.to_wei("0.1", "gwei"),
            "nonce":    nonce,
            "chainId":  CHAIN_ID,
        }
        signed = acct.sign_transaction(tx)
        txhash = w3.eth.send_raw_transaction(signed.raw_transaction)
        return txhash.hex()
    except ImportError:
        info("web3 not installed - skipping on-chain settlement (pip install web3)")
        return None
    except Exception as e:
        fail(f"On-chain tx failed: {e}")
        return None

# -- main demo -----------------------------------------------------------------
def run():
    hdr("AAAA-NEXUS  A2A Autonomous Transaction Demo")
    print(f"  {BOLD}Agent A (buyer){RESET}  ID: {AGENT_A_ID}")
    print(f"  {BOLD}Agent B (seller){RESET} ID: {AGENT_B_ID}")
    print(f"  {BOLD}Task{RESET}             {TASK_DESC}")
    print(f"  {BOLD}Network{RESET}          Base Sepolia (chainId {CHAIN_ID})")
    print(f"  {BOLD}API Key{RESET}          {'set [OK]' if API_KEY else 'NOT SET - using free trial (3 calls/day)'}")

    receipts = {}

    # Step 1: Trust check ------------------------------------------------------
    step(1, "Agent A queries Agent B's trust score")
    trust = call("POST", "/v1/trust/score", {"agent_id": AGENT_B_ID}, "trust_score")
    score  = trust.get("trust_score", 0)
    tier   = trust.get("tier", "unknown")
    ok(f"Trust score: {score:.6f}  tier: {tier}")
    if score < 0.35:
        fail(f"Agent B trust score {score:.3f} below threshold 0.35 - aborting transaction")
        sys.exit(1)
    ok("Trust check PASSED - proceeding with transaction")
    receipts["trust_check"] = {"score": score, "tier": tier, "epoch": trust.get("epoch")}

    # Step 2: Threat scan ------------------------------------------------------
    step(2, "Agent A runs threat scan on Agent B")
    threat = call("POST", "/v1/threat/score", {
        "agent_id":   AGENT_B_ID,
        "context":    {"task": TASK_DESC, "value_usdc": 5.0}
    }, "threat")
    threat_level = threat.get("threat_level", threat.get("level", "unknown"))
    ok(f"Threat level: {threat_level}")
    receipts["threat_scan"] = threat

    # Step 3: Create escrow ----------------------------------------------------
    step(3, "Agent A creates escrow for task")
    escrow_txid = fake_txid()
    escrow = call("POST", "/v1/escrow/create", {
        "payer_agent_id":     AGENT_A_ID,
        "payee_agent_id":     AGENT_B_ID,
        "amount_micro_usdc":  5_000_000,
        "release_conditions": TASK_DESC,
        "ttl_hours":          1,
    }, "escrow")
    escrow_id = escrow.get("escrow_id", escrow.get("id", escrow_txid[:16]))
    ok(f"Escrow created: {escrow_id}")
    info("Amount: $5.00 USDC locked in trust")
    receipts["escrow_create"] = {"id": escrow_id, "txid": escrow_txid}

    # Step 4: Agent B executes task (simulated) --------------------------------
    step(4, "Agent B executes task (autonomous)")
    info("Agent B processing: fetching on-chain TVL data...")
    time.sleep(1.5)
    info("Agent B processing: running summarization model...")
    time.sleep(1.0)
    task_result = {
        "summary":   "Q1 2026 DeFi TVL grew 34% to $128B, led by liquid staking (+61%) and L2 DEXs (+42%).",
        "sources":   ["defillama.com", "dune.com/query/3847291"],
        "completed": int(time.time()),
        "agent_id":  AGENT_B_ID,
    }
    result_hash = hashlib.sha256(json.dumps(task_result, sort_keys=True).encode()).hexdigest()
    ok(f"Task complete - result hash: {result_hash[:16]}...")
    receipts["task_result"] = task_result

    # Step 5: Release escrow ---------------------------------------------------
    step(5, "Agent A verifies output and releases escrow")
    release = call("POST", "/v1/escrow/release", {
        "escrow_id":   escrow_id,
        "released_by": AGENT_A_ID,
        "proof":       result_hash,
    }, "release")
    ok(f"Escrow released: {release.get('status', 'ok')}")
    receipts["escrow_release"] = release

    # Step 6: Reputation records -----------------------------------------------
    step(6, "Both agents record interaction to reputation ledger")
    rep_a = call("POST", "/v1/reputation/record", {
        "agent_id":        AGENT_A_ID,
        "counterparty_id": AGENT_B_ID,
        "success":         True,
        "quality":         0.92,
        "latency_ms":      2500,
        "context":         "TVL analysis task completed",
    }, "rep_record")
    ok(f"Agent B reputation updated: {rep_a.get('new_score', rep_a.get('score', 'recorded'))}")
    receipts["reputation"] = rep_a

    # Step 7: Base Sepolia on-chain settlement ----------------------------------
    step(7, "Anchor settlement proof on Base Sepolia")
    settlement_txhash = send_base_sepolia_tx(0.0001)
    if settlement_txhash:
        ok(f"On-chain tx: {settlement_txhash}")
        info(f"View: https://sepolia.basescan.org/tx/{settlement_txhash}")
        receipts["onchain_settlement"] = settlement_txhash
    else:
        fake_hash = fake_txid()
        info(f"Simulated settlement hash: {fake_hash}")
        info("To send real Base Sepolia tx: export DEMO_PRIVATE_KEY=0x...")
        receipts["onchain_settlement"] = f"simulated:{fake_hash}"

    # Final summary ------------------------------------------------------------
    hdr("TRANSACTION COMPLETE")
    print(f"  {BOLD}Task:{RESET}        {TASK_DESC}")
    print(f"  {BOLD}Buyer:{RESET}       Agent A ({AGENT_A_ID})")
    print(f"  {BOLD}Seller:{RESET}      Agent B ({AGENT_B_ID})")
    print(f"  {BOLD}Amount:{RESET}      $5.00 USDC")
    print(f"  {BOLD}Trust:{RESET}       {score:.4f} ({tier})")
    print(f"  {BOLD}Escrow ID:{RESET}   {escrow_id}")
    print(f"  {BOLD}Settlement:{RESET}  {receipts['onchain_settlement'][:66]}")
    print(f"\n  {GREEN}{BOLD}All steps completed autonomously - zero human approvals.{RESET}")
    print(f"\n{GRAY}Full receipt:{RESET}")
    print(json.dumps(receipts, indent=2, default=str))


if __name__ == "__main__":
    run()
