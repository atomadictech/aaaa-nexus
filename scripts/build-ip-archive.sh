#!/usr/bin/env bash
# build-ip-archive.sh
# Builds a cryptographic IP archive for Atomadic Tech blockchain timestamping.
# Output: atomadic-ip-anchor-<date>.tar.gz + MANIFEST.txt with per-file SHA-256 hashes
# Usage: bash build-ip-archive.sh [output-dir]

set -euo pipefail

DATE=$(date +%Y-%m-%d)
ARCHIVE_NAME="atomadic-ip-anchor-${DATE}"
OUT_DIR="${1:-/tmp/${ARCHIVE_NAME}}"
FINAL_TAR="${OUT_DIR}/../${ARCHIVE_NAME}.tar.gz"
MANIFEST="${OUT_DIR}/MANIFEST.txt"

echo "==> Building IP archive: ${ARCHIVE_NAME}"
echo "    Output directory: ${OUT_DIR}"
echo ""

# ─── Clean start ─────────────────────────────────────────────────────────────
rm -rf "${OUT_DIR}"
mkdir -p \
  "${OUT_DIR}/mhed-codex" \
  "${OUT_DIR}/0xseed-kernel" \
  "${OUT_DIR}/aaaa-nexus-docs" \
  "${OUT_DIR}/ass-ade-core" \
  "${OUT_DIR}/sdk-source" \
  "${OUT_DIR}/uep-prior-art"

# ─── Helper: copy files excluding bloat ──────────────────────────────────────
rsync_clean() {
  local src="$1"
  local dst="$2"
  rsync -a --exclude='node_modules' \
            --exclude='target' \
            --exclude='.venv' \
            --exclude='venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='dist' \
            --exclude='build' \
            --exclude='.git' \
            --exclude='*.log' \
            --exclude='.DS_Store' \
            "$src" "$dst"
}

# ─── Tier 1: MHED-TOE Codex (highest-value IP) ───────────────────────────────
echo "[1/6] MHED-TOE Codex..."
SRC_CODEX="/c/!mhed-codex"
if [ -d "$SRC_CODEX" ]; then
  # JSON canonical sources
  for f in \
    "MHED_TOE_CODEX_V22_OMNIS.json" \
    "MHED_TOE_CODEX_V20_SOVEREIGN.json" \
    "mhed-codex-v20.json" \
    "README.md"; do
    [ -f "${SRC_CODEX}/${f}" ] && cp "${SRC_CODEX}/${f}" "${OUT_DIR}/mhed-codex/${f}" || true
  done
  # Lean4 proofs
  [ -d "${SRC_CODEX}/proofs" ] && rsync_clean "${SRC_CODEX}/proofs" "${OUT_DIR}/mhed-codex/"
  # Rust constants
  [ -d "${SRC_CODEX}/constants" ] && rsync_clean "${SRC_CODEX}/constants" "${OUT_DIR}/mhed-codex/"
  [ -d "${SRC_CODEX}/codex_api" ]  && rsync_clean "${SRC_CODEX}/codex_api"  "${OUT_DIR}/mhed-codex/"
  [ -d "${SRC_CODEX}/docs" ]       && rsync_clean "${SRC_CODEX}/docs"       "${OUT_DIR}/mhed-codex/"
  echo "    ✓ mhed-codex"
else
  echo "    ⚠ WARNING: ${SRC_CODEX} not found — skipping"
fi

# ─── Tier 1: 0xSeed Kernel ───────────────────────────────────────────────────
echo "[2/6] 0xSeed kernel..."
SRC_SEED="/c/!0xSeed"
if [ -d "$SRC_SEED" ]; then
  rsync_clean "${SRC_SEED}/kernel_rs/src/" "${OUT_DIR}/0xseed-kernel/kernel_rs/src/"
  for f in "GENESIS.md" "Cargo.toml" "agent_manifest.json"; do
    [ -f "${SRC_SEED}/${f}" ] && cp "${SRC_SEED}/${f}" "${OUT_DIR}/0xseed-kernel/${f}" || true
  done
  echo "    ✓ 0xseed-kernel"
else
  echo "    ⚠ WARNING: ${SRC_SEED} not found — skipping"
fi

# ─── Tier 1: AAAA-Nexus public docs ──────────────────────────────────────────
echo "[3/6] AAAA-Nexus docs..."
SRC_NEXUS="/c/!aaaa-nexus-github"
if [ -d "$SRC_NEXUS" ]; then
  rsync_clean "${SRC_NEXUS}/" "${OUT_DIR}/aaaa-nexus-docs/"
  echo "    ✓ aaaa-nexus-docs"
else
  echo "    ⚠ WARNING: ${SRC_NEXUS} not found — skipping"
fi

# ─── Tier 2: ASS-ADE source + docs ───────────────────────────────────────────
echo "[4/6] ASS-ADE..."
SRC_ADE="/c/!ass-ade"
if [ -d "$SRC_ADE" ]; then
  rsync_clean "${SRC_ADE}/src/"  "${OUT_DIR}/ass-ade-core/src/"
  rsync_clean "${SRC_ADE}/docs/" "${OUT_DIR}/ass-ade-core/docs/"
  for f in "README.md" "pyproject.toml" "setup.py"; do
    [ -f "${SRC_ADE}/${f}" ] && cp "${SRC_ADE}/${f}" "${OUT_DIR}/ass-ade-core/${f}" || true
  done
  echo "    ✓ ass-ade-core"
else
  echo "    ⚠ WARNING: ${SRC_ADE} not found — skipping"
fi

# ─── Tier 2: SDK source ──────────────────────────────────────────────────────
echo "[5/6] SDK source..."
SRC_SDK="/c/!aaaa-nexus-sdk"
if [ -d "$SRC_SDK" ]; then
  rsync_clean "${SRC_SDK}/src/" "${OUT_DIR}/sdk-source/src/"
  for f in "package.json" "tsconfig.json" "README.md"; do
    [ -f "${SRC_SDK}/${f}" ] && cp "${SRC_SDK}/${f}" "${OUT_DIR}/sdk-source/${f}" || true
  done
  echo "    ✓ sdk-source"
else
  echo "    ⚠ WARNING: ${SRC_SDK} not found — skipping"
fi

# ─── Tier 3: UEP prior art (core source only, no venv) ───────────────────────
echo "[6/6] UEP prior art..."
SRC_UEP="/c/!atomadic-uep"
if [ -d "$SRC_UEP" ]; then
  for subdir in agents memory tools codex prompts; do
    [ -d "${SRC_UEP}/${subdir}" ] && rsync_clean "${SRC_UEP}/${subdir}" "${OUT_DIR}/uep-prior-art/"
  done
  for f in "README.md" "SYSTEM_INTEGRATION_MAP.md" "ONBOARDING.md" \
           "api_server.py" "codex_prover_bridge.py" "llm_router.py"; do
    [ -f "${SRC_UEP}/${f}" ] && cp "${SRC_UEP}/${f}" "${OUT_DIR}/uep-prior-art/${f}" || true
  done
  # UEP IDE
  SRC_IDE="/c/!uep_ide"
  if [ -d "$SRC_IDE" ]; then
    rsync_clean "${SRC_IDE}/codex/" "${OUT_DIR}/uep-prior-art/uep_ide/codex/"
    rsync_clean "${SRC_IDE}/tests/" "${OUT_DIR}/uep-prior-art/uep_ide/tests/"
  fi
  echo "    ✓ uep-prior-art"
else
  echo "    ⚠ WARNING: ${SRC_UEP} not found — skipping"
fi

# ─── Write MANIFEST.txt with per-file SHA-256 ────────────────────────────────
echo ""
echo "==> Generating MANIFEST.txt..."

{
  echo "# Atomadic Tech — IP Archive Manifest"
  echo "# Archive: ${ARCHIVE_NAME}"
  echo "# Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# Purpose: Cryptographic prior-art anchor for Base L2 blockchain timestamp"
  echo "#"
  echo "# Format: SHA256  filepath"
  echo ""
} > "${MANIFEST}"

# Generate SHA-256 for every file in the archive
find "${OUT_DIR}" -type f ! -name "MANIFEST.txt" | sort | while read -r f; do
  rel="${f#${OUT_DIR}/}"
  if command -v sha256sum &>/dev/null; then
    sha256=$(sha256sum "$f" | awk '{print $1}')
  else
    sha256=$(shasum -a 256 "$f" | awk '{print $1}')
  fi
  echo "${sha256}  ${rel}"
done >> "${MANIFEST}"

FILE_COUNT=$(grep -c "^[a-f0-9]" "${MANIFEST}" || true)
echo "    ✓ MANIFEST.txt — ${FILE_COUNT} files indexed"

# ─── Create the tar.gz ───────────────────────────────────────────────────────
echo ""
echo "==> Creating tar.gz archive..."
tar -czf "${FINAL_TAR}" -C "$(dirname ${OUT_DIR})" "$(basename ${OUT_DIR})"

# ─── Final SHA-256 of the archive ────────────────────────────────────────────
echo ""
echo "==> Computing archive SHA-256..."
if command -v sha256sum &>/dev/null; then
  ARCHIVE_HASH=$(sha256sum "${FINAL_TAR}" | awk '{print $1}')
else
  ARCHIVE_HASH=$(shasum -a 256 "${FINAL_TAR}" | awk '{print $1}')
fi

ARCHIVE_SIZE=$(du -sh "${FINAL_TAR}" | awk '{print $1}')

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║               ATOMADIC IP ANCHOR — READY FOR BROADCAST              ║"
echo "╠══════════════════════════════════════════════════════════════════════╣"
printf "║  Archive:  %-58s ║\n" "${ARCHIVE_NAME}.tar.gz"
printf "║  Size:     %-58s ║\n" "${ARCHIVE_SIZE}"
printf "║  Files:    %-58s ║\n" "${FILE_COUNT}"
echo "╠══════════════════════════════════════════════════════════════════════╣"
echo "║  SHA-256 (broadcast this hash to Base L2):                          ║"
printf "║  %-68s ║\n" "${ARCHIVE_HASH}"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next step — broadcast to Base L2 using cast:"
echo ""
echo "  cast send 0x000000000000000000000000000000000000dead \\"
echo "    --value 0 \\"
echo "    --data 0x$(echo -n "${ARCHIVE_HASH}" | xxd -p | tr -d '\n') \\"
echo "    --rpc-url https://mainnet.base.org \\"
echo "    --private-key YOUR_PRIVATE_KEY"
echo ""
echo "Or store the hash and tx receipt in:"
echo "  ${OUT_DIR}/BLOCKCHAIN_ANCHOR.txt"
echo ""
echo "Archive location: ${FINAL_TAR}"
