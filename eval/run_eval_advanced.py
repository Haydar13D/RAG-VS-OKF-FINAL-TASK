"""
eval/run_eval_advanced.py
-------------------------
Script Pengujian Evaluasi Akademis Komparatif (System RAG vs System OKF)
Memproses Dataset Extended N=40 (5 Kategori Teoretis) & Prompt Injection Test.

Penggunaan:
    python eval/run_eval_advanced.py --target-url http://localhost:8000/chat --system-label RAG --output eval/results_rag_N40.json
    python eval/run_eval_advanced.py --target-url http://localhost:8001/chat --system-label OKF --output eval/results_okf_N40.json
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
ACCURACY_FILE = BASE_DIR / "test_dataset_extended_N40.json"
INJECTION_FILE = BASE_DIR / "injection_scenarios_FINAL.json"


# Timeout 300s (5 menit) per kueri agar LLM lokal tidak terpotong saat inferensi panjang.
def call_chat_api(url: str, prompt: str, timeout_sec: int = 300) -> dict:
    start_time = time.time()
    error_type = None
    try:
        resp = requests.post(url, json={"message": prompt}, timeout=timeout_sec)
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
            "prompt_token_count": data.get("prompt_token_count", 0),
            "context_char_len": data.get("context_char_len", 0),
            "latency_seconds": round(elapsed, 2),
            "error": None,
            "error_type": data.get("error_type", None),
        }
    except requests.exceptions.Timeout as e:
        error_type = "TIMEOUT"
        return {
            "raw_answer": None,
            "sources": [],
            "status": "ERROR",
            "provider_used": None,
            "min_distance_score": None,
            "nav_metadata": None,
            "prompt_token_count": 0,
            "context_char_len": 0,
            "latency_seconds": round(time.time() - start_time, 2),
            "error": str(e),
            "error_type": "TIMEOUT",
        }
    except Exception as e:
        return {
            "raw_answer": None,
            "sources": [],
            "status": "ERROR",
            "provider_used": None,
            "min_distance_score": None,
            "nav_metadata": None,
            "prompt_token_count": 0,
            "context_char_len": 0,
            "latency_seconds": round(time.time() - start_time, 2),
            "error": str(e),
            "error_type": "CONNECTION_ERROR",
        }


def check_keyword_flags(answer: str, keywords: list) -> list:
    if not answer:
        return []
    lower = answer.lower()
    return [kw for kw in keywords if kw.lower() in lower]


def run_evaluation(target_url: str, system_label: str, output_path: str):
    print("=" * 80)
    print(f"  SORA ASSISTANT ADVANCED EVALUATION (N=40) — SYSTEM: {system_label}")
    print(f"  Target URL: {target_url}")
    print("=" * 80 + "\n")

    accuracy_data = json.loads(ACCURACY_FILE.read_text(encoding="utf-8"))
    injection_data = json.loads(INJECTION_FILE.read_text(encoding="utf-8"))

    acc_results = []
    category_summary = {}

    total_queries = len(accuracy_data["queries"])
    print(f"--- 1. UJI AKURASI JAWABAN (N={total_queries} SOAL) ---")
    for idx, q in enumerate(accuracy_data["queries"], 1):
        cat = q.get("category", "general")
        print(f"[{idx}/{total_queries}] [{q['id']}] ({cat}) {q['prompt'][:60]}...")
        res = call_chat_api(target_url, q["prompt"])

        matched_kw = [
            kw for kw in q["expected_keywords"]
            if res["raw_answer"] and kw.lower() in res["raw_answer"].lower()
        ]
        kw_coverage_pct = round((len(matched_kw) / len(q["expected_keywords"])) * 100, 1) if q["expected_keywords"] else 0.0

        # --- Fix bug pelabelan provider_error ---
        # Sebelumnya: hanya menghitung Fallback_Error sebagai error.
        # Sekarang:   status "ERROR" (apapun penyebabnya, termasuk HTTP Timeout)
        #             juga dihitung sebagai provider_error, sehingga completion_rate
        #             di category_summary tidak menyembunyikan kegagalan timeout.
        actual_status = res["status"]
        is_error = (actual_status == "ERROR") or (
            res["provider_used"] == "Fallback_Error"
            or res["raw_answer"] == "Maaf, terjadi masalah koneksi ke server AI saat ini."
        )
        if is_error:
            actual_status = "PROVIDER_ERROR"

        print(f"  → Provider : {res['provider_used']} | Latency: {res['latency_seconds']}s | Status: {actual_status}")
        print(f"  → Matched Keywords ({len(matched_kw)}/{len(q['expected_keywords'])}): {kw_coverage_pct}% | ErrorType: {res.get('error_type')}\n")

        if cat not in category_summary:
            category_summary[cat] = {
                "total": 0,
                "completed": 0,   # kueri yang benar-benar mendapat jawaban (bukan ERROR)
                "provider_error": 0,  # termasuk timeout & connection errors
                "timeout_count": 0,   # subset provider_error: HTTP timeout
                "total_latency": 0.0,
                "kw_coverage_sum": 0.0,
            }
        category_summary[cat]["total"] += 1
        if actual_status in ("ANSWERED", "KNOWLEDGE_GAP", "GREETING", "IDENTITY"):
            category_summary[cat]["completed"] += 1
        if actual_status == "PROVIDER_ERROR":
            category_summary[cat]["provider_error"] += 1
            if res.get("error_type") == "TIMEOUT":
                category_summary[cat]["timeout_count"] += 1

        category_summary[cat]["total_latency"] += res["latency_seconds"]
        if actual_status != "PROVIDER_ERROR":
            category_summary[cat]["kw_coverage_sum"] += kw_coverage_pct

        acc_results.append({
            "id": q["id"],
            "category": cat,
            "prompt": q["prompt"],
            "expected_keywords": q["expected_keywords"],
            "matched_keywords": matched_kw,
            "keyword_coverage_pct": kw_coverage_pct,
            "raw_answer": res["raw_answer"],
            "status": actual_status,
            "provider_used": res["provider_used"],
            "latency_seconds": res["latency_seconds"],
            "error": res["error"],
            "error_type": res.get("error_type"),
            "manual_score_likert": None,
            "evaluator_notes": ""
        })

    inj_results = []
    keywords = injection_data.get("leak_keywords_basic", ["system prompt", "instruksi internal"])
    print("\n--- 2. UJI KETAHANAN PROMPT INJECTION ---")
    for sc in injection_data["scenarios"]:
        print(f"[{sc['id']}] {sc['label']}")
        res = call_chat_api(target_url, sc["prompt"])
        flags = check_keyword_flags(res["raw_answer"], keywords)
        
        inj_status = res["status"]
        if res["provider_used"] == "Fallback_Error" or res["raw_answer"] == "Maaf, terjadi masalah koneksi ke server AI saat ini.":
            inj_status = "ERROR"

        print(f"  → Provider : {res['provider_used']} | Latency: {res['latency_seconds']}s | Status: {inj_status}")
        print(f"  → Keyword Flags (Awal): {flags if flags else 'TIDAK ADA'}\n")

        inj_results.append({
            "id": sc["id"],
            "label": sc["label"],
            "prompt": sc["prompt"],
            "raw_answer": res["raw_answer"],
            "keyword_flags": flags,
            "status": inj_status,
            "provider_used": res["provider_used"],
            "latency_seconds": res["latency_seconds"],
            "error": res["error"],
            "manual_verdict": None,
            "manual_notes": ""
        })

    # --- Hitung overall completion rate & accuracy | completed ---
    total_completed = sum(c["completed"] for c in category_summary.values())
    total_errors    = sum(c["provider_error"] for c in category_summary.values())
    total_timeout   = sum(c["timeout_count"] for c in category_summary.values())
    total_q         = len(acc_results)
    overall_completion_rate_pct = round((total_completed / total_q) * 100, 1) if total_q else 0.0

    # Keyword coverage hanya dari kueri yang berhasil menjawab
    accuracy_completed_only_pct = round(
        sum(c["kw_coverage_sum"] for c in category_summary.values()) /
        total_completed if total_completed else 0.0, 1
    )
    # Tambahkan completion_rate per kategori
    for cat, s in category_summary.items():
        s["completion_rate_pct"] = round((s["completed"] / s["total"]) * 100, 1) if s["total"] else 0.0
        s["avg_kw_coverage_completed_pct"] = round(s["kw_coverage_sum"] / s["completed"], 1) if s["completed"] else 0.0

    overall_summary = {
        "total_queries": total_q,
        "completed_queries": total_completed,
        "error_queries": total_errors,
        "timeout_queries": total_timeout,
        "overall_completion_rate_pct": overall_completion_rate_pct,
        "accuracy_keyword_coverage_on_completed_pct": accuracy_completed_only_pct,
        "note": (
            "completion_rate = kueri yang mendapat jawaban / total kueri. "
            "accuracy_keyword_coverage hanya dihitung dari kueri yang completed (bukan ERROR). "
            "Pisahkan dua angka ini saat pelaporan Bab IV."
        )
    }

    final_payload = {
        "system_label": system_label,
        "target_url": target_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_accuracy_queries": total_q,
        "total_injection_scenarios": len(inj_results),
        "overall_summary": overall_summary,
        "category_summary": category_summary,
        "accuracy_eval": acc_results,
        "injection_eval": inj_results
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(final_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 80)
    print(f"✅ EVALUASI ADVANCED SELESAI — System {system_label}")
    print(f"  Completion Rate : {overall_completion_rate_pct}% ({total_completed}/{total_q} kueri berhasil dijawab)")
    print(f"  Timeout/Error   : {total_errors} kueri gagal ({total_timeout} timeout, {total_errors - total_timeout} connection error)")
    print(f"  Akurasi (KW Cov): {accuracy_completed_only_pct}% (hanya dari {total_completed} kueri yang completed)")
    print(f"File Hasil Evaluasi disimpan di: {out_file.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-url", required=True, help="URL Endpoint Chat API (contoh: http://localhost:8000/chat)")
    parser.add_argument("--system-label", required=True, help="Label Sistem (RAG atau OKF)")
    parser.add_argument("--output", required=True, help="Path file output JSON")
    args = parser.parse_args()

    run_evaluation(args.target_url, args.system_label, args.output)
