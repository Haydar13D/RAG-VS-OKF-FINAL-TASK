---
id: DOC-23-SORA-COIN
title: Sora Coin — Topup & Saldo Koin Toko
category: langganan
target_role: owner
tags:
- sora coin
- koin
- topup koin
- beli koin
- saldo koin
- midtrans
- pembayaran koin
- virtual money
- owner
---

## Deskripsi
Sora Coin adalah mata uang digital internal platform Sora Seventh yang digunakan oleh **toko** (bukan pelanggan akhir) untuk membayar biaya langganan aplikasi dan menyalurkan donasi ke program sosial pilihan. Koin dibeli menggunakan uang nyata via payment gateway Midtrans dan disimpan sebagai saldo toko.

## Perbedaan Sora Coin vs Poin Pelanggan

| | Sora Coin | Poin/Loyalty Pelanggan |
|---|---|---|
| **Siapa yang pakai** | Pemilik/Owner toko | Pelanggan pembeli |
| **Untuk apa** | Bayar langganan aplikasi, donasi | Ditukar diskon saat belanja |
| **Cara dapat** | Beli dengan uang nyata | Otomatis dari transaksi |
| **Masa kadaluarsa** | Tidak ada | Bisa diatur (setting poin) |

## Cara Topup Koin

1. Buka menu **Pengaturan** > **Sora Coin** (atau langsung dari notifikasi langganan hampir habis).
2. Masukkan **jumlah koin** yang ingin dibeli.
3. Sistem menampilkan **total harga** (jumlah koin × harga per koin).
4. Tap **Topup Koin** — sistem membuat tagihan via **Midtrans**.
5. Sistem mengirim **email** berisi link pembayaran ke email Owner.
6. Lakukan pembayaran di halaman Midtrans (semua metode tersedia: transfer bank, QRIS, e-wallet, kartu kredit, dll.).
7. Setelah pembayaran dikonfirmasi, **koin otomatis masuk** ke saldo toko dalam 1–2 menit.
8. Email konfirmasi sukses dikirim ke Owner.

> ⚠️ **Hanya Owner** yang bisa melakukan topup koin. Kasir dan karyawan tidak memiliki akses ini.

## Format Nomor Order
- Topup koin: `TOP-{timestamp}` (contoh: `TOP-1722160000000`)

## Harga Koin
Harga per koin bersifat dinamis dan dikonfigurasi oleh tim Sora (bukan oleh pemilik toko). Formula:

```
Harga per koin = Nominal (Rp) ÷ Jumlah koin
Contoh: Rp 25.000 ÷ 1 koin = Rp 25.000/koin
```

Harga terkini selalu ditampilkan sebelum konfirmasi topup.

## Status Transaksi Topup

| Status | Keterangan |
|---|---|
| **Pending** | Tagihan dibuat, menunggu pembayaran |
| **Paid** | Pembayaran berhasil, koin sudah masuk |
| **Failed** | Pembayaran gagal/ditolak/kadaluarsa |
| **Refunded** | Dana dikembalikan (proses manual oleh Sora) |

## Riwayat Transaksi Koin
Semua transaksi koin (topup masuk dan pemakaian keluar) tercatat di **Riwayat Koin** dengan tipe:

| Tipe | Arah | Keterangan |
|---|---|---|
| Topup | ➕ Masuk | Pembelian koin baru |
| Langganan | ➖ Keluar | Pembayaran perpanjangan masa aktif |
| Donasi | ➖ Keluar | Donasi ke program sosial |
| Langganan + Donasi | ➖ Keluar | Keduanya dalam satu transaksi |
| Support | ➖ Keluar | Pembayaran di luar masa grace period |

## FAQ & Troubleshooting

**Q: Apa itu Sora Coin? Apa bedanya dengan poin yang diberikan ke pelanggan?**
A: Sora Coin adalah mata uang antara toko dan platform Sora — digunakan untuk membayar langganan aplikasi. Poin loyalty pelanggan adalah reward yang diberikan toko ke pembeli mereka. Keduanya adalah sistem yang benar-benar terpisah dan tidak saling mempengaruhi.

**Q: Kenapa karyawan/kasir saya tidak bisa topup koin?**
A: Topup koin, bayar langganan, dan donasi hanya bisa dilakukan oleh **Owner**. Ini adalah keamanan bawaan sistem — fitur finansial platform tidak boleh diakses oleh kasir biasa.

**Q: Saya sudah bayar di Midtrans tapi koin belum masuk ke saldo. Kenapa?**
A: Koin masuk secara otomatis setelah Midtrans mengirim notifikasi konfirmasi pembayaran ke sistem Sora. Biasanya membutuhkan **1–2 menit** setelah pembayaran selesai. Jika lebih dari 5 menit belum masuk, cek status transaksi di Riwayat Koin. Jika masih Pending, hubungi tim support Sora.

**Q: Apakah koin yang sudah dibeli bisa dikembalikan (refund)?**
A: Koin yang belum digunakan bisa diajukan refund secara manual ke tim Sora. Koin yang **sudah digunakan** untuk langganan atau donasi tidak bisa di-refund.

**Q: Apakah koin punya masa kadaluarsa?**
A: **Tidak.** Saldo koin toko tidak memiliki masa kadaluarsa. Koin akan tetap tersimpan sampai digunakan, berbeda dengan masa aktif langganan yang ada tanggal kadaluarsanya.

**Q: Berapa minimal koin yang bisa dibeli saat topup?**
A: Minimal pembelian adalah **1 koin**. Tidak ada maksimum, namun pastikan jumlah yang dibeli cukup untuk membayar paket langganan yang dipilih.

**Q: Link pembayaran Midtrans sudah kadaluarsa sebelum sempat dibayar. Bagaimana?**
A: Buat permintaan topup baru. Setiap permintaan topup menghasilkan link pembayaran baru dengan masa berlaku tertentu dari Midtrans. Transaksi lama yang kadaluarsa akan otomatis berstatus `Failed` dan tidak mengurangi saldo koin.
