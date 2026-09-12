---
id: DOC-27-SORA-STOK
title: Satuan, Input, Bulk Import, dan Manajemen Stok Bahan Baku
category: inventaris
target_role: supervisor
tags:
- bahan baku
- satuan
- stok
- import
- bulk upload
- HPP
prerequisites:
- DOC-10-BAHAN-BAKU
related:
- DOC-08-STOK-OPNAME
---

## Membuat Satuan Bahan Baku
1. Masukkan nama satuan (misal: ml).
2. Isi deskripsi (opsional), lalu tap "Simpan".

**Catatan Penting:** Nama satuan sangat berpengaruh pada perhitungan selanjutnya — pastikan semua jenis satuan sudah dimasukkan di awal agar input data ke depannya lancar.

## Input Bahan Baku (Inti)
1. Ketik kode bahan (bebas kombinasi huruf/angka) dan nama bahan baku (contoh: Saus tomat).
2. Ketik total stok berdasarkan satuan terkecil resep. Contoh: untuk 1 liter, ketik 1.000 (dalam satuan terkecil yaitu mililiter).
3. Ketik harga total (contoh: 1.000 ml saus tomat harganya 25.000). Harga per satuan (misal per ml) akan otomatis terhitung.
4. Tentukan limit minimal stok (contoh: 210 ml) — jika stok mencapai angka ini, akan muncul notifikasi peringatan untuk restock. Pilih satuannya.
5. Masukkan keterangan (opsional). Bahan baku resmi terdaftar.

**Catatan Penting:** Bahan baku menjadi acuan utama seluruh resep di Sora Seventh — perhitungan stok dan sisa saldo aset produk otomatis tersinkronisasi dari data bahan baku ini.

## Input Banyak Bahan Baku Sekaligus (Bulk Import)
1. Tap menu "Upload File", pilih "Download Template", lalu tap "Download".
2. Simpan file "template_import_bahan_baku.xlsx", buka di Excel atau aplikasi sejenis.
3. Isi data (Kode, Nama bahan baku, Satuan, dll) mengikuti contoh di baris paling atas, lalu simpan.
   - **Penting:** pada kolom "Satuan", wajib pilih dari drop-down yang tersedia — jangan diketik manual, agar sistem tidak error saat membaca.
4. Kembali ke aplikasi, tap "Upload File" → pilih "File Data Bahan Baku" → tap "Pilih File" → pilih file yang sudah diedit → tap "Import".
5. Bahan baku otomatis bertambah secara massal.

**Catatan:** Pastikan kode dan nama bahan bersifat unik (tidak sama dengan yang sudah terdaftar di aplikasi).

## Mengelola Stok Bahan Baku

### Menambah Stok (Top Up)
1. Pilih bahan bakunya.
2. Ketik jumlah bahan yang ditambahkan dan total harganya.
3. Masukkan deskripsi (opsional). Klik "Tambah Stok".

### Mengurangi Stok (Deduct)
1. Pilih bahan bakunya, ketik jumlah bahan yang dikurangi.
2. Masukkan deskripsi (opsional). Klik "Kurangi Stok".

**Catatan Penting:** Harga bahan baku otomatis menyesuaikan (auto-adjust) dengan harga stok terbaru, dikalkulasikan dengan sisa modal stok sebelumnya. Ini menjaga perhitungan HPP tetap akurat meskipun harga pasar berfluktuasi.
