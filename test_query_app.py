import sys
from app import retrieve_context

sys.stdout.reconfigure(encoding='utf-8')

queries = [
    "jelaskan sistem langganan",
    "sistme langganan",
    "sistem langganan",
    "apa itus osra coin",
    "coba jelaskan sistem langganan",
    "apa itu langganan"
]

for q in queries:
    chunks, min_dist = retrieve_context(q)
    print(f"Query: '{q}'")
    print(f"  Min Distance: {min_dist:.4f} (Threshold: 0.60)")
    print(f"  Lolos Filter: {len(chunks) > 0}")
    if chunks:
        doc, meta = chunks[0]
        print(f"  Top Match Title: {meta.get('title')}")
    else:
        print("  Top Match Title: NONE (TERTOLAK / KNOWLEDGE GAP)")
    print("-" * 60)
