---
type: fitur
title: Transaksi Pembayaran & Checkout Kasir
category: kasir
tags: [kasir, transaksi, checkout, cash, qris, debit, edc, offline mode]
---

## Deskripsi
Fitur Transaksi Kasir digunakan untuk mencatat pesanan pelanggan, memilih metode pembayaran (Tunai, QRIS, Kartu Debit/Kredit, Transfer Bank), memproses kembalian, serta mencetak struk belanja secara instan baik dalam mode online maupun offline.

## Langkah Operasional
1. **Memilih Menu**: Pada layar Kasir, pilih kategori menu lalu klik item makanan/minuman yang dipesan pelanggan (pilih varian/topping jika ada).
2. **Pilih Tipe Pesanan & Meja**: Tentukan tipe pesanan (*Dine In*, *Take Away*, atau *Online Food*). Jika *Dine In*, pilih nomor meja pelanggan.
3. **Proses Checkout**: Klik tombol **Bayar** di pojok kanan bawah. Pilih metode pembayaran:
   - *Tunai (Cash)*: Input jumlah uang yang diterima, sistem otomatis menghitung kembalian.
   - *QRIS*: Tampilkan kode QRIS dinamis/statis ke pelanggan, tunggu verifikasi pembayaran.
   - *EDC Debit/Kredit*: Gesek/Tap kartu di mesin EDC dan masukkan nomor referensi/Approval Code.
4. **Cetak Struk**: Klik **Selesaikan Transaksi & Cetak Nota**. Struk otomatis dicetak ke printer thermal.

## FAQ & Troubleshooting
**Q: Apa yang harus dilakukan jika internet mati saat transaksi sedang berlangsung?**
A: Sistem otomatis beralih ke **Mode Offline**. Anda tetap bisa melayani transaksi **Tunai (Cash)**. Data transaksi tersimpan aman di memori lokal dan akan otomatis sinkron (*auto-sync*) ke cloud server begitu koneksi internet terhubung kembali.

**Q: Bagaimana jika pembayaran QRIS pelanggan sudah sukses di HP pelanggan tetapi belum terverifikasi di layar kasir?**
A: Klik tombol **Cek Status Pembayaran QRIS** pada modal checkout. Jika masih belum terupdate, cek bukti transfer pada aplikasi merchant/e-wallet lalu konfirmasi manual oleh Supervisor.