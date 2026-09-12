import os
import sys
import json
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "system-okf"))
from okf_navigator import OKFNavigator, INDONESIAN_STOP_WORDS
from shared.query_normalizer import normalize_query

nav = OKFNavigator(min_entry_score=0)

queries = [
    ("In-Domain Clean", "bagaimana cara membuat promo kasir"),
    ("In-Domain Dirty", "gimana void nota yang salah"),
    ("In-Domain Dirty", "caranya batalin pesanan gimana"),
    ("In-Domain Dirty", "cara bikin akun sorapos baru"),
    ("In-Domain Specific", "bagaimana cara mengatur qris"),
    ("In-Domain Specific", "apakah sora seventh terhubung dengan gofood"),
    ("Out-of-Domain", "siapa presiden Indonesia"),
    ("Out-of-Domain", "resep membuat nasi goreng enak"),
    ("Out-of-Domain", "bagaimana cara install python di windows"),
    ("Out-of-Domain", "berapa harga saham google hari ini"),
    ("Out-of-Domain", "cuaca hari ini di jakarta"),
]

print("=" * 80)
print(f"{'TYPE':<20} | {'MAX SCORE':<10} | {'TOP DOC MATCHED':<30} | {'QUERY'}")
print("=" * 80)

for q_type, q in queries:
    norm_q = normalize_query(q)
    raw_words = set(re.findall(r"\w+", norm_q))
    q_kw = {w for w in raw_words if w not in INDONESIAN_STOP_WORDS and len(w) > 1}

    scores = []
    for doc_id, doc in nav.documents.items():
        fm = doc["fm"]
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        category = fm.get("category", "")
        title = fm.get("title", "")

        score = 0
        if category.lower() in q_kw:
            score += 3
        for t in tags:
            tw = {w for w in re.findall(r"\w+", t.lower()) if w not in INDONESIAN_STOP_WORDS}
            mc = len(tw.intersection(q_kw))
            if mc > 0:
                score += mc * 2
        title_words = {w for w in re.findall(r"\w+", title.lower()) if w not in INDONESIAN_STOP_WORDS}
        score += len(title_words.intersection(q_kw))

        if score > 0:
            scores.append((score, doc_id))

    scores.sort(key=lambda x: x[0], reverse=True)
    max_score = scores[0][0] if scores else 0
    top_doc = scores[0][1] if scores else "NONE (REFUSAL)"
    print(f"{q_type:<20} | {max_score:<10} | {top_doc:<30} | {q}")

print("=" * 80)
