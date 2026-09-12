---
id: DOC-24-LANGGANAN
title: Sistem Langganan (Subscription) — Perpanjangan Masa Aktif
category: langganan
target_role: owner
tags:
- langganan
- subscription
- perpanjangan
- masa aktif
- paket langganan
- expired
- grace period
- sora coin
- max user
- owner
prerequisites:
- DOC-16-PENDAFTARAN
related:
- DOC-23-SORA-COIN
- DOC-17-LAPORAN
---

## Deskripsi
Sistem Langganan mengatur masa aktif toko di aplikasi Sora Seventh. Agar semua fitur bisa digunakan, toko harus memiliki masa langganan yang aktif. Langganan dibayar menggunakan **Sora Coin** dengan memilih paket yang tersedia. Sistem akan otomatis menambah hari aktif ke tanggal kadaluarsa toko sesuai paket yang dipilih.

## Konsep Utama

### Masa Aktif (Expired Date)
Setiap toko memiliki `tanggal kadaluarsa langganan`. Jika tanggal ini sudah lewat dan toko tidak memperbarui langganan, akses ke fitur aplikasi akan terbatas.

### Paket Langganan
Tersedia beberapa paket langganan dengan detail berbeda:

| Yang Berbeda Antar Paket | Keterangan |
|---|---|
| **Nama Paket** | Misal: "Paket Standard", "Paket Premium" |
| **Jumlah Koin** | Berapa koin yang dibutuhkan untuk paket ini |
| **Jumlah Hari** | Berapa hari ditambahkan ke masa aktif |
| **Maks. Pengguna** | Maksimum jumlah akun karyawan di toko |
| **Label Best Seller** | Paket yang paling banyak dipilih diberi label khusus |

### Saldo Koin Harus Cukup
Sebelum bisa membayar langganan, pastikan **saldo Sora Coin toko mencukupi** sesuai kebutuhan paket. Jika kurang, lakukan [topup koin](23-sora-coin-topup.md) terlebih dahulu.

## Langkah Operasional

### Memperpanjang Masa Langganan
1. Buka menu **Langganan** atau **Pengaturan** > **Paket Saya**.
2. Pilih **paket langganan** yang diinginkan dari daftar yang tersedia.
3. Sistem menampilkan detail paket: jumlah koin, jumlah hari yang ditambah, dan tanggal expired baru.
4. Pastikan saldo koin mencukupi (ditampilkan di halaman ini).
5. Tap **Konfirmasi Perpanjangan**.
6. Sistem langsung memotong koin dari saldo toko dan menambah hari ke masa aktif.
7. Email konfirmasi dikirim otomatis ke email Owner dengan detail nomor order dan tanggal expired baru.

> ⚠️ **Hanya Owner** yang bisa melakukan pembayaran langganan. Kasir tidak memiliki akses ini.

### Melihat Status Langganan Saat Ini
- Buka **Pengaturan** > **Paket Saya** — tampil tanggal expired, paket aktif, dan saldo koin.
- Notifikasi pengingat juga dikirim beberapa hari sebelum masa aktif habis (jumlah hari bisa dikonfigurasi).

## Format Nomor Order
- Order langganan: `SUB-{timestamp}` (contoh: `SUB-1722160000000`)

## Aturan Perpanjangan

### Grace Period
**Grace period** adalah jendela waktu menjelang habisnya langganan di mana perpanjangan akan langsung **menambah hari** ke tanggal expired. Jika perpanjangan dilakukan **di luar grace period** (terlalu jauh sebelum expired atau setelah expired), koin tetap dikurangi namun tanggal expired **tidak otomatis bertambah** (dihitung sebagai "Support" ke pengembang).

### Validasi Koin
Jumlah koin yang dibayarkan harus **tepat sama** dengan koin yang dibutuhkan paket. Tidak bisa membayar kurang atau lebih dari harga paket.

## Notifikasi Email Otomatis

| Kapan | Isi Email |
|---|---|
| Setelah perpanjangan berhasil | Nomor order + tanggal expired baru + jumlah koin yang digunakan |
| Setelah topup koin berhasil | Jumlah koin yang masuk + total yang dibayar |
| Pengingat masa aktif hampir habis | Informasi sisa hari + ajakan perpanjangan |

## Jumlah Karyawan per Toko (Max Users)
Setiap paket langganan memiliki batas maksimum akun karyawan yang bisa dibuat dalam satu toko. Jika sudah mencapai batas, tambah akun karyawan baru tidak bisa dilakukan sampai upgrade ke paket dengan kapasitas lebih tinggi.

- Default bawaan sistem: **5 akun karyawan** per toko
- Paket tertentu bisa mengizinkan lebih banyak

## FAQ & Troubleshooting

**Q: Apa yang terjadi kalau langganan saya habis?**
A: Jika masa aktif sudah lewat, akses ke fitur-fitur aplikasi akan terbatas atau terkunci. Segera lakukan topup koin (jika saldo habis) kemudian perpanjang langganan untuk memulihkan akses penuh.

**Q: Berapa hari yang saya dapat dari membeli satu paket?**
A: Jumlah hari berbeda tergantung paket yang dipilih. Detail hari selalu ditampilkan sebelum konfirmasi pembayaran. Pilih paket yang sesuai kebutuhan durasi Anda.

**Q: Apakah saya bisa perpanjang langganan jauh-jauh hari sebelum habis?**
A: Bisa, tapi perhatikan **grace period**. Perpanjangan yang dilakukan di luar jendela grace period (terlalu awal) akan mengurangi koin Anda, namun tanggal expired tidak langsung bertambah. Disarankan perpanjang dalam rentang notifikasi pengingat yang muncul di aplikasi.

**Q: Saya topup koin tapi belum sempat bayar langganan. Apakah koin saya hangus?**
A: Tidak. Koin tersimpan di saldo toko tanpa batas waktu dan hanya berkurang jika Anda secara aktif membayar langganan atau melakukan donasi.

**Q: Kenapa toko saya tidak bisa menambah karyawan baru padahal kuota masih ada?**
A: Cek kembali batas maksimum user di paket langganan aktif Anda. Jika jumlah akun karyawan sudah mencapai `max_users` paket, Anda perlu upgrade ke paket dengan kapasitas lebih tinggi.

**Q: Apakah saya bisa membayar langganan dan donasi sekaligus?**
A: Ya! Sistem mendukung satu transaksi yang sekaligus membayar langganan dan donasi. Pilih paket langganan, lalu pilih juga program donasi dan jumlah koin untuk donasi. Koin akan dipotong sekaligus dan satu email konfirmasi dikirim.

**Q: Berapa lama proses perpanjangan setelah konfirmasi?**
A: Perpanjangan langganan (berbeda dengan topup koin) langsung diproses secara **real-time** — tidak perlu menunggu karena menggunakan koin yang sudah ada di saldo, bukan pembayaran eksternal. Tanggal expired toko langsung berubah setelah konfirmasi.

**Q: Apakah ada bonus langganan untuk toko yang baru pertama kali daftar?**
A: Sistem memiliki program "1st User Bonus" untuk toko yang baru mendaftar, namun ketersediaan bonus ini bergantung pada kebijakan promosi Sora yang berlaku saat pendaftaran. Hubungi tim Sora untuk informasi lebih lanjut.

```
Harga per koin = Nominal (Rp) ÷ Jumlah koin
Contoh: Rp 25.000 ÷ 1 koin = Rp 25.000/koin
```

Harga terkini selalu ditampilkan sebelum konfirmasi topup.
