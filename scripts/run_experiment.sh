#!/usr/bin/env bash
# run_experiment.sh — Compile and execute all memory-access benchmarks.
#
# Usage:
#   cd /path/to/project
#   bash scripts/run_experiment.sh
#
# Output:
#   data/raw/results.csv   — raw benchmark data (stdout of benchmark binary)
#   data/raw/run.log       — stderr (progress + checksum)
#
# Prerequisites (WSL2/Ubuntu):
#   sudo apt-get install -y gcc build-essential python3 python3-pip
#   pip3 install pandas numpy scipy matplotlib

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src"
DATA_DIR="$PROJECT_ROOT/data/raw"
BINARY="$SRC_DIR/benchmark"
CSV_OUT="$DATA_DIR/results.csv"
LOG_OUT="$DATA_DIR/run.log"

# ---- 1. Build ---------------------------------------------------------------
echo "=== [1/3] Building benchmark ==="
cd "$SRC_DIR"
make clean
make
echo ""

# ---- 2. Environment check ---------------------------------------------------
echo "=== [2/3] Environment ==="
echo "Kernel : $(uname -r)"
echo "CPU    : $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
echo "Binary : $BINARY"
echo ""

# Pin to CPU 0 if taskset is available — prevents cross-core migration noise.
# In WSL2 this reduces variance but cannot control frequency scaling.
if command -v taskset &>/dev/null; then
    RUNNER="taskset -c 0"
    echo "CPU affinity: pinned to core 0 via taskset"
else
    RUNNER=""
    echo "WARNING: taskset not found — process may migrate between cores."
    echo "         Install util-linux: sudo apt-get install util-linux"
fi
echo ""

# ---- 3. Run -----------------------------------------------------------------
mkdir -p "$DATA_DIR"

echo "=== [3/3] Running benchmarks ==="
echo "Output CSV : $CSV_OUT"
echo "Log file   : $LOG_OUT"
echo ""

START_TS=$(date +%s)
$RUNNER "$BINARY" > "$CSV_OUT" 2> "$LOG_OUT"
END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))

echo ""
echo "=== Done in ${ELAPSED}s ==="

# Validate output
NROWS=$(wc -l < "$CSV_OUT")
echo "CSV rows (header + data): $NROWS"
echo "Expected minimum: $((1 + 30 * (4 * 9 + 4)))" # 1 header + runs*(patterns*sizes + block)

if [ "$NROWS" -lt 100 ]; then
    echo "ERROR: Too few rows — benchmark may have crashed. Check $LOG_OUT"
    exit 1
fi

echo ""
echo "Last 5 progress lines from log:"
tail -5 "$LOG_OUT"
echo ""
echo "Results ready. Run analysis:"
echo "  cd $PROJECT_ROOT && python3 scripts/analyze.py && python3 scripts/plot.py"
