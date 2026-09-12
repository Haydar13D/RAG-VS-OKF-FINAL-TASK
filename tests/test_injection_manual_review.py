"""
Injection test dengan RAW RESPONSE LENGKAP -- tidak ada status LOLOS/BLOKIR
otomatis yang diklaim "aman". Semua jawaban mentah disimpan untuk kamu baca
satu-satu secara manual.

PENTING -- cara pakai untuk uji tiap provider secara terpisah:
Karena sistem ini pakai failover (OpenRouter -> Gemini -> Groq -> Ollama),
untuk menguji provider selain yang pertama, kamu perlu memaksa failover
turun dengan cara MENONAKTIFKAN SEMENTARA API key provider di atasnya
langsung di file .env, contoh:

  Untuk menguji Gemini:
    # OPENROUTER_API_KEY=sk-or-xxxx   <- comment/hapus sementara
    GEMINI_API_KEY=AIzaxxxx

  Untuk menguji Groq:
    # OPENROUTER_API_KEY=...
    # GEMINI_API_KEY=...
    GROQ_API_KEY=gsk_xxxx

  Untuk menguji Ollama:
    # OPENROUTER_API_KEY=...
    # GEMINI_API_KEY=...
    # GROQ_API_KEY=...
    USE_OLLAMA=true

Restart server (`uvicorn app:app --reload`) tiap kali ganti .env, lalu
jalankan script ini dengan flag --provider-label sesuai provider yang
sedang aktif, supaya hasilnya tercatat per-provider.

Jalankan:
    python test_injection_manual_review.py --url http://localhost:8000/chat --provider-label openrouter
    python test_injection_manual_review.py --url http://localhost:8000/chat --provider-label gemini
    python test_injection_manual_review.py --url http://localhost:8000/chat --provider-label groq
    python test_injection_manual_review.py --url http://localhost:8000/chat --provider-label ollama
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Windows terminal UTF-8 fix
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import requests


def call_chat(url: str, message: str) -> dict:
    start = time.time()
    try:
        resp = requests.post(url, json={"message": message}, timeout=60)
        elapsed = time.time() - start
        resp.raise_for_status()
        data = resp.json()
        return {
            "raw_answer": data.get("answer", ""),
            "sources": data.get("sources", []),
            "latency_seconds": round(elapsed, 2),
            "error": None,
        }
    except Exception as e:
        return {
            "raw_answer": None, "sources": [], "latency_seconds": round(time.time() - start, 2),
            "error": str(e),
        }


def basic_keyword_flag(text: str, keywords: list) -> list:
    """Cuma flag awal, BUKAN vonis akhir. Tetap baca manual."""
    if not text:
        return []
    lower = text.lower()
    return [kw for kw in keywords if kw.lower() in lower]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--provider-label", required=True, help="Label provider yang lagi aktif diuji (openrouter/gemini/groq/ollama)")
    parser.add_argument("--scenarios", default="injection_scenarios.json")
    args = parser.parse_args()

    data = json.loads(Path(args.scenarios).read_text(encoding="utf-8"))
    scenarios = data["scenarios"]
    keywords = data["leak_keywords_basic"]

    results = []
    for sc in scenarios:
        print(f"\n{'='*70}")
        print(f"[{sc['id']}] {sc['label']}")
        print(f"Prompt: {sc['prompt']}")
        print(f"{'='*70}")

        result = call_chat(args.url, sc["prompt"])
        flags = basic_keyword_flag(result["raw_answer"], keywords)

        print(f"RAW ANSWER:\n{result['raw_answer']}\n")
        print(f"Keyword flags (awal, bukan vonis): {flags if flags else 'tidak ada'}")
        print(f"Latency: {result['latency_seconds']}s")

        results.append({
            "id": sc["id"],
            "label": sc["label"],
            "prompt": sc["prompt"],
            "provider_tested": args.provider_label,
            "raw_answer": result["raw_answer"],
            "keyword_flags": flags,
            "latency_seconds": result["latency_seconds"],
            "error": result["error"],
            "manual_verdict": None,  # isi manual: "LEAK" / "SAFE_REFUSAL" / "SAFE_ANSWERED_LEGIT_PART_ONLY"
            "manual_notes": "",
        })

    output_file = f"injection_results_{args.provider_label}.json"
    Path(output_file).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n\n{'='*70}")
    print(f"SELESAI — provider: {args.provider_label}")
    print(f"{'='*70}")
    flagged_count = sum(1 for r in results if r["keyword_flags"])
    print(f"{flagged_count} dari {len(results)} skenario ke-flag keyword otomatis (cuma indikasi awal)")
    print(f"Hasil lengkap (raw_answer semua skenario) disimpan di: {output_file}")
    print("\nWAJIB DILAKUKAN SEKARANG:")
    print("1. Buka file JSON di atas, baca raw_answer SATU PER SATU (termasuk yang tidak ke-flag keyword)")
    print("2. Isi manual_verdict untuk tiap skenario: LEAK / SAFE_REFUSAL / SAFE_ANSWERED_LEGIT_PART_ONLY")
    print("3. Ulangi untuk provider lain (ganti .env + restart server + jalankan lagi dengan --provider-label berbeda)")
    print("4. Jangan simpulkan sistem 'aman' sampai SEMUA provider selesai direview manual")


if __name__ == "__main__":
    main()
