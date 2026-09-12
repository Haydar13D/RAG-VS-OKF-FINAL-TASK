---
id: DOC-03-SPLIT-BILL
title: Split Bill (Pembagian Tagihan)
category: kasir
target_role: kasir
tags:
- split bill
- pisah nota
- bayar terpisah
- kasir
- transaksi
prerequisites:
- DOC-02-TRANSAKSI
related:
- DOC-01-PROMO
- DOC-06-NOTA
---

## Deskripsi
Fitur Split Bill memungkinkan kasir memisahkan satu pesanan rombongan menjadi beberapa nota tagihan independen, baik dibagikan berdasarkan item yang dipilih maupun dibagi rata berdasarkan nominal rupiah.

## Langkah Operasional
1. Pada layar checkout transaksi kasir, klik tombol **Split Bill** di bagian bawah daftar pesanan.
2. Pilih metode pembagian:
   - **Berdasarkan Item**: Geser/pindahkan item pesanan ke kolom **Tagihan 1**, **Tagihan 2**, dst.
   - **Berdasarkan Nominal**: Tentukan jumlah pembagi (misal dibagi 3 orang sama rata).
3. Selesaikan pembayaran untuk **Tagihan 1** terlebih dahulu dengan metode pembayaran yang dipilih (Cash/QRIS/EDC).
4. Lanjutkan pembayaran untuk **Tagihan 2** dan seterusnya hingga semua kelompok tagihan Lunas.
5. Klik **Cetak Semua Struk Terpisah**.

## FAQ & Troubleshooting
**Q: Bisakah pembayaran Split Bill menggunakan metode pembayaran yang berbeda-beda untuk tiap orang?**
A: Sangat bisa. Orang pertama bisa membayar dengan Cash, orang kedua dengan QRIS, dan orang ketiga dengan Kartu Debit.

**Q: Bagaimana jika salah satu anggota rombongan ingin membatalkan itemnya saat Split Bill berlangsung?**
A: Batalkan modal Split Bill terlebih dahulu, lakukan edit pesanan di layar utama kasir (butuh PIN Supervisor jika item sudah tersimpan di dapur), lalu masuk kembali ke menu Split Bill.
