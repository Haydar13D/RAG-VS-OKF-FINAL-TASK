---
id: DOC-25-DONASI-KOIN
title: Donasi Koin Sora ke Program Sosial
category: donasi
target_role: owner
tags:
- donasi
- koin sora
- program sosial
- support pengembang
- coin donation
- kontribusi
- owner
---

## Deskripsi
Fitur Donasi Koin memungkinkan Owner toko untuk menyalurkan Sora Coin yang dimiliki ke program-program sosial yang tersedia di platform Sora Seventh. Donasi bersifat sukarela dan tidak memberikan penambahan masa aktif langganan — ini adalah bentuk kontribusi sosial dari toko ke masyarakat melalui platform Sora.

## Perbedaan Donasi vs Perpanjangan Langganan

| | Donasi | Perpanjangan Langganan |
|---|---|---|
| **Koin berkurang** | ✅ Ya | ✅ Ya |
| **Masa aktif bertambah** | ❌ Tidak | ✅ Ya |
| **Tujuan** | Program sosial / kemanusiaan | Biaya penggunaan aplikasi |
| **Sifat** | Sukarela | Wajib untuk akses penuh |

## Langkah Operasional

### Donasi Saja (Tanpa Perpanjangan Langganan)
1. Buka menu **Langganan** atau **Sora Coin** > pilih tab **Donasi**.
2. Lihat daftar **program donasi** yang tersedia (nama, deskripsi, dan logo program).
3. Pilih program donasi yang ingin didukung.
4. Masukkan **jumlah koin** yang ingin didonasikan.
5. Tap **Lanjutkan** > periksa ringkasan transaksi.
6. Tap **Konfirmasi** — koin langsung dipotong dari saldo toko.
7. Email konfirmasi donasi dikirim ke Owner (berisi nama program, jumlah koin, dan nomor order).

### Donasi + Langganan Sekaligus (Satu Transaksi)
1. Buka menu **Langganan** > pilih paket langganan yang diinginkan.
2. Di halaman yang sama, aktifkan opsi **Tambah Donasi**.
3. Pilih **program donasi** dan masukkan **jumlah koin untuk donasi**.
4. Sistem menampilkan total koin yang akan dipotong: koin langganan + koin donasi.
5. Tap **Konfirmasi** — keduanya diproses dalam satu transaksi sekaligus.
6. Email konfirmasi gabungan dikirim ke Owner.

> ⚠️ **Hanya Owner** yang bisa melakukan donasi. Kasir dan karyawan tidak memiliki akses ke fitur ini.

## Format Nomor Order
- Donasi saja: `DON-{timestamp}` (contoh: `DON-1722160000000`)
- Langganan + donasi: `SUBDON-{timestamp}`

## Validasi Donasi
- Jika memasukkan jumlah koin donasi lebih dari 0, **wajib memilih program donasi** terlebih dahulu. Sistem akan menolak transaksi jika program donasi belum dipilih.
- Saldo koin toko harus mencukupi untuk total donasi (dan langganan jika digabung).

## Program Donasi yang Tersedia
Daftar program donasi dikelola oleh tim Sora dan bisa berubah sewaktu-waktu. Setiap program donasi menampilkan:
- **Nama** program
- **Deskripsi** singkat tujuan donasi
- **Logo** / **gambar banner** program

## FAQ & Troubleshooting

**Q: Apakah donasi akan memperpanjang masa aktif langganan saya?**
A: **Tidak.** Donasi adalah kontribusi sukarela ke program sosial dan tidak mempengaruhi masa aktif langganan sama sekali. Untuk memperpanjang masa aktif, gunakan fitur **Perpanjangan Langganan** secara terpisah.

**Q: Apakah donasi bisa dibatalkan atau di-refund?**
A: Donasi yang sudah dikonfirmasi **tidak bisa dibatalkan atau di-refund** karena koin langsung dipotong dari saldo saat konfirmasi. Pastikan program donasi dan jumlah koin sudah benar sebelum mengkonfirmasi.

**Q: Saya mau donasi tapi muncul error "pilih program donasi dulu". Bagaimana?**
A: Anda harus memilih program donasi terlebih dahulu dari daftar yang tersedia sebelum memasukkan jumlah koin. Tidak bisa melakukan donasi tanpa memilih program tujuan.

**Q: Apakah bisa donasi ke lebih dari satu program sekaligus?**
A: Dalam satu transaksi, hanya bisa memilih **satu program donasi**. Untuk donasi ke program berbeda, lakukan transaksi terpisah.

**Q: Berapa minimal koin yang bisa didonasikan?**
A: Minimal donasi adalah **1 koin**. Tidak ada jumlah maksimum, namun tentu saldo koin toko harus mencukupi.

**Q: Apakah ada bukti donasi yang bisa saya simpan?**
A: Ya. Setelah donasi berhasil, sistem mengirimkan **email konfirmasi** ke Owner berisi nomor order, nama program donasi, dan jumlah koin yang didonasikan. Riwayat donasi juga tercatat di **Riwayat Koin** toko.

**Q: Apakah kasir saya bisa lihat riwayat donasi yang sudah dilakukan?**
A: Riwayat transaksi koin (termasuk donasi) bisa dilihat di menu Riwayat Koin, namun hak aksesnya terbatas pada pengguna dengan izin yang sesuai. Biasanya hanya Owner yang bisa melihat seluruh riwayat koin.
