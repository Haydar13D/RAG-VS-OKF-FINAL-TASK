---
type: fitur
title: Regulasi Service Charge & Pajak PPN
category: pengaturan
tags: [regulasi, service charge, ppn, pajak, biaya layanan, merchant]
---

## Deskripsi
Fitur Regulasi Service Charge & Pajak digunakan untuk mengatur persentase biaya tambahan operasional (seperti service charge resto 5%) dan Pajak PPN (misal 10/11%) yang otomatis dihitung pada setiap transaksi checkout.

## Langkah Operasional
1. Buka menu **Pengaturan** > pilih tab **Regulasi & Pajak**.
2. **Tambah Regulasi Baru**: Klik tombol **Buat Regulasi**.
3. Isi kolom:
   - **Nama Regulasi**: (misal: "Service Charge Resto" atau "PPN 10%").
   - **Tipe Biaya**: Persentase (%) atau Nominal Fix (Rp).
   - **Nilai**: Input angka (misal: 5 untuk 5%).
   - **Penanggung Biaya**: Pilih **Dibebankan ke Pembeli** (menambah total tagihan) atau **Ditanggung Penjual** (dipotong dari profit margin).
4. Klik **Aktifkan Regulasi** > **Simpan**.

## FAQ & Troubleshooting
**Q: Apakah service charge bisa dinegasikan/dihilangkan untuk pesanan khusus (seperti pesanan Karyawan / VIP)?**
A: Bisa. Kasir yang memiliki otorisasi Supervisor dapat menghapus checklist Regulasi pada panel pesanan sebelum memproses checkout.

**Q: Bagaimana jika toko memiliki dua regulasi sekaligus (Service Charge 5% dan PPN 10%)?**
A: Sistem mendukung skema *Multi-Regulation*. Keduanya dapat diaktifkan bersamaan, dan sistem akan mengkalkulasikan secara berurutan sesuai urutan regulasi yang di-setting.