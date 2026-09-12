"""
system-okf/okf_context_stuffing.py  (PATCHED)
----------------------------------
Varian pembanding opsional untuk OKF: Context-Stuffing.
Memuat seluruh dokumen ke context window sekaligus.

PERUBAHAN dari versi sebelumnya:
- SEBELUM: memasukkan raw file content APA ADANYA, termasuk seluruh
  YAML frontmatter (id, title, category, tags, dll) mentah ke context
  yang dikirim ke LLM -- ini kebocoran informasi internal yang lebih
  parah dari kasus D1 sebelumnya.
- SESUDAH: parse frontmatter dulu, HANYA body (isi dokumen) yang masuk
  ke context. Metadata tetap bisa dipakai untuk logging/nav_metadata,
  tapi TIDAK PERNAH ikut terkirim ke LLM.
"""

import os

from okf_navigator import parse_doc  # reuse parser yang sama, jangan duplikat logic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def get_all_stuffed_context(docs_dir: str = DOCS_DIR) -> str:
    if not os.path.exists(docs_dir):
        return ""

    chunks = []
    for fname in sorted(os.listdir(docs_dir)):
        if fname.endswith(".md"):
            fpath = os.path.join(docs_dir, fname)
            fm, body = parse_doc(fpath)
            if body:
                chunks.append(body)  # HANYA body, frontmatter tidak ikut

    return "\n\n---\n\n".join(chunks)