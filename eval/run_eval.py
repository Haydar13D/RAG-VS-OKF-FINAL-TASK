"""
eval/run_eval.py
----------------
Script pengujian komparatif Head-to-Head untuk System RAG vs System OKF.
Menjalankan pengujian akurasi dan ketahanan prompt injection ke endpoint FastAPI target.

Penggunaan:
    python eval/run_eval.py --target-url http://localhost:8000/chat --system-label RAG --output eval/results_rag.json
    python eval/run_eval.py --target-url http://localhost:8001/chat --system-label OKF --output eval/results_okf.json
"""

import argparse
import json
import sys
import time
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
ACCURACY_FILE = BASE_DIR / "accuracy_test_set_FINAL.json"
INJECTION_FILE = BASE_DIR / "injection_scenarios_FINAL.json"


def call_chat_api(url: str, prompt: str) -> dict:
    start_time = time.time()
    try:
        resp = requests.post(url, json={"message": prompt}, timeout=45)
        elapsed = time.time() - start_time
        resp.raise_for_status()
        data = resp.json()
        return {
            "raw_answer": data.get("answer", ""),
            "sources": data.get("sources", []),
            "status": data.get("status", "UNKNOWN"),
            "provider_used": data.get("provider_used", "UNKNOWN"),
            "min_distance_score": data.get("min_distance_score", None),
            "nav_metadata": data.get("nav_metadata", None),
            "latency_seconds": round(elapsed, 2),
            "error": None,
        }
    except Exception as e:
        return {
            "raw_answer": None,
            "sources": [],
            "status": "ERROR",
            "provider_used": None,
            "min_distance_score": None,
            "nav_metadata": None,
            "latency_seconds": round(time.time() - start_time, 2),
            "error": str(e),
        }


def check_keyword_flags(answer: str, keywords: list) -> list:
    if not answer:
        return []
    lower = answer.lower()
    return [kw for kw in keywords if kw.lower() in lower]


def run_evaluation(target_url: str, system_label: str, output_path: str):
    print("=" * 70)
    print(f"  SORA ASSISTANT EVALUATION — SYSTEM: {system_label}")
    print(f"  Target URL: {target_url}")
    print("=" * 70 + "\n")

    # Load instruments
    accuracy_data = json.loads(ACCURACY_FILE.read_text(encoding="utf-8"))
    injection_data = json.loads(INJECTION_FILE.read_text(encoding="utf-8"))

    acc_results = []
    print("--- 1. UJI AKURASI JAWABAN ---")
    for q in accuracy_data["queries"]:
        print(f"[{q['id']}] {q['prompt'][:60]}...")
        res = call_chat_api(target_url, q["prompt"])
        matched_kw = [kw for kw in q["expected_keywords"] if res["raw_answer"] and kw.lower() in res["raw_answer"].lower()]
        print(f"  → Provider : {res['provider_used']} | Latency: {res['latency_seconds']}s | Status: {res['status']}")
        print(f"  → Matched Keywords ({len(matched_kw)}/{len(q['expected_keywords'])}): {matched_kw}\n")

        acc_results.append({
            "id": q["id"],
            "category": q["category"],
            "prompt": q["prompt"],
            "expected_keywords": q["expected_keywords"],
            "matched_keywords": matched_kw,
            "raw_answer": res["raw_answer"],
            "status": res["status"],
            "provider_used": res["provider_used"],
            "latency_seconds": res["latency_seconds"],
            "error": res["error"]
        })

    inj_results = []
    keywords = injection_data["leak_keywords_basic"]
    print("\n--- 2. UJI KETAHANAN PROMPT INJECTION ---")
    for sc in injection_data["scenarios"]:
        print(f"[{sc['id']}] {sc['label']}")
        res = call_chat_api(target_url, sc["prompt"])
        flags = check_keyword_flags(res["raw_answer"], keywords)
        print(f"  → Provider : {res['provider_used']} | Latency: {res['latency_seconds']}s")
        print(f"  → Keyword Flags (Awal): {flags if flags else 'TIDAK ADA'}\n")

        inj_results.append({
            "id": sc["id"],
            "label": sc["label"],
            "prompt": sc["prompt"],
            "raw_answer": res["raw_answer"],
            "keyword_flags": flags,
            "status": res["status"],
            "provider_used": res["provider_used"],
            "latency_seconds": res["latency_seconds"],
            "error": res["error"],
            "manual_verdict": None,
            "manual_notes": ""
        })

    final_payload = {
        "system_label": system_label,
        "target_url": target_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy_eval": acc_results,
        "injection_eval": inj_results
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(final_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 70)
    print(f"✅ EVALUASI SELESAI — System {system_label}")
    print(f"File Hasil Evaluasi disimpan di: {out_file.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-url", required=True, help="URL Endpoint Chat API (contoh: http://localhost:8000/chat)")
    parser.add_argument("--system-label", required=True, help="Label Sistem (RAG atau OKF)")
    parser.add_argument("--output", required=True, help="Path file output JSON")
    args = parser.parse_args()

    run_evaluation(args.target_url, args.system_label, args.output)
