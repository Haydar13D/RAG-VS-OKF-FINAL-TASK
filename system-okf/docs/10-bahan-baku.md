---
id: DOC-10-BAHAN-BAKU
title: Pendaftaran Bahan Baku & Satuan
category: inventaris
target_role: supervisor
tags:
- bahan baku
- satuan
- harga satuan
- resep
- hpp
- gram
- ml
prerequisites:
- DOC-33-SORA-ONBOARDING
related:
- DOC-08-STOK-OPNAME
- DOC-11-MENU
---

## Deskripsi
Fitur Pendaftaran Bahan Baku digunakan untuk mencatat bahan mentah (*raw materials*) usaha lengkap dengan satuan ukur terkecil (gram, ml, pcs) dan harga satuan sebagai dasar perhitungan HPP resep menu makanan/minuman.

## Langkah Operasional
1. Buka menu **Inventaris** > **Bahan Baku** > pilih kategori bahan baku.
2. Klik **Buat Bahan Baku**.
3. Isi formulir:
   - **Kode Bahan**: Masukkan kode unik (misal: `BB-KOP-01`).
   - **Nama Bahan Baku**: (misal: "Biji Kopi Arabika").
   - **Satuan Dasar**: Pilih unit terkecil (misal: *Gram* atau *Ml*).
   - **Harga Satuan**: Masukkan harga per satuan terkecil (misal: Rp 200 / gram).
   - **Minimum Stok**: Set batas peringatan restock (misal: 1000 gram).
4. Klik **Simpan**.

## FAQ & Troubleshooting
**Q: Mengapa saya harus menginput harga satuan per gram/ml dan bukan per kg/liter?**
A: Menginput harga per unit terkecil sangat penting agar kalkulasi HPP resep menu (misal espresso memakai 18 gram kopi) menjadi 100% presisi dan akurat secara otomatis.

**Q: Bolehkah mengubah satuan dasar bahan baku yang sudah pernah ditransaksikan?**
A: Tidak disarankan mengubah satuan bahan baku yang sudah berjalan karena akan merusak riwayat HPP transaksi terdahulu. Solusinya: Nonaktifkan bahan baku lama dan buat item bahan baku baru dengan satuan yang benar.
