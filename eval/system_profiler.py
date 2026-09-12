"""
eval/system_profiler.py
------------------------
Script Profiler Sistem untuk Mengukur Latency, Konsumsi RAM (MB), dan CPU Utilization (%)
saat System RAG / OKF menerima beban kerja pengujian.

Penggunaan:
    python eval/system_profiler.py --target-url http://localhost:8000/chat --system-label RAG --output eval/profile_rag.json
    python eval/system_profiler.py --target-url http://localhost:8001/chat --system-label OKF --output eval/profile_okf.json
"""

import argparse
import json
import sys
import time
import requests
import psutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
ACCURACY_FILE = BASE_DIR / "test_dataset_extended_N40.json"


def call_chat_api(url: str, prompt: str) -> float:
    start_time = time.time()
    try:
        resp = requests.post(url, json={"message": prompt}, timeout=120)
        resp.raise_for_status()
    except Exception:
        pass
    return round(time.time() - start_time, 2)


def profile_system(target_url: str, system_label: str, output_path: str):
    print("=" * 80)
    print(f"  SYSTEM PROFILER (RAM / CPU / LATENCY) — SYSTEM: {system_label}")
    print(f"  Target URL: {target_url}")
    print("=" * 80 + "\n")

    accuracy_data = json.loads(ACCURACY_FILE.read_text(encoding="utf-8"))
    queries = accuracy_data.get("queries", [])[:10]  # Take 10 sample queries for load profiling

    ram_samples_mb = []
    cpu_samples_pct = []
    latency_list = []

    # Measure baseline
    base_ram = psutil.virtual_memory().used / (1024 * 1024)
    base_cpu = psutil.cpu_percent(interval=1.0)
    print(f"Baseline System Metrics -> RAM Used: {base_ram:.2f} MB | CPU Usage: {base_cpu:.1f}%\n")

    print("--- Running Load Test for Profiling ---")
    for idx, q in enumerate(queries, 1):
        cpu_before = psutil.cpu_percent(interval=None)
        lat = call_chat_api(target_url, q["prompt"])
        cpu_after = psutil.cpu_percent(interval=None)
        ram_now = psutil.virtual_memory().used / (1024 * 1024)

        latency_list.append(lat)
        ram_samples_mb.append(ram_now)
        cpu_samples_pct.append(cpu_after)

        print(f"Query #{idx:02d} -> Latency: {lat}s | RAM Used: {ram_now:.2f} MB | CPU Load: {cpu_after:.1f}%")
        time.sleep(0.5)

    avg_latency = round(sum(latency_list) / len(latency_list), 2)
    avg_ram_mb = round(sum(ram_samples_mb) / len(ram_samples_mb), 2)
    max_ram_mb = round(max(ram_samples_mb), 2)
    avg_cpu_pct = round(sum(cpu_samples_pct) / len(cpu_samples_pct), 1)
    max_cpu_pct = round(max(cpu_samples_pct), 1)

    result_payload = {
        "system_label": system_label,
        "target_url": target_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "baseline_ram_mb": round(base_ram, 2),
        "baseline_cpu_pct": base_cpu,
        "avg_latency_seconds": avg_latency,
        "avg_ram_used_mb": avg_ram_mb,
        "max_ram_used_mb": max_ram_mb,
        "avg_cpu_usage_pct": avg_cpu_pct,
        "max_cpu_usage_pct": max_cpu_pct,
        "latency_samples": latency_list,
        "ram_samples_mb": ram_samples_mb,
        "cpu_samples_pct": cpu_samples_pct
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(result_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 80)
    print(f"📊 PROFILING SUMMARY — System {system_label}:")
    print(f"  • Avg Latency   : {avg_latency}s")
    print(f"  • Avg RAM Used  : {avg_ram_mb} MB (Peak: {max_ram_mb} MB)")
    print(f"  • Avg CPU Usage : {avg_cpu_pct}% (Peak: {max_cpu_pct}%)")
    print(f"File profiling disimpan di: {out_file.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-url", required=True, help="URL Endpoint Chat API")
    parser.add_argument("--system-label", required=True, help="Label Sistem (RAG atau OKF)")
    parser.add_argument("--output", required=True, help="Path file output JSON")
    args = parser.parse_args()

    profile_system(args.target_url, args.system_label, args.output)
