import csv
from pathlib import Path
from statistics import mean, stdev, median

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "baremetal"
OUTPUT = ROOT / "data" / "processed" / "cpu_statistics.csv"


def load_column(path: Path, column: str) -> list[float]:
    with path.open(newline="") as f:
        return [float(row[column]) for row in csv.DictReader(f)]


benchmarks = [
    ("sysbench", RESULTS / "sysbench_cpu.csv", "events_per_sec"),
    ("taskset",  RESULTS / "sysbench_taskset.csv", "events_per_sec"),
    ("stressng", RESULTS / "stressng_cpu.csv", "bogo_ops_per_sec"),
]

rows = []
for name, path, col in benchmarks:
    values = load_column(path, col)
    rows.append({
        "benchmark": name,
        "mean":      round(mean(values), 4),
        "std":       round(stdev(values), 4),
        "median":    round(median(values), 4),
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["benchmark", "mean", "std", "median"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved: {OUTPUT}")
