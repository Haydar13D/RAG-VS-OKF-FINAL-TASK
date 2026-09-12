---
id: DOC-21-DONASI-KASIR
title: Donasi Uang Kembalian & Pembulatan Nominal
category: donasi
target_role: kasir
tags:
- donasi
- pembulatan
- kembalian
- uang tunai
- kasir
- amal
prerequisites:
- DOC-02-TRANSAKSI
related:
- DOC-25-DONASI-KOIN
- DOC-30-SORA-KOIN-DONASI
---

## Deskripsi
Fitur Donasi Uang Kembalian & Pembulatan Nominal digunakan untuk membulatkan total tagihan belanja pecahan kecil serta memungkinkan pelanggan mengalokasikan sisa uang kembalian tunai sebagai donasi/amal.

## Langkah Operasional
1. **Pengaturan Pembulatan Tagihan**:
   - Buka menu **Pengaturan** > **Atur Pembulatan (Rounding Rule)**.
   - Set batas pembulatan (misal: Bulatkan Ke Atas / Ke Bawah per kelipatan Rp 100 atau Rp 500).
2. **Memproses Donasi Kembalian Saat Transaksi**:
   - Pada layar checkout kasir saat transaksi tunai, jika ada uang kembalian pecahan kecil (misal: Rp 400), klik tombol **Donasikan Kembalian**.
   - Konfirmasi persetujuan pelanggan.
   - Sistem akan mengalokasikan Rp 400 tersebut ke akun Donasi dan mencetak keterangan donasi pada struk belanja.

## FAQ & Troubleshooting
**Q: Ke mana alokasi dana donasi kembalian tersebut dicatat dalam laporan keuangan?**
A: Dana donasi dicatat secara terpisah dari omset penjualan bersih toko. Anda dapat mengunduh laporan rekapitulasi dana donasi melalui menu **Laporan Finansial** > tab **Laporan Donasi**.

**Q: Apakah donasi kembalian wajib diisi oleh kasir?**
A: Tidak. Donasi bersifat opsional dan hanya diinput oleh kasir setelah mendapatkan persetujuan lisan dari pelanggan.
