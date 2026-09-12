---
id: DOC-22-PELANGGAN-LENGKAP
title: Manajemen Pelanggan (Customer) — Lengkap
category: sistem
target_role: owner
tags:
- pelanggan
- customer
- member
- tambah pelanggan
- blokir
- unblock
- tipe pelanggan
- menu favorit
- avatar
- tanggal lahir
- filter pelanggan
---

## Deskripsi
Fitur Manajemen Pelanggan digunakan untuk mencatat dan mengelola database pembeli yang terdaftar di toko. Setiap pelanggan terikat ke satu toko, sehingga data antar-toko tidak saling bercampur. Kasir bisa mendaftarkan pelanggan baru, memperbarui datanya, melihat menu favorit mereka, serta memblokir pelanggan yang bermasalah.

## Tipe Pelanggan
Sistem mengenal 3 tipe pelanggan yang ditetapkan otomatis:

| Tipe | Keterangan |
|---|---|
| **Baru** | Status saat pertama kali didaftarkan |
| **Pelanggan** | Status reguler setelah beberapa transaksi |
| **Member** | Status member loyalty program |

## Langkah Operasional

### Mendaftarkan Pelanggan Baru
1. Di layar Kasir saat transaksi, tap tombol **+ Tambah Pelanggan** di bagian atas nota.
2. Isi **Nama Lengkap** dan **Nomor HP** (format wajib: diawali `+62`, panjang 10–15 digit).
3. Opsional: upload **foto avatar** (PNG/JPG, maks 200KB) dan isi **Tanggal Lahir**.
4. Tap **Simpan** — pelanggan langsung terdaftar dan bisa dipilih di transaksi berikutnya.

### Memperbarui Data Pelanggan
1. Buka menu **Pelanggan** > cari nama atau nomor HP.
2. Tap nama pelanggan > tap **Edit**.
3. Ubah data yang perlu (nama, nomor HP, foto, atau tanggal lahir) > tap **Simpan**.

### Melihat Detail & Menu Favorit Pelanggan
1. Buka menu **Pelanggan** > tap nama pelanggan.
2. Di halaman detail, sistem menampilkan otomatis **menu yang paling sering dipesan** oleh pelanggan tersebut berdasarkan riwayat transaksi.

### Memblokir Pelanggan (Blacklist)
1. Buka menu **Pelanggan** > cari pelanggan yang ingin diblokir.
2. Tap nama pelanggan > tap **Blokir**.
3. Masukkan **password akun** admin/owner untuk konfirmasi.
4. Isi **Alasan** dan **Keterangan** pemblokiran > tap **Blokir**.
5. Pelanggan berstatus "Diblokir" dan tidak bisa digunakan di transaksi baru.

> ⚠️ Hanya pengguna dengan hak akses **Blokir Pelanggan** yang bisa melakukan ini (biasanya Owner atau Admin).

### Membuka Blokir Pelanggan (Unblock)
1. Buka tab **Pelanggan Diblokir** > cari pelanggan.
2. Tap ikon gembok / tap **Buka Blokir**.
3. Masukkan password, isi alasan unblock > tap **Konfirmasi**.

### Filter & Pencarian Pelanggan
Gunakan filter berikut di daftar pelanggan:
- **Cari**: berdasarkan nama atau nomor HP
- **Tanggal**: filter rentang waktu pendaftaran
- **Status**: `Aktif` atau `Diblokir`
- **Tipe**: `Baru`, `Pelanggan`, atau `Member`

## FAQ & Troubleshooting

**Q: Apakah satu nomor HP bisa didaftarkan untuk dua pelanggan berbeda?**
A: Tidak. Dalam satu toko, nama pelanggan dan nomor HP harus unik. Jika nomor HP sudah terdaftar, sistem akan menolak dengan pesan error. Tapi nomor HP yang sama bisa digunakan di toko yang berbeda.

**Q: Muncul error "nama customer ini udah dipakai" padahal namanya beda — kenapa?**
A: Pastikan tidak ada spasi tersembunyi atau perbedaan kecil di penulisan nama. Sistem melakukan pencocokan nama secara ketat. Coba cari nama tersebut di daftar pelanggan untuk memastikan.

**Q: Saya salah input nomor HP pelanggan, bisa diubah?**
A: Bisa. Masuk ke **Edit Pelanggan**, ubah nomor HP ke yang benar. Sistem akan memvalidasi bahwa nomor baru tidak digunakan pelanggan lain di toko.

**Q: Kenapa pelanggan yang sudah dihapus masih muncul di laporan transaksi lama?**
A: Hapus pelanggan bersifat *soft delete* — data tidak benar-benar hilang dari database agar riwayat transaksi tetap utuh untuk keperluan laporan. Pelanggan hanya tidak akan muncul lagi di daftar aktif.

**Q: Apa bedanya blokir dan hapus pelanggan?**
A: Pelanggan yang **diblokir** masih ada di sistem, riwayat tetap ada, tapi tidak bisa dipakai transaksi baru. Pelanggan yang **dihapus** tidak muncul di daftar, tapi data historisnya tetap tersimpan di backend.

**Q: Apakah kasir biasa bisa memblokir pelanggan?**
A: Tidak. Pemblokiran memerlukan hak akses khusus dan konfirmasi password, yang biasanya hanya dimiliki Owner atau Admin.

**Q: Apa itu "menu favorit" yang muncul di detail pelanggan?**
A: Sistem secara otomatis menganalisis riwayat pemesanan pelanggan tersebut dan menampilkan menu atau varian yang paling sering dipesan. Berguna untuk memberi rekomendasi atau promo yang relevan.

**Q: Apakah foto avatar pelanggan ada batasan ukuran?**
A: Ya. Foto avatar maksimal **200KB** dengan format **PNG, JPG, atau JPEG**. Foto yang terlalu besar atau format tidak sesuai akan ditolak oleh sistem.
