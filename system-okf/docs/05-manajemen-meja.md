---
id: DOC-05-MEJA
title: Manajemen Meja & Layout Restoran
category: sistem
target_role: supervisor
tags:
- meja
- layout
- dine in
- qr order
- nomor meja
prerequisites:
- DOC-16-PENDAFTARAN
related:
- DOC-02-TRANSAKSI
- DOC-29-SORA-KASIR
---

## Deskripsi
Fitur Manajemen Meja berfungsi untuk mendaftarkan denah dan nomor meja restoran/kafe, memantau status terisi/kosong secara real-time, serta mencetak kode QR Meja untuk pemesanan mandiri oleh pelanggan.

## Langkah Operasional
1. Buka menu **Pengaturan** > pilih tab **Manajemen Meja** (atau dari menu Tagihan > Tambah Meja).
2. **Tambah Meja Massal**: Klik **Buat Banyak Meja**, masukkan jumlah meja (contoh: 10), sistem otomatis membuat Meja 1 hingga Meja 10 secara berurutan.
3. **Tambah Meja Custom**: Klik **Tambah Satu Meja**, isi Nomor/Nama Meja (contoh: "Meja VIP A" atau "Outdoor 05").
4. **Cetak QR Meja**: Klik tombol **Download/Cetak QR Code** pada meja yang diinginkan untuk ditempel di meja restoran.

## FAQ & Troubleshooting
**Q: Bagaimana jika pelanggan berpindah dari Meja 3 ke Meja 8 saat makanan belum disajikan?**
A: Pada layar daftar pesanan kasir, klik nota meja bersangkutan > pilih **Pindah Meja** > pilih **Meja 8** > klik **Konfirmasi Pindah**. Sistem akan memperbarui posisi meja secara otomatis.

**Q: Mengapa meja masih berstatus "Terisi" padahal pelanggan sudah pulang?**
A: Pastikan transaksi meja tersebut sudah diproses checkout hingga statusnya **Lunas**. Jika belum dibayar, kasir wajib menyelesaikan pembayaran atau membatalkan pesanan.
