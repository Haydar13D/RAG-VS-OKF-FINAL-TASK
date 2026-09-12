"""
shared/query_normalizer.py
---------------------------
Satu sumber kebenaran (Single Source of Truth) untuk normalisasi query dan koreksi typo.
Digunakan secara IDENTIK oleh system-rag, system-okf, dan root app server.

PENTING UNTUK METODOLOGI SKRIPSI:
Module ini mengekstrak `normalize_query()` dari `system-rag/app.py` beserta seluruh 15 aturan
regex typo map dan aturan query expansion langganan agar tidak ada bias/confounding variable
saat membandingkan akurasi RAG vs OKF.
"""

import re

# Dictionary typo_map yang Otentik dan Lengkap dari RAG pipeline (system-rag/app.py & app.py)
TYPO_MAP = {
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
    r"\bsistme\b": "sistem",
    r"\bitus osra\b": "itu sora",
    r"\bosra\b": "sora",
}


def normalize_query(query: str) -> str:
    """
    Normalisasi query: lowercase + pembersihan typo + query expansion.
    HARUS dipanggil dengan cara yang SAMA PERSIS di system-rag, system-okf, dan root app.
    """
    normalized = query.lower().strip()

    for pattern, replacement in TYPO_MAP.items():
        normalized = re.sub(pattern, replacement, normalized)

    # Query expansion untuk topik langganan (pastikan bukan 'pelanggan')
    clean_for_sub = re.sub(r"\b(pelanggan|pelangganan)\b", "", normalized)
    if re.search(r"\b(langganan|subscription|berlangganan|perpanjang masa aktif|perpanjang langganan)\b", clean_for_sub):
        normalized += " sistem paket langganan subscription perpanjangan masa aktif toko sora coin"

    return normalized
