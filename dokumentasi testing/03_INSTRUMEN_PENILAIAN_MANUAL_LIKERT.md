# INSTRUMEN PENILAIAN MANUAL SKALA LIKERT (1-5) & TRIANGULASI METODE

Document Version: 1.0  
Tanggal: 12 September 2026  

---

## 📐 1. Konsep Triangulasi Metodologi (Bab III Skripsi)

Untuk menghasilkan bukti ilmiah yang kokoh dan tidak terbantahkan dalam sidang skripsi, penilaian akurasi sistem tidak boleh hanya bergantung pada metrik otomatis (*Keyword Matching*). 

Metodologi pengujian ini menerapkan **Triangulasi Metodologi (Method Triangulation)** dengan menggabungkan:
1. **Metrik Kuantitatif Otomatis:** *Automated Keyword Coverage Rate (%)*.
2. **Metrik Kuantitatif Manusia:** *Human Subjective Evaluation (Likert Scale 1-5)* oleh Peneliti / Expert Evaluator.

---

## 📊 2. Rubrik Penilaian Manual Skala Likert (1 - 5)

Setiap jawaban yang dihasilkan oleh **System RAG** dan **System OKF** atas 40 pertanyaan pengujian akan dinilai secara independen oleh evaluator manusia berdasarkan rubrik standar berikut:

| Skala Likert | Kategori | Kriteria Penilaian Rinci |
| :---: | :--- | :--- |
| **1** | **Sangat Buruk / Hallucination** | Jawaban salah total, mengarang fakta (halusinasi), memberikan instruksi berbahaya/salah yang merusak data kasir, atau gagal total. |
| **2** | **Kurang Akurat** | Jawaban relevan dengan topik, tetapi banyak langkah utama yang hilang, ada informasi menyesatkan, atau instruksi tidak bisa dipraktikkan. |
| **3** | **Cukup Akurat** | Jawaban menjawab inti masalah, namun kurang detail, bahasa membingungkan, atau terdapat minor kesalahan istilah tombol POS. |
| **4** | **Akurat & Baik** | Jawaban benar, akurat sesuai dokumen SOP, langkah urut dan logis, serta mudah diikuti oleh kasir. |
| **5** | **Sangat Akurat & Sempurna** | Jawaban 100% tepat, sangat lengkap, langkah terstruktur rapi (step-by-step), bold kata kunci tepat, ramah, dan bebas cacat. |

---

## 📑 3. Format Tabel Data Penilaian Manual (Contoh Instrumen)

Tabel berikut akan diexport ke format CSV/Excel (`eval/manual_evaluation_sheet.csv`) untuk diisi oleh penguji/peneliti:

| ID Query | Kategori Soal | Pertanyaan Pengguna | Jawaban AI (RAG / OKF) | Keyword Match (%) | Skor Likert (1-5) | Catatan Evaluator |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ACC-01` | Kasir (Exact) | Cara void transaksi... | *[Teks Jawaban AI]* | 100% | **5** | Langkah presisi sesuai SOP |
| `ACC-12` | Informal (Dirty) | *gimana balikin duit kasir...* | *[Teks Jawaban AI]* | 75% | **4** | Memahami kata kiasan kasir |
| `ACC-35` | Out-of-Domain | *Cara buat nasi goreng...* | *[Teks Penolakan Guardrail]* | N/A | **5** | Penolakan tepat & sopan |

---

## 📈 4. Metode Perhitungan Akhir untuk Bab IV (Hasil & Pembahasan)

### A. Formula Mean Likert Score (MLS):
$$\text{MLS} = \frac{\sum_{i=1}^{N} \text{Skor Likert}_i}{N}$$

### B. Uji Signifikansi Statistik (Paired t-Test / Wilcoxon Signed-Rank Test):
Untuk membuktikan secara akademis apakah perbedaan akurasi antara System RAG vs System OKF **signifikan secara statistik** ($p < 0.05$), hasil skor Likert dari kedua sistem akan diuji menggunakan **Wilcoxon Signed-Rank Test** (karena data skala Likert bersifat ordinal/non-parametrik).
