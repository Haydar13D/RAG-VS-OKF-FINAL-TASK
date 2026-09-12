import os
import sys
import re
import chromadb
from sentence_transformers import SentenceTransformer

# Standardize UTF-8 stdout encoding for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_DIR = "chroma_db"
COLLECTION_NAME = "pos_knowledge"
EMBED_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

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

def run_benchmark():
    print("Memuat embedding model & ChromaDB...")
    embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    in_domain_queries = [
        "bagaimana cara buat promo kasir",
        "cara absen masuk karyawan",
        "bagaimana cara void nota transaksi",
        "bagaimana cara daftar online food gofood shopeefood",
        "aturan service charge dan pb1 pajak",
        "bagaimana cara atur stok bahan baku",
        "bagaimana cara tambah menu baru di kasir",
    ]

    out_of_domain_queries = [
        "bagaimana cara cuci mobil sedan",
        "resep memasak nasi goreng jawa enak",
        "bagaimana cara ajukan pinjaman modal bank bri",
        "siapa presiden indonesia pertama",
        "cara memperbaiki mesin cuci rusak",
        "apa rumus fisika hukum newton 2",
    ]

    print("\n" + "="*70)
    print(" 1. BENCHMARK PERTANYAAN IN-DOMAIN (DOKUMENTASI ADA)")
    print("="*70)

    in_distances = []
    for q in in_domain_queries:
        search_q = normalize_query(q)
        q_emb = embed_model.encode([search_q]).tolist()
        res = collection.query(query_embeddings=q_emb, n_results=3, include=["documents", "distances", "metadatas"])
        dists = res.get("distances", [[]])[0]
        min_d = min(dists) if dists else 1.0
        in_distances.append(min_d)
        doc_title = res.get("metadatas", [[]])[0][0].get("title", "unknown") if res.get("metadatas") else "none"
        print(f"Query : '{q}'")
        print(f"  |- Distance Terdekat: {min_d:.4f} (Doc: {doc_title})\n")

    print("="*70)
    print(" 2. BENCHMARK PERTANYAAN OUT-OF-DOMAIN (TIDAK ADA DI DOKUMEN)")
    print("="*70)

    out_distances = []
    for q in out_of_domain_queries:
        search_q = normalize_query(q)
        q_emb = embed_model.encode([search_q]).tolist()
        res = collection.query(query_embeddings=q_emb, n_results=3, include=["documents", "distances", "metadatas"])
        dists = res.get("distances", [[]])[0]
        min_d = min(dists) if dists else 1.0
        out_distances.append(min_d)
        doc_title = res.get("metadatas", [[]])[0][0].get("title", "unknown") if res.get("metadatas") else "none"
        print(f"Query : '{q}'")
        print(f"  |- Distance Terdekat: {min_d:.4f} (Doc Terdekat: {doc_title})\n")

    avg_in = sum(in_distances) / len(in_distances)
    avg_out = sum(out_distances) / len(out_distances)
    max_in = max(in_distances)
    min_out = min(out_distances)

    print("="*70)
    print(" RINGKASAN REKOMENDASI THRESHOLD")
    print("="*70)
    print(f"Distance Max In-Domain     : {max_in:.4f}")
    print(f"Distance Avg In-Domain     : {avg_in:.4f}")
    print(f"Distance Min Out-Of-Domain : {min_out:.4f}")
    print(f"Distance Avg Out-Of-Domain : {avg_out:.4f}")

    suggested_threshold = round((max_in + min_out) / 2, 2)
    if suggested_threshold < max_in:
        suggested_threshold = round(max_in + 0.03, 2)

    print(f"\nREKOMENDASI MAX_DISTANCE_THRESHOLD TERKETAT: {suggested_threshold:.2f}")

if __name__ == "__main__":
    run_benchmark()
