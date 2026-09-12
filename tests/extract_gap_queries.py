"""
extract_gap_queries.py
----------------------
Ekstrak semua query KNOWLEDGE_GAP dari log percakapan nyata, lalu:
1. Print ringkasan statistik post-ingest (breakdown status terbaru)
2. Ekspor unique gap queries ke file test set untuk benchmark ulang
3. Jalankan benchmark gap queries + in-domain queries pakai gaya "kotor"
   (seperti cara user asli ngetik) terhadap ChromaDB saat ini
4. Kasih rekomendasi threshold baru yang lebih realistis

Cara pakai:
    python extract_gap_queries.py
"""

import os
import sys
import re
import json
from collections import Counter, defaultdict
import chromadb
from sentence_transformers import SentenceTransformer

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "chat_conversations.jsonl")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pos_knowledge"
EMBED_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# ── Typo normalization (sama persis dengan app.py) ──────────────────
typo_map = {
    r"\bistempromosinya\b": "sistem promo",
    r"\bistempromosi\b": "sistem promo",
    r"\bmembaut\b": "membuat",
    r"\bbaut\b": "buat",
    r"\bgimana\b": "bagaimana",
    r"\bgiman\b": "bagaimana",
    r"\bcar\b": "cara",
    r"\bnerapin\b": "menerapkan mengatur konfigurasi",
    r"\bqrisnya\b": "qris",
    r"\bdatabse\b": "database",
    r"\bsorasevvnth\b": "sora seventh",
    r"\bsora seveth\b": "sora seventh",
}

def normalize_query(query: str) -> str:
    normalized = query.lower()
    for pattern, replacement in typo_map.items():
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


# ── Muat log ─────────────────────────────────────────────────────────
def load_logs():
    conversations = []
    if not os.path.exists(LOG_FILE):
        print(f"ERROR: Log file tidak ditemukan: {LOG_FILE}")
        sys.exit(1)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                conversations.append(json.loads(line))
            except Exception:
                pass
    return conversations


# ── Statistik post-ingest ─────────────────────────────────────────────
def print_stats(conversations):
    total = len(conversations)
    statuses = Counter(c.get("status", "UNKNOWN") for c in conversations)
    print("=" * 70)
    print(f" STATUS PERCAKAPAN (total: {total})")
    print("=" * 70)
    for st, count in sorted(statuses.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"  {st:18s}: {count:4d} ({pct:5.1f}%)  {bar}")
    print()

    gap_count = statuses.get("KNOWLEDGE_GAP", 0)
    answered_count = statuses.get("ANSWERED", 0)
    print(f"  ⚠️  REFUSAL RATE   : {gap_count/total*100:.1f}%  ({gap_count} dari {total} pesan)")
    print(f"  ✅ ANSWER RATE    : {answered_count/total*100:.1f}%  ({answered_count} dari {total} pesan)")
    print()


# ── Ekstrak gap queries (unique, diurutkan by frekuensi) ─────────────
def extract_gap_queries(conversations):
    gap_convos = [c for c in conversations if c.get("status") == "KNOWLEDGE_GAP"]
    freq = Counter(c.get("user_message", "").strip().lower() for c in gap_convos)
    # Hapus kosong
    freq.pop("", None)
    return freq


# ── Benchmark gap queries vs ChromaDB ────────────────────────────────
def benchmark_queries(queries_with_freq, embed_model, collection, label, threshold):
    print("=" * 70)
    print(f" BENCHMARK: {label}")
    print("=" * 70)

    distances = []
    would_pass = 0
    would_fail = 0

    for q, freq in sorted(queries_with_freq.items(), key=lambda x: -x[1]):
        search_q = normalize_query(q)
        q_emb = embed_model.encode([search_q]).tolist()
        res = collection.query(
            query_embeddings=q_emb,
            n_results=3,
            include=["distances", "metadatas"]
        )
        dists = res.get("distances", [[]])[0]
        min_d = min(dists) if dists else 1.0
        distances.append(min_d)
        doc_title = (
            res.get("metadatas", [[]])[0][0].get("title", "unknown")
            if res.get("metadatas") and res["metadatas"][0]
            else "none"
        )
        passes = min_d <= threshold
        if passes:
            would_pass += 1
        else:
            would_fail += 1

        status_icon = "✅ PASS" if passes else "❌ BLOCK"
        freq_label = f"(x{freq})" if freq > 1 else ""
        print(f"  [{status_icon}] dist={min_d:.4f}  {freq_label}")
        print(f"         Query  : \"{q}\"")
        print(f"         Doc    : {doc_title}")
        print()

    if distances:
        avg_d = sum(distances) / len(distances)
        max_d = max(distances)
        min_d_val = min(distances)
        print(f"  ── Statistik ──")
        print(f"  Min distance : {min_d_val:.4f}")
        print(f"  Avg distance : {avg_d:.4f}")
        print(f"  Max distance : {max_d:.4f}")
        print(f"  Lolos threshold ({threshold}) : {would_pass}/{len(distances)}")
        print(f"  Terblokir                    : {would_fail}/{len(distances)}")

    return distances


# ── Ekspor test set ke file ────────────────────────────────────────────
def export_test_set(gap_freq):
    out_path = os.path.join(BASE_DIR, "gap_test_set.json")
    test_set = [
        {"query": q, "frequency": freq, "expected_status": "KNOWLEDGE_GAP"}
        for q, freq in sorted(gap_freq.items(), key=lambda x: -x[1])
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)
    print(f"  ✔ Test set diekspor ke: {out_path}  ({len(test_set)} unique queries)")


# ── "Dirty" in-domain queries (gaya user asli) ────────────────────────
# Kontras dengan benchmark_clean yang lo buat sendiri
DIRTY_IN_DOMAIN = [
    "gimana cara bikin promo di kasir",
    "cara absen karyawan masuk",
    "gimana void nota yang salah",
    "cara daftar gofood shopeefood di sora",
    "aturan service charge pajak gmn",
    "gimana atur stok bahan baku",
    "cara tambah menu baru",
    "caranya batalin pesanan gimana",
    "qrisnya gimana cara settingnya",
    "cara bikin akun sorapos baru",
]

CLEAN_IN_DOMAIN = [
    "bagaimana cara buat promo kasir",
    "cara absen masuk karyawan",
    "bagaimana cara void nota transaksi",
    "bagaimana cara daftar online food gofood shopeefood",
    "aturan service charge dan pb1 pajak",
    "bagaimana cara atur stok bahan baku",
    "bagaimana cara tambah menu baru di kasir",
    "bagaimana cara membatalkan pesanan",
    "bagaimana cara mengatur qris",
    "bagaimana cara mendaftar akun toko",
]


def main():
    THRESHOLD = 0.60  # Sesuaikan dengan nilai aktif di app.py

    print("\n" + "=" * 70)
    print("  ANALISIS GAP & BENCHMARK REPRESENTATIF — SORA ASSISTANT")
    print("=" * 70 + "\n")

    # 1. Load & stats
    conversations = load_logs()
    print_stats(conversations)

    # 2. Load embedding model & ChromaDB
    print("Memuat model embedding & ChromaDB...")
    embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)
    print("  ✔ Model & DB siap.\n")

    # 3. Benchmark clean in-domain (seperti test_threshold.py asli)
    clean_queries = {q: 1 for q in CLEAN_IN_DOMAIN}
    clean_dists = benchmark_queries(clean_queries, embed_model, collection,
                                    "IN-DOMAIN CLEAN (buatan, seperti benchmark lama)", THRESHOLD)

    # 4. Benchmark dirty in-domain (gaya user asli)
    dirty_queries = {q: 1 for q in DIRTY_IN_DOMAIN}
    dirty_dists = benchmark_queries(dirty_queries, embed_model, collection,
                                    "IN-DOMAIN DIRTY (gaya user asli, typo & santai)", THRESHOLD)

    # 5. Ekstrak gap queries dari log
    gap_freq = extract_gap_queries(conversations)
    # Filter: buang sapaan, buang query yang jelas out-of-domain (nasi goreng, dll)
    OOD_KEYWORDS = ["nasi goreng", "cuci mobil", "mesin cuci", "newton", "presiden",
                    "pinjaman", "bank bri", "kaya", "untung banyak"]
    gap_in_scope = {
        q: freq for q, freq in gap_freq.items()
        if not any(kw in q for kw in OOD_KEYWORDS) and len(q) > 10
    }

    print("\n" + "=" * 70)
    print(f" KNOWLEDGE GAP QUERIES DARI LOG ASLI ({len(gap_in_scope)} unique, non-OOD)")
    print("=" * 70)
    gap_dists = benchmark_queries(
        {q: f for q, f in list(gap_in_scope.items())[:30]},  # top 30
        embed_model, collection,
        "REAL USER GAP QUERIES (dari log percakapan aktual)", THRESHOLD
    )

    # 6. Ekspor test set
    print("\n" + "=" * 70)
    print(" EKSPOR TEST SET")
    print("=" * 70)
    export_test_set(gap_in_scope)

    # 7. Perbandingan clean vs dirty max_in
    print("\n" + "=" * 70)
    print(" PERBANDINGAN: CLEAN vs DIRTY IN-DOMAIN BENCHMARK")
    print("=" * 70)
    max_clean = max(clean_dists) if clean_dists else 0
    max_dirty = max(dirty_dists) if dirty_dists else 0
    avg_clean = sum(clean_dists) / len(clean_dists) if clean_dists else 0
    avg_dirty = sum(dirty_dists) / len(dirty_dists) if dirty_dists else 0

    print(f"  Clean max_in (benchmark buatan) : {max_clean:.4f}")
    print(f"  Dirty max_in (gaya user asli)   : {max_dirty:.4f}  ← Lebih representatif")
    print(f"  Clean avg_in                    : {avg_clean:.4f}")
    print(f"  Dirty avg_in                    : {avg_dirty:.4f}")
    print()
    if max_dirty > max_clean:
        delta = max_dirty - max_clean
        print(f"  ⚠️  Gap: dirty max_in lebih tinggi {delta:.4f} dari clean max_in.")
        print(f"     Ini artinya kalkulasi 'safe zone' berdasarkan clean benchmark")
        print(f"     kemungkinan under-estimate batas atas in-domain yang sesungguhnya.")
        new_rec = round((max_dirty + 0.6141) / 2, 2)  # pakai OOD floor lama
        if new_rec < max_dirty:
            new_rec = round(max_dirty + 0.03, 2)
        print(f"\n  REKOMENDASI THRESHOLD BARU (dari dirty benchmark): {new_rec:.2f}")
        print(f"  Nilai aktif saat ini                            : {THRESHOLD}")
        if new_rec > THRESHOLD:
            print(f"  → Pertimbangkan naikkan threshold ke {new_rec} untuk reduce false rejection")
        else:
            print(f"  → Threshold saat ini masih aman.")
    print()
    print("  Selanjutnya:")
    print("  1. Periksa gap_test_set.json — jadikan test set resmi setelah re-ingest")
    print("  2. Uji injection yang 'dibungkus legit': python test_injection.py (buat menyusul)")
    print("  3. Debug QRIS: cek chunking dokumen QRIS vs cara user nanya")
    print("=" * 70)


if __name__ == "__main__":
    main()
