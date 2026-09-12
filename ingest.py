"""
ingest.py
Baca semua file .md di folder docs/, potong jadi chunk, embed, simpan ke ChromaDB.

Cara pakai:
    python ingest.py

Jalankan ini setiap kali dokumentasi di folder docs/ berubah/nambah.
"""

import os
import re
import glob
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cek lokasi folder docs secara fleksibel (apakah di ./docs atau ../docs)
LOCAL_DOCS = os.path.join(BASE_DIR, "docs")
PARENT_DOCS = os.path.abspath(os.path.join(BASE_DIR, "..", "docs"))

if os.path.exists(LOCAL_DOCS) and len(os.listdir(LOCAL_DOCS)) > 0:
    DOCS_DIR = LOCAL_DOCS
elif os.path.exists(PARENT_DOCS):
    DOCS_DIR = PARENT_DOCS
else:
    DOCS_DIR = LOCAL_DOCS

DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pos_knowledge"
CHUNK_SIZE = 800       # karakter per chunk (bukan token, tapi cukup buat awal)
CHUNK_OVERLAP = 150

# Model embedding open-source, ringan, jalan di CPU tanpa masalah.
# Multilingual jadi cukup oke untuk Bahasa Indonesia.
EMBED_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


try:
    import yaml
except ImportError:
    yaml = None


def parse_yaml_content(content: str) -> str:
    """Mengubah isi YAML menjadi teks terstruktur yang mudah dipahami model embedding."""
    if yaml:
        try:
            data = yaml.safe_load(content)
            if data:
                return yaml_to_text(data)
        except Exception:
            pass
    # Fallback jika PyYAML tidak ada atau gagal
    clean_lines = []
    for line in content.splitlines():
        if line.strip() and not line.strip().startswith("#"):
            clean_lines.append(line)
    return "\n".join(clean_lines)


def yaml_to_text(data, indent=0) -> str:
    """Mengubah dict/list dari YAML menjadi teks deskriptif yang rapi."""
    lines = []
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            key_name = str(key).replace("_", " ").title()
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}**{key_name}**:")
                lines.append(yaml_to_text(value, indent + 1))
            else:
                lines.append(f"{prefix}- **{key_name}**: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(yaml_to_text(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{data}")
    return "\n".join(lines)


def read_docs():
    patterns = [
        os.path.join(DOCS_DIR, "**/*.md"),
        os.path.join(DOCS_DIR, "**/*.yaml"),
        os.path.join(DOCS_DIR, "**/*.yml"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p, recursive=True))

    docs = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(path)
        ext = os.path.splitext(filename)[1].lower()
        title = filename
        tags = []

        if ext in [".yaml", ".yml"]:
            # Format file YAML menjadi deskripsi teks terstruktur + raw content
            readable_text = parse_yaml_content(content)
            body = f"DOKUMEN FITUR & OPERASIONAL POS SORA SEVENTH ({filename}):\n\n{readable_text}\n\n[Raw Structure]:\n{content}"
            tags = ["yaml", "fitur", "operasional", filename.replace(".yaml", "").replace(".yml", "")]
        else:
            # File .md
            m = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
            if m:
                frontmatter, body = m.group(1), m.group(2)
                title_match = re.search(r"title:\s*(.+)", frontmatter)
                if title_match:
                    title = title_match.group(1).strip()
                tags_match = re.search(r"tags:\s*\[(.*?)\]", frontmatter)
                if tags_match:
                    tags = [t.strip() for t in tags_match.group(1).split(",") if t.strip()]
            else:
                body = content

        docs.append({"source": path, "title": title, "tags": tags, "text": body.strip()})
    return docs


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return [c.strip() for c in chunks if c.strip()]


def main():
    print("Membaca dokumen dari folder docs/ ...")
    docs = read_docs()
    if not docs:
        print(f"WARNING: tidak ada file .md ditemukan di folder '{DOCS_DIR}/'. "
              f"Tambahkan dokumentasi dulu sebelum lanjut.")
        return

    print(f"Ditemukan {len(docs)} dokumen. Memecah jadi chunk ...")
    all_chunks = []
    all_metadatas = []
    all_ids = []
    chunk_id = 0
    for doc in docs:
        chunks = chunk_text(doc["text"])
        tags_str = ", ".join(doc.get("tags", []))
        for c in chunks:
            context_chunk = f"Document Title: {doc['title']}\nTags: {tags_str}\nContent:\n{c}"
            all_chunks.append(context_chunk)
            all_metadatas.append({
                "source": doc["source"],
                "title": doc["title"],
                "tags": tags_str
            })
            all_ids.append(f"chunk_{chunk_id}")
            chunk_id += 1

    print(f"Total {len(all_chunks)} chunk. Memuat model embedding "
          f"({EMBED_MODEL_NAME}) ...")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    print("Membuat embedding ...")
    embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()

    print("Menyimpan ke ChromaDB ...")
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=all_ids,
        embeddings=embeddings,
        documents=all_chunks,
        metadatas=all_metadatas,
    )

    print(f"Selesai. {len(all_chunks)} chunk tersimpan di '{DB_DIR}/'.")


if __name__ == "__main__":
    main()