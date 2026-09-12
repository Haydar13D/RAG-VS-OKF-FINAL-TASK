"""
system-rag/ingest.py
--------------------
Membaca 36 dokumen dari system-rag/docs/, mengekstrak frontmatter + body,
membuat embedding menggunakan paraphrase-multilingual-MiniLM-L12-v2,
dan menyimpannya ke ChromaDB lokal di system-rag/chroma_db/.
"""

import os
import sys
import re
import yaml
import chromadb
from sentence_transformers import SentenceTransformer

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pos_knowledge"
EMBED_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def parse_doc(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        fm = yaml.safe_load(match.group(1)) or {}
        body = match.group(2).strip()
    else:
        fm = {}
        body = content.strip()

    return fm, body


def ingest():
    print("=" * 70)
    print("  SYSTEM RAG — INGESTION DOKUMEN KE CHROMADB")
    print("=" * 70)

    if not os.path.exists(DOCS_DIR):
        print(f"ERROR: Folder dokumen tidak ditemukan di {DOCS_DIR}")
        sys.exit(1)

    doc_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    print(f"Ditemukan {len(doc_files)} dokumen di {DOCS_DIR}")

    print(f"Memuat model embedding '{EMBED_MODEL_NAME}'...")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    print(f"Menyambung ke ChromaDB di {DB_DIR}...")
    client = chromadb.PersistentClient(path=DB_DIR)

    # Re-create collection to ensure clean state
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' lama dihapus.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    documents = []
    metadatas = []
    ids = []

    for fname in doc_files:
        fpath = os.path.join(DOCS_DIR, fname)
        fm, body = parse_doc(fpath)

        doc_id = fm.get("id", fname.replace(".md", ""))
        title = fm.get("title", fname)
        category = fm.get("category", "general")
        tags = fm.get("tags", [])
        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)

        # Chunk content: Frontmatter header info + document body
        text_content = f"Judul: {title}\nKategori: {category}\nTags: {tags_str}\n\n{body}"

        documents.append(text_content)
        metadatas.append({
            "id": doc_id,
            "title": title,
            "category": category,
            "tags": tags_str,
            "file": fname
        })
        ids.append(doc_id)

    print(f"Membuat embeddings untuk {len(documents)} dokumen...")
    embeddings = model.encode(documents).tolist()

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print("=" * 70)
    print(f"✅ INGESTION RAG SUKSES! {len(documents)} dokumen tersimpan di ChromaDB.")
    print("=" * 70)


if __name__ == "__main__":
    ingest()
