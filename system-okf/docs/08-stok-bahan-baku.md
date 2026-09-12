---
id: DOC-08-STOK-OPNAME
title: Manajemen Stok Opname & Restock Bahan
category: inventaris
target_role: supervisor
tags:
- stok opname
- restock
- bahan baku
- selisih stok
- inventaris
- import excel
prerequisites:
- DOC-10-BAHAN-BAKU
related:
- DOC-27-SORA-STOK
- DOC-12-VARIAN
---

## Deskripsi
Fitur Stok Opname & Restock digunakan untuk menambah pasokan bahan baku masuk, mengoreksi selisih stok fisik versus sistem, serta melacak riwayat perubahan stok akibat penggunaan resep atau barang rusak/kadaluarsa.

## Langkah Operasional
1. **Restock Bahan Baku (Penambahan Stok)**:
   - Buka menu **Inventaris** > **Bahan Baku** > pilih tab **Riwayat Stok**.
   - Klik **+ Tambah Stok**, pilih nama bahan baku, masukkan jumlah penambahan, harga beli total, dan tanggal restock.
   - Atau gunakan fitur **Import File Excel** untuk menambah banyak bahan baku sekaligus.
2. **Melakukan Stok Opname (Penyesuaian Selisih)**:
   - Buka menu **Inventaris** > **Stok Opname**.
   - Klik **Sesi Opname Baru**, pilih kategori bahan baku.
   - Input **Jumlah Stok Fisik** riil di gudang/dapur.
   - Sistem akan menghitung **Selisih Stok** (+ / -). Masukkan **Keterangan Selisih** (misal: "Barang Tumpah / Kadaluarsa") lalu klik **Simpan & Sesuaikan**.

## FAQ & Troubleshooting
**Q: Apa bedanya fitur Tambah Stok dengan Stok Opname?**
A: **Tambah Stok** digunakan saat Anda membeli pasokan baru dari supplier. **Stok Opname** digunakan untuk mencocokkan stok aktual di gudang dengan catatan sistem jika terjadi perbedaan (hilang/rusak/selisih hitung).

**Q: Bagaimana jika harga beli bahan baku dari supplier mengalami kenaikan saat restock?**
A: Saat menginput Tambah Stok baru, sistem akan menyesuaikan rata-rata HPP (*Moving Average Cost*) atau menggunakan harga beli terbaru sesuai konfigurasi akuntansi toko.
