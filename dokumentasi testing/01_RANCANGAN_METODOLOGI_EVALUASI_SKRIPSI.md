# RANCANGAN METODOLOGI EVALUASI SKRIPSI (HEAD-TO-HEAD: RAG vs OKF)

Document Version: 1.0  
Tanggal: 12 September 2026  
Status: Draft Final Rencana Pengujian Akademis  

---

## 📌 1. Latar Belakang & Pembahasan 5 Lubang Metodologi

Evaluasi komparatif antara **System RAG (Retrieval-Augmented Generation)** dan **System OKF (Open Knowledge Format)** memerlukan standar metodologi yang komprehensif, valid, dan dapat dipertanggungjawabkan secara ilmiah saat ujian skripsi.

Berdasarkan tinjauan kritis terhadap pengujian awal, ditemukan **5 Lubang Metodologi** yang harus ditutup:

| Lubang Metodologi | Masalah pada Pengujian Lama | Solusi & Penyempurnaan Baru |
| :--- | :--- | :--- |
| **Lubang #1: Metrik Akurasi Cuma Keyword** | Keyword matching saja bersifat superficial (proxy lemah). AI bisa menyebut keyword tanpa memberi solusi. | **Triangulasi Metrik:** Keyword Coverage (Otomatis) + **Human Manual Evaluation Skala Likert 1-5** (Akurasi & Kelengkapan). |
| **Lubang #2: Ukuran Sampel Soal Kecil (N=10)** | 10 pertanyaan tidak representatif untuk mengklaim performa sistem secara keseluruhan. | **Dataset Diperluas (N=40 Soal):** Terbagi dalam 5 kategori teoretis (*Exact-Match, Paraphrase/Informal, Out-of-Domain, Multi-Dokumen, Ambigu*). |
| **Lubang #3: Keamanan Cuma Biner (Lolos/Tidak)** | LLM bersifat probabilistik. Menguji 1x tidak cukup membuktikan ketahanan prompt injection. | **Multi-Run Leak Rate Test:** Skenario kritis diuji 20-30x per sistem untuk menghitung **Persentase Kebocoran (Leak Rate %)**. |
| **Lubang #4: Tanpa Baseline & Profiling Performa** | Tidak ada data trade-off antara akurasi, kecepatan, dan konsumsi daya komputer. | **System Profiling:** Pengukuran **Latency (detik)** + **Resource Usage (RAM MB & CPU %)** selama beban kerja. |
| **Lubang #5: Variabel Kontrol Tidak Identik** | Risiko perbedaan provider/model/normalizer yang membuat perbandingan tidak adil. | **Strict Control Variables:** Model LLM (`gemini-1.5-flash`), temperature (`0.1`), query normalizer, dan isi dokumen dijamin **SAMA PERSIS 100%**. |

---

## 🎯 2. Kerangka Metodologi & Matriks Evaluasi Akademis

### A. Triangulasi Metrik Akurasi (Lubang #1)
1. **Automated Keyword Coverage Rate ($K_c$):**
   $$K_c = \frac{\text{Jumlah Keyword Terdeteksi}}{\text{Total Expected Keywords}} \times 100\%$$
2. **Human Manual Scoring (Skala Likert 1-5):**
   - **Skor 1 (Gagal Total / Hallucination):** Jawaban salah, ngarang, atau menyesatkan.
   - **Skor 2 (Kurang):** Menjawab sebagian kecil tapi banyak langkah penting hilang.
   - **Skor 3 (Cukup):** Menjawab inti pertanyaan tapi kurang detail atau ada minor typo langkah.
   - **Skor 4 (Baik):** Menjawab benar, akurat, dan langkah operasional jelas.
   - **Skor 5 (Sempurna / Sangat Akurat):** Menjawab 100% akurat, lengkap, terstruktur, dan ramah.

### B. Taksonomi Dataset Pertanyaan N=40 (Lubang #2)
Dataset akan disusun dalam file `eval/test_dataset_extended_N40.json` dengan 5 kategori:
1. **Exact-Match (10 Soal):** Bahasa formal persis dokumentasi resmi.
2. **Paraphrase / Informal / Typo (10 Soal):** Bahasa sehari-hari, santai, kata kiasan kasir Indonesia (misal: *"gimana cara balikin duit kasir salah input"*).
3. **Multi-Dokumen Integration (8 Soal):** Membutuhkan penggabungan konteks dari 2 atau lebih dokumen/bagian.
4. **Ambigu / Underspecified (6 Soal):** Pertanyaan setengah menggantung yang membutuhkan klarifikasi atau jawaban kondisional.
5. **Out-of-Domain / Boundary Test (6 Soal):** Pertanyaan di luar SOP toko yang wajib ditolak oleh Guardrail (`KNOWLEDGE_GAP`).

### C. Pengujian Keamanan & Leak Rate (Lubang #3)
Menguji 5 skenario injection paling kritis sebanyak **20 kali pengulangan (N_run = 20)** per sistem (Total 100 request RAG + 100 request OKF):
$$\text{Leak Rate (\%)} = \frac{\text{Jumlah Response yang Bocor / Melanggar Guardrail}}{\text{Total Pengulangan (20)}} \times 100\%$$

### D. Profiling Performa & Resource Usage (Lubang #4)
Mencatat latensi (detik), penggunaan RAM (MB), dan CPU utilization (%) menggunakan `psutil` saat pengujian sedang berlangsung.

---

## 📁 3. Struktur Direktori Dokumentasi & Output

```
dokumentasi testing/
├── 01_RANCANGAN_METODOLOGI_EVALUASI_SKRIPSI.md  <-- Dokumen Metodologi Utama
├── 02_RENCANA_PERBAIKAN_KODE_DAN_DATASET.md     <-- Rencana Eksekusi File & Code
└── 03_INSTRUMEN_PENILAIAN_MANUAL_LIKERT.md      <-- Panduan Scoring Manusia (1-5)
```
