"""
system-okf/okf_navigator.py  (PATCHED)
---------------------------
Mekanisme Navigasi Tautan Eksplisit untuk Open Knowledge Format (OKF).

PERUBAHAN dari versi sebelumnya:
1. Pakai shared.query_normalizer.normalize_query() -- SAMA PERSIS dengan
   yang dipakai system-rag, supaya perbandingan tidak bias oleh
   preprocessing yang berbeda.
2. Tambah MIN_ENTRY_SCORE -- sebelumnya "score > 0" terlalu longgar,
   sekarang ada ambang minimum yang bisa dikalibrasi (lihat catatan di
   bawah soal cara kalibrasinya).
3. Tambah try/except di parse_doc -- dokumen dengan frontmatter YAML
   rusak tidak lagi bikin sistem crash, cukup di-skip + di-log.

ATURAN MUTLAK (tidak berubah):
- TIDAK ADA vector database (ChromaDB), TIDAK ADA embeddings, TIDAK ADA
  cosine similarity search.
"""

import os
import re
import sys
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Tambahkan folder root project ke path supaya bisa import shared/
sys.path.insert(0, os.path.join(BASE_DIR, ".."))
from shared.query_normalizer import normalize_query  # noqa: E402

INDONESIAN_STOP_WORDS = {
    "bagaimana", "gimana", "cara", "apa", "apakah", "di", "ke", "dari", "yang",
    "untuk", "dan", "atau", "ini", "itu", "dengan", "bisa", "sudah", "tolong",
    "mohon", "saya", "kamu", "anda", "iya", "oh", "btw", "haloo", "halo", "hai"
}

# CATATAN KALIBRASI:
# Berdasarkan hasil kalibrasi empiris (In-Domain min score = 8 vs Out-of-Domain max score = 2):
# Nilai MIN_ENTRY_SCORE = 5 memberikan margin keamanan yang ideal (delta = 5)
# untuk memisahkan pertanyaan in-domain dari out-of-domain noise.
MIN_ENTRY_SCORE = 3
MAX_TOTAL_DOCS  = 5  # Hard cap total dokumen yang dikumpulkan per-query.
                     # Tanpa cap ini, 1-depth expansion bisa menarik 10+ dokumen
                     # -> context bloat -> latensi 40s+. Nilai 5 = 3 entry + 2 linked.



def parse_doc(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"WARNING [OKFNavigator]: Gagal baca file {file_path}: {e}")
        return {}, ""

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"WARNING [OKFNavigator]: Frontmatter YAML rusak di {file_path}: {e}")
            fm = {}
        body = match.group(2).strip()
    else:
        fm = {}
        body = content.strip()

    return fm, body


class OKFNavigator:
    def __init__(self, docs_dir: str = DOCS_DIR, min_entry_score: int = MIN_ENTRY_SCORE, max_total_docs: int = MAX_TOTAL_DOCS):
        self.docs_dir       = docs_dir
        self.min_entry_score = min_entry_score
        self.max_total_docs  = max_total_docs
        self.documents = {}  # doc_id -> {"fm": fm, "body": body, "file": fname}
        self.load_documents()

    def load_documents(self):
        self.documents.clear()
        if not os.path.exists(self.docs_dir):
            print(f"WARNING [OKFNavigator]: Folder {self.docs_dir} tidak ditemukan.")
            return

        skipped = []
        for fname in os.listdir(self.docs_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(self.docs_dir, fname)
                fm, body = parse_doc(fpath)
                if not fm and not body:
                    skipped.append(fname)
                    continue
                doc_id = fm.get("id", fname.replace(".md", ""))
                self.documents[doc_id] = {
                    "id": doc_id,
                    "fm": fm,
                    "body": body,
                    "file": fname
                }
        print(f"[OKFNavigator] Memuat {len(self.documents)} dokumen terstruktur.")
        if skipped:
            print(f"[OKFNavigator] {len(skipped)} file di-skip karena gagal parse: {skipped}")

    def navigate(self, query: str, max_entry_docs: int = 3) -> tuple[list[dict], dict]:
        """
        Melakukan pencarian entry point + 1-depth link expansion.
        Query di-normalize dulu pakai preprocessing yang SAMA dengan RAG.
        """
        normalized_query = normalize_query(query)

        raw_words = set(re.findall(r"\w+", normalized_query))
        query_keywords = {w for w in raw_words if w not in INDONESIAN_STOP_WORDS and len(w) > 1}

        if not query_keywords:
            return [], {
                "status": "KNOWLEDGE_GAP",
                "entry_docs": [],
                "linked_docs": [],
                "total_docs": 0,
                "reason": "no_keywords_after_normalization",
            }

        # 1. Entry point keyword matching against tags dan category
        scored_entries = []
        for doc_id, doc in self.documents.items():
            fm = doc["fm"]
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            category = fm.get("category", "")
            title = fm.get("title", "")

            score = 0
            if category.lower() in query_keywords:
                score += 3

            for tag in tags:
                tag_words = {w for w in re.findall(r"\w+", tag.lower()) if w not in INDONESIAN_STOP_WORDS}
                match_count = len(tag_words.intersection(query_keywords))
                if match_count > 0:
                    score += match_count * 2

            title_words = {w for w in re.findall(r"\w+", title.lower()) if w not in INDONESIAN_STOP_WORDS}
            score += len(title_words.intersection(query_keywords))

            # PERUBAHAN: pakai MIN_ENTRY_SCORE, bukan "score > 0"
            if score >= self.min_entry_score:
                scored_entries.append((score, doc_id))

        scored_entries.sort(key=lambda x: x[0], reverse=True)

        if not scored_entries:
            return [], {
                "status": "KNOWLEDGE_GAP",
                "entry_docs": [],
                "linked_docs": [],
                "total_docs": 0,
                "reason": f"no_match_above_min_score_{self.min_entry_score}",
            }

        entry_doc_ids = [doc_id for score, doc_id in scored_entries[:max_entry_docs]]

        # 2. 1-Depth Link Expansion via prerequisites & related
        collected_ids = set(entry_doc_ids)
        linked_doc_ids = set()

        for doc_id in entry_doc_ids:
            fm = self.documents[doc_id]["fm"]
            prereqs = fm.get("prerequisites", [])
            related = fm.get("related", [])

            for link_id in prereqs + related:
                if link_id in self.documents and link_id not in collected_ids:
                    linked_doc_ids.add(link_id)
                    collected_ids.add(link_id)

        gathered_docs = [self.documents[did] for did in collected_ids if did in self.documents]

        # Hard cap: batasi jumlah dokumen yang dikirim ke LLM untuk mencegah context bloat.
        # Urutan prioritas: entry docs dulu, baru linked docs.
        if len(gathered_docs) > self.max_total_docs:
            priority_order = entry_doc_ids + [d for d in collected_ids if d not in entry_doc_ids]
            gathered_docs  = [
                self.documents[did] for did in priority_order
                if did in self.documents
            ][:self.max_total_docs]

        nav_metadata = {
            "status":      "NAVIGATED",
            "entry_docs":  entry_doc_ids,
            "linked_docs": list(linked_doc_ids),
            "total_docs":  len(gathered_docs),
            "capped":      len(gathered_docs) < len(collected_ids),  # flag jika ada dokumen yang di-cap
        }

        return gathered_docs, nav_metadata