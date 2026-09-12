"""
validate_docs.py
----------------
Linter dan validator dokumentasi untuk proyek riset OKF vs RAG.

Fungsi utama:
1. Memastikan skema YAML frontmatter di system-rag/docs/ dan system-okf/docs/ valid.
2. Memastikan jumlah dokumen tepat 36 di kedua folder.
3. Memastikan semua tautan (prerequisites dan related) di system-okf/docs/ terhubung ke ID dokumen yang valid.
4. Memastikan kesetaraan teks (informational parity) antara system-rag/docs/ dan system-okf/docs/.
"""

import os
import sys
import re
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "docs-shared-schema", "knowledge_schema.yaml")
RAG_DOCS_DIR = os.path.join(BASE_DIR, "system-rag", "docs")
OKF_DOCS_DIR = os.path.join(BASE_DIR, "system-okf", "docs")

REQUIRED_COUNT = 36


def parse_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content.strip(), "Frontmatter missing or invalid header delimiter"

    yaml_str = match.group(1)
    body = match.group(2).strip()

    try:
        data = yaml.safe_load(yaml_str)
        return data, body, None
    except Exception as e:
        return None, body, f"YAML parsing error: {e}"


def run_validation():
    print("=" * 70)
    print("  VALIDASI DOKUMENTASI SORA POS (OKF VS RAG)")
    print("=" * 70)

    errors = []

    # 1. Load schema rules
    if not os.path.exists(SCHEMA_PATH):
        errors.append(f"Schema file not found at: {SCHEMA_PATH}")

    # 2. Check document counts
    rag_files = [f for f in os.listdir(RAG_DOCS_DIR) if f.endswith(".md")] if os.path.exists(RAG_DOCS_DIR) else []
    okf_files = [f for f in os.listdir(OKF_DOCS_DIR) if f.endswith(".md")] if os.path.exists(OKF_DOCS_DIR) else []

    print(f"  - Document Count system-rag/docs : {len(rag_files)} (target: {REQUIRED_COUNT})")
    print(f"  - Document Count system-okf/docs : {len(okf_files)} (target: {REQUIRED_COUNT})")

    if len(rag_files) != REQUIRED_COUNT:
        errors.append(f"system-rag/docs count is {len(rag_files)}, expected {REQUIRED_COUNT}")
    if len(okf_files) != REQUIRED_COUNT:
        errors.append(f"system-okf/docs count is {len(okf_files)}, expected {REQUIRED_COUNT}")

    # 3. Parse frontmatter & gather document IDs
    rag_docs = {}
    okf_docs = {}

    for fname in rag_files:
        fpath = os.path.join(RAG_DOCS_DIR, fname)
        fm, body, err = parse_frontmatter(fpath)
        if err:
            errors.append(f"[RAG] {fname}: {err}")
        else:
            rag_docs[fname] = {"fm": fm, "body": body, "path": fpath}

    for fname in okf_files:
        fpath = os.path.join(OKF_DOCS_DIR, fname)
        fm, body, err = parse_frontmatter(fpath)
        if err:
            errors.append(f"[OKF] {fname}: {err}")
        else:
            okf_docs[fname] = {"fm": fm, "body": body, "path": fpath}

    # Extract all OKF IDs
    okf_ids = set()
    for fname, d in okf_docs.items():
        doc_id = d["fm"].get("id")
        if not doc_id:
            errors.append(f"[OKF] {fname}: Missing 'id' field in frontmatter")
        else:
            okf_ids.add(doc_id)

    # 4. Validate OKF links (prerequisites & related)
    for fname, d in okf_docs.items():
        fm = d["fm"]
        doc_id = fm.get("id", fname)

        # Check required fields
        for req_field in ["id", "title", "category", "target_role", "tags"]:
            if req_field not in fm:
                errors.append(f"[OKF] {fname}: Missing required field '{req_field}'")

        prereqs = fm.get("prerequisites", [])
        related = fm.get("related", [])

        if not isinstance(prereqs, list):
            errors.append(f"[OKF] {fname}: 'prerequisites' must be a list")
        else:
            for pid in prereqs:
                if pid not in okf_ids:
                    errors.append(f"[OKF] {fname} ({doc_id}): Broken prerequisite link '{pid}'")

        if not isinstance(related, list):
            errors.append(f"[OKF] {fname}: 'related' must be a list")
        else:
            for rid in related:
                if rid not in okf_ids:
                    errors.append(f"[OKF] {fname} ({doc_id}): Broken related link '{rid}'")

    # 5. Check Parity between RAG and OKF
    for fname in rag_files:
        if fname not in okf_docs:
            errors.append(f"File '{fname}' present in system-rag/docs but missing in system-okf/docs")
            continue

        rag_body = rag_docs[fname]["body"]
        okf_body = okf_docs[fname]["body"]

        if rag_body != okf_body:
            errors.append(f"Content mismatch between system-rag/docs/{fname} and system-okf/docs/{fname}")

    print("=" * 70)
    if errors:
        print(f"❌ VALIDASI GAGAL! Ditemukan {len(errors)} masalah:\n")
        for err in errors:
            print(f"  • {err}")
        print("=" * 70)
        sys.exit(1)
    else:
        print("✅ VALIDASI SUKSES! Semua 36 dokumen valid & paralel 100%.")
        print("=" * 70)
        sys.exit(0)


if __name__ == "__main__":
    run_validation()
