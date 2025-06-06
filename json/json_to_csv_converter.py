import json
import csv
import os
from datetime import datetime

# Constants
INPUT_JSON = "sample_json.json"
BASE_OUTPUT_PATH = r"C:\temp\namespace"
TODAY = datetime.now().strftime("%Y%m%d")

# Metrics of interest
EXPECTED_METRICS = {
    "A": "cpu_usage",
    "B": "cpu_throttling",
    "C": "cpu_requests",
    "D": "cpu_limits",
    "E": "memory_requests",
    "F": "memory_limits",
    "H": "num_pods"
}

# Validation: Check input file
if not os.path.exists(INPUT_JSON):
    print(f"❌ Input file not found: {INPUT_JSON}")
    exit(1)

# Load JSON content
try:
    with open(INPUT_JSON, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON format: {e}")
    exit(1)

tiles = data.get("tiles", [])
if not tiles:
    print("❌ No 'tiles' found in JSON.")
    exit(1)

metrics_tile = next((tile for tile in tiles if tile.get("tileType") == "DATA_EXPLORER"), None)
if not metrics_tile or not metrics_tile.get("queries"):
    print("❌ DATA_EXPLORER tile with queries not found.")
    exit(1)

# Simulate metric data (since input JSON lacks values)
sample_keys = [
    ("cluster-1", "namespace-a", "workload-x"),
    ("cluster-1", "namespace-a", "workload-y"),
    ("cluster-2", "namespace-b", "workload-z")
]
metric_data = {qid: {} for qid in EXPECTED_METRICS}
for qid in EXPECTED_METRICS:
    for key in sample_keys:
        metric_data[qid][key] = round(1 + hash(key + (qid,)) % 500 / 100, 2)

# Organize rows by namespace
namespace_map = {}
for key in sample_keys:
    cluster, namespace, workload = key
    row = {
        "Cluster Name": cluster,
        "Namespace Name": namespace,
        "Workload Name": workload,
        "CPU Usage": metric_data["A"].get(key, 0.0),
        "CPU Throttling": metric_data["B"].get(key, 0.0),
        "CPU Requests": metric_data["C"].get(key, 0.0),
        "CPU Limits": metric_data["D"].get(key, 0.0),
        "Memory Requests": metric_data["E"].get(key, 0.0),
        "Memory Limits": metric_data["F"].get(key, 0.0),
        "Number of Pods": metric_data["H"].get(key, 0)
    }
    namespace_map.setdefault(namespace, []).append(row)

# Write CSV per namespace
for namespace, rows in namespace_map.items():
    output_dir = os.path.join(BASE_OUTPUT_PATH, TODAY)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{namespace}_resource_usage.csv")

    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV created: {output_file}")
