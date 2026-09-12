---
type: fitur
title: Pembatalan Pesanan & Void Nota Transaksi
category: kasir
tags: [void, pembatalan, batalin nota, batalin pesanan, salah input, hapus pesanan, pin supervisor, stok return]
---

## Deskripsi
Fitur Void Nota dan Pembatalan Pesanan digunakan untuk membatalkan nota transaksi yang sudah terbayar atau salah input pesanan, mengembalikan stok bahan baku ke inventaris secara otomatis, serta mencatat alasan pembatalan untuk audit toko.

## Langkah Operasional
1. Buka menu **Daftar Transaksi / Riwayat Pesanan** di navigasi sebelah kiri.
2. Cari dan klik **Nomor Nota** yang ingin dibatalkan.
3. Klik tombol **Atur Transaksi** di kanan atas > pilih **Void Nota / Batalkan Transaksi**.
4. Pilih atau ketik **Alasan Pembatalan** (misal: "Pelanggan Salah Pesan" atau "Kualitas Bahan Rusak").
5. Masukkan **PIN Supervisor / Manager / Owner**.
6. Klik **Konfirmasi Void**. Struk pembatalan (*Void Slip*) akan tercetak jika printer terhubung.

## FAQ & Troubleshooting
**Q: Apakah transaksi yang sudah di-void bisa dikembalikan lagi (*undo*)?**
A: Tidak bisa. Transaksi yang sudah di-void berstatus permanen Batal. Jika pelanggan ingin memesan ulang, buatkan nota baru.

**Q: Apakah stok bahan baku otomatis bertambah kembali setelah dilakukan Void Nota?**
A: Ya, sistem secara otomatis melakukan *auto-return inventory* sehingga jumlah stok bahan baku dikembalikan sesuai porsi menu yang dibatalkan.