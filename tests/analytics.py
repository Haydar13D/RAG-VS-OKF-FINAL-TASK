import os
import sys
import json
from collections import Counter

# Standardize UTF-8 stdout encoding for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "chat_conversations.jsonl")

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print(f"INFO: File log '{LOG_FILE}' belum ada. Belum ada percakapan yang terekam.")
        return

    conversations = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                conversations.append(json.loads(line))
            except Exception:
                pass

    if not conversations:
        print("INFO: File log kosong.")
        return

    print("=" * 70)
    print(" LAPORAN ANALISTIK PERCAKAPAN SORA ASSISTANT AI")
    print("=" * 70)
    print(f"Total Percakapan Terekam : {len(conversations)}")

    # Status Breakdown
    statuses = Counter(c.get("status", "UNKNOWN") for c in conversations)
    print("\n--- Ringkasan Status Answer ---")
    for st, count in statuses.items():
        pct = (count / len(conversations)) * 100
        print(f"  * {st:15s} : {count:3d} ({pct:.1f}%)")

    # Provider Breakdown
    providers = Counter(c.get("provider_used", "UNKNOWN") for c in conversations)
    print("\n--- Provider LLM Yang Digunakan ---")
    for pr, count in providers.items():
        print(f"  * {pr:18s} : {count:3d}")

    # Feedback Breakdown
    feedbacks = Counter(c.get("feedback_rating") for c in conversations)
    print("\n--- Ringkasan Feedback User (Thumbs Rating) ---")
    print(f"  * Thumbs Up  [+] : {feedbacks.get('up', 0)}")
    print(f"  * Thumbs Down [-] : {feedbacks.get('down', 0)}")
    print(f"  * Belum Rating    : {feedbacks.get(None, 0)}")

    # Knowledge Gaps (Pertanyaan yang belum ada panduannya di docs/)
    gaps = [c for c in conversations if c.get("status") == "KNOWLEDGE_GAP"]
    print("\n" + "=" * 70)
    print(f" DAFTAR KNOWLEDGE GAPS ({len(gaps)} Pertanyaan Belum Ada di Dokumentasi)")
    print("=" * 70)
    if gaps:
        for i, g in enumerate(gaps, 1):
            print(f" [{i}] {g.get('timestamp', '')[:19]}")
            print(f"     User Query   : \"{g.get('user_message', '')}\"")
            print(f"     Min Distance : {g.get('min_distance_score', 1.0):.4f} (Melebihi threshold 0.48)")
            print(f"     Action Req   : Tambahkan materi ini ke folder docs/ lalu jalankan `python ingest.py`\n")
    else:
        print("  [+] Selamat! Semua pertanyaan kasir sejauh ini berhasil dijawab berdasarkan dokumentasi.")

    print("=" * 70)

if __name__ == "__main__":
    analyze_logs()
