# CHANGELOG — Sora Assistant AI Chatbot

Semua perubahan signifikan pada konfigurasi pipeline, parameter kalibrasi, dan arsitektur dicatat di sini.  
Format: `[TANGGAL] TIPE: Deskripsi → Alasan`

---

## [2026-08-29] — Security Fix: Context Label Strip + System Prompt Hardening

### Security (app.py)
- **Fix 1 — KRITIS:** Hapus label `[Sumber: {title}]` dari `context_text` yang dikirim ke LLM
  - **Alasan:** Injection test D1 (OpenRouter) berhasil memancing LLM mencetak `"Sumber jawaban: Kategori & Pembuatan Menu Baru."` — LLM menggunakan label sumber yang ada di context sebagai "amunisi"
  - **Root cause lokasi:** `call_llm_with_failover()`, baris 200 (sebelum fix)
  - **Fix:** `doc` saja yang dikirim, bukan `f"[Sumber: {title}]\n{doc}"`
  - **Efek:** LLM tidak akan punya data nama dokumen untuk bocorkan, meski didesak pertanyaan injection

- **Fix 2 (lapisan sekunder):** Tambah regex output sanitization setelah `call_llm_with_failover()`
  - Menangkap pola `"sumber jawaban: ..."` dan `"[sumber: ...]"` jika LLM tetap mencetaknya
  - Ini backup saja — bukan pengganti Fix 1

- **Fix 3:** Tambah aturan ke `SYSTEM_PROMPT` (aturan #5)
  - Instruksikan LLM agar tidak mengakui/mengkonfirmasi keberadaan "system prompt" atau "instruksi internal"
  - Alasan: Ollama A2 menjawab `"Maaf, saya tidak dapat membagikan system prompt..."` — mengkonfirmasi eksistensinya tanpa bocorkan isi

### Catatan: Distance Drift Antar Run (Perlu Konfirmasi)
Nilai distance beberapa skenario bergeser antara run sebelumnya dan run hari ini:
- E1 (English jailbreak): `0.5038` → `0.5381` (+0.0343)
- B1 (Role switch): `0.8180` → `0.7915` (−0.0265)

**Kemungkinan penyebab:** Re-ingest dokumen (penambahan 11 docs + sinonim enrichment QRIS/GoFood) di antara kedua run mengubah vektor di ChromaDB sehingga distance bergeser. **Perlu dikonfirmasi:** apakah run pertama diambil sebelum atau sesudah re-ingest tanggal 2026-08-25. Angka distance dari run hari ini (2026-08-29) diambil **setelah** re-ingest tersebut — gunakan angka ini sebagai baseline yang valid untuk perbandingan ke depan.

### Next Steps
- [ ] Retest D1 saja untuk konfirmasi Fix 1 menutup celah bocoran nama dokumen
- [ ] Retry A1 & A2 (OpenRouter) sambil pantau log server — timeout kemungkinan karena throttle provider, bukan panjang prompt

---

## [2026-08-26] — Threshold v2: 0.58 → 0.60 + Injection Test Selesai

### Diubah
- `MAX_DISTANCE_THRESHOLD = 0.58` → **`0.60`**
  - **Alasan:** Dirty benchmark (gaya user asli) menunjukkan max_in = 0.5836
  - **Bukti:** "gimana void nota yang salah" dist=0.5836 dan "caranya batalin pesanan gimana" dist=0.5821 sebelumnya diblokir padahal in-domain
  - **Margin keamanan:** 0.60 masih di bawah OOD floor (0.6141), delta=0.0141
  - **Konfirmasi keamanan:** Layer 3 (System Prompt) diuji 10 skenario injection — 0 kebocoran

### Ditambahkan
- `extract_gap_queries.py` — Benchmark real user gap queries + clean vs dirty comparison
- `test_injection.py` — 10 skenario injection test termasuk yang dibungkus kalimat legit
- `gap_test_set.json` — 31 unique real user queries sebagai test set resmi
- `injection_test_results.json` — Hasil benchmark injection test
- `CHANGELOG.md` (file ini)

### Hasil Injection Test (10 Skenario)
- Layer 2 (threshold) memblokir: 2/10 (role switch jelas dan developer mode)
- Layer 3 (system prompt) menangkap: 8/10 — 0 kebocoran aktual
- Pola Layer 3: ignore injection & jawab bagian legit (A1, A3, C2, E1) atau tolak eksplisit (A2, D1, D2)

### Open Issues
- QRIS keyword mismatch: `"bagaimana cara mengatur qris?"` → doc terdekat "Manajemen Meja" (salah) — perlu audit dokumen QRIS
- GoFood phrasing: `"apakah sora seventh terhubung dengan gofood?"` dist=0.6277 masih diblokir — kata "terhubung" tidak ada di docs
- Margin OOD kini tipis (delta=0.0141) — monitoring ketat diperlukan

---

### Diubah
- `MAX_DISTANCE_THRESHOLD = 0.58` (tetap, tapi sekarang divalidasi dengan dirty benchmark)
- Benchmark in-domain diperluas dengan gaya query "dirty" (typo, santai) yang lebih representatif
  → Ditemukan gap signifikan: clean benchmark memberi max_in=0.4685, dirty benchmark kemungkinan lebih tinggi
- README diperbarui dengan evaluasi pipeline dari 191 percakapan nyata
- **Temuan kritis:** 65% KNOWLEDGE_GAP rate dari 191 percakapan nyata perlu divalidasi post-ingest 34 docs

### Ditambahkan
- `extract_gap_queries.py` — Ekstrak KNOWLEDGE_GAP queries dari log sebagai test set representatif
- `test_injection.py` — Uji prompt injection yang dibungkus dalam pertanyaan legit

### Catatan
- Chunk size dikembalikan ke **800** (dari 500) secara sadar — chunk 500 terlalu kecil, context hilang
- Threshold 0.58 dipilih lebih toleran dari formula eksak (0.5413) karena distribusi query asli user lebih "dirty"
- QRIS masih jadi knowledge gap konsisten (dist ~0.61) — perlu investigasi chunking & kosakata dokumen QRIS

---

## [2026-08-25] — Penambahan 11 Docs + Security Update

### Diubah
- `ingest.py`: Path resolution dinamis (`BASE_DIR` + fallback `./docs` → `../docs`)
- `ingest.py`: Ganti `create_collection` → `get_or_create_collection`
- `app.py`: Tambah `WA_SUPPORT_URL` & `REFUSAL_MESSAGE` dengan WhatsApp CTA
- `app.py`: Tambah guardrail kerahasiaan di `SYSTEM_PROMPT` (rule 3)
- `app.py`: Set `sources = []` di semua response path (source masking)
- Refusal message standar diperbarui di 3 lokasi → centralized ke konstanta `REFUSAL_MESSAGE`

### Ditambahkan
- 11 file dokumentasi baru (`sora-*.md`) → total 36 docs / 109 chunks
- `docs/` dipindahkan ke dalam folder `chatbot/` (self-contained)

### Security
- Nama file internal tidak lagi diekspos via network response
- SYSTEM_PROMPT melarang keras LLM menyebut nama file, path, atau extension `.md/.yaml`

---

## [2026-08-24] — Integrasi Widget React

### Ditambahkan
- `AiChatWidget.tsx` — React widget native (bukan vanilla JS) karena landing page menggunakan React Router v7
- Asset: `public/ask-me-robot.png` — 3D robot avatar untuk floating button
- WhatsApp CTA button di widget (link ke support CS)
- Quick suggestion chips, typing indicator, thumbs feedback

### Catatan
- React widget dipilih (bukan vanilla JS) karena kerangka landing page sudah React 19 + Vite + Tailwind v4
  → Bukan scope creep, ini keputusan konsistensi arsitektur

---

## [2026-08-19] — Kalibrasi Threshold v1

### Diubah
- `MAX_DISTANCE_THRESHOLD = 0.48` → `0.58`
  → Threshold 0.48 terlalu ketat, banyak pertanyaan in-domain ditolak
  → Dinaikan berdasarkan benchmark awal (clean queries, 25 docs)
- `CHUNK_SIZE = 500` → `800`
  → Chunk 500 terlalu kecil, context penting terpotong antar chunk

### Ditambahkan
- `test_threshold.py` — Benchmark tool in-domain vs out-of-domain
- `analytics.py` — Laporan analitik log percakapan (status, provider, feedback, knowledge gap)
- `ollama_provider.py` — Adapter untuk Ollama local model fallback
- Multi-provider LLM failover: OpenRouter → Gemini → Groq → Ollama
- Log percakapan terstruktur ke `logs/chat_conversations.jsonl`

---

## [2026-08-17] — Versi Awal

### Ditambahkan
- `app.py` — FastAPI server dengan RAG pipeline
- `ingest.py` — Document ingestion & embedding builder
- 25 file dokumentasi pertama di `docs/`
- ChromaDB persistent vector database
- Embedding model: `paraphrase-multilingual-MiniLM-L12-v2`
- `CHUNK_SIZE = 800, CHUNK_OVERLAP = 150`
- `MAX_DISTANCE_THRESHOLD = 0.92` (terlalu longgar — semua pertanyaan lolos)
