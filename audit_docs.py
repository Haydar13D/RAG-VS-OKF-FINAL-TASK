import os
import re
import sys
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Cek folder docs di root dan di system-okf/docs
target_dirs = []
if os.path.exists("docs"):
    target_dirs.append("docs")
if os.path.exists("system-okf/docs"):
    target_dirs.append("system-okf/docs")

for docs_dir in target_dirs:
    print("=" * 80)
    print(f"  AUDIT DOKUMENTASI & FRONTMATTER LINKING: {docs_dir}")
    print("=" * 80)

    doc_map = {}
    files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]

    for fname in sorted(files):
        fpath = os.path.join(docs_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if match:
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except Exception as e:
                print(f"[ERROR] YAML Frontmatter Rusak di {fname}: {e}")
                fm = {}
        else:
            fm = {}

        doc_id = fm.get("id", fname.replace(".md", ""))
        prereqs = fm.get("prerequisites", []) or []
        related = fm.get("related", []) or []
        tags = fm.get("tags", []) or []

        if isinstance(prereqs, str):
            prereqs = [prereqs]
        if isinstance(related, str):
            related = [related]
        if isinstance(tags, str):
            tags = [tags]

        doc_map[doc_id] = {
            "file": fname,
            "id": doc_id,
            "title": fm.get("title", "NO_TITLE"),
            "category": fm.get("category", "NO_CATEGORY"),
            "tags": tags,
            "prerequisites": prereqs,
            "related": related,
        }

    all_registered_ids = set(doc_map.keys())

    broken_prereqs = []
    broken_related = []
    referenced_ids = set()

    for doc_id, info in doc_map.items():
        for p in info["prerequisites"]:
            referenced_ids.add(p)
            if p not in all_registered_ids:
                broken_prereqs.append((info["file"], doc_id, p))

        for r in info["related"]:
            referenced_ids.add(r)
            if r not in all_registered_ids:
                broken_related.append((info["file"], doc_id, r))

    print(f"Total File Markdown: {len(files)}")
    print(f"Total Registered Document IDs: {len(all_registered_ids)}")
    print("-" * 80)

    # 1. Broken Links Check
    if broken_prereqs:
        print(f"\n❌ TERDETEKSI {len(broken_prereqs)} BROKEN PREREQUISITES LINK:")
        for fname, did, target in broken_prereqs:
            print(f"   - File: {fname} (ID: '{did}') -> Prerequisite 'ID: {target}' TIDAK DITEMUKAN!")
    else:
        print("\n✅ Prerequisites Links: ALL VALID (0 broken links)")

    if broken_related:
        print(f"\n❌ TERDETEKSI {len(broken_related)} BROKEN RELATED LINK:")
        for fname, did, target in broken_related:
            print(f"   - File: {fname} (ID: '{did}') -> Related 'ID: {target}' TIDAK DITEMUKAN!")
    else:
        print("✅ Related Links: ALL VALID (0 broken links)")

    # 2. Duplicate IDs Check
    id_counts = {}
    for info in doc_map.values():
        id_counts[info["id"]] = id_counts.get(info["id"], 0) + 1
    dup_ids = [did for did, cnt in id_counts.items() if cnt > 1]
    if dup_ids:
        print(f"\n❌ TERDETEKSI DUPLICATE DOCUMENT ID: {dup_ids}")
    else:
        print("✅ Document IDs Uniqueness: ALL UNIQUE (0 duplicate IDs)")

    # 3. Structural Link Consistency Check
    print("-" * 80)
    print("DAFTAR DETAIL DOKUMEN & RELASINYA:")
    for did in sorted(doc_map.keys()):
        d = doc_map[did]
        p_str = ", ".join(d["prerequisites"]) if d["prerequisites"] else "-"
        r_str = ", ".join(d["related"]) if d["related"] else "-"
        print(f"[{did}] {d['title']} ({d['file']})")
        print(f"   - Category: {d['category']}")
        print(f"   - Tags    : {d['tags']}")
        print(f"   - Prereqs : {p_str}")
        print(f"   - Related : {r_str}")

print("\n" + "=" * 80)
print("AUDIT DOKUMENTASI SELESAI")
print("=" * 80)
