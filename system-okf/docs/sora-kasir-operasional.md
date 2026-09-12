---
id: DOC-29-SORA-KASIR
title: Operasional Kasir (Buka/Tutup Kasir, Pesanan, Meja, Void)
category: kasir
target_role: kasir
tags:
- kasir
- shift
- pesanan
- meja
- void
- transaksi
- riwayat
prerequisites:
- DOC-19-SHIFT-KAS
related:
- DOC-02-TRANSAKSI
- DOC-05-MEJA
- DOC-07-VOID
---

## Mulai Kasir (Buka Shift)
1. Masukkan modal awal pada kolom nominal kas awal (contoh: 300.000).
2. Tap tombol "Mulai Kasir" untuk mulai menerima transaksi.
3. Jika perlu menambah modal kembalian di tengah shift, ketik nominalnya di tabel "Tambah Modal".
4. Untuk mencatat pengeluaran dadakan (kas kecil), ketik nominal di bagian "Belanja Kas Kecil" dan lampirkan bukti nota jika diperlukan.

## Tutup Kasir (Akhiri Shift)
1. Tap tombol "Tutup Kasir".
2. Pada tabel penerimaan aktual, masukkan total uang tunai fisik di laci kasir, dan total pendapatan non-tunai (QRIS, debit, transfer).
3. Jika ada selisih (kas minus atau lebih), tambahkan catatan/keterangan penjelasan.
4. Proses tutup kasir selesai.

## Membuat Pesanan Baru
1. Tap tombol "Tambah Customer" untuk memasukkan data pelanggan beserta nomor meja, lalu tap "Simpan".
2. Pilih menu yang akan dipesan.
3. Tentukan apakah pesanan untuk dine-in atau takeaway, masukkan varian menu (jika ada permintaan khusus), dan tambahkan diskon jika perlu.
4. Tulis catatan khusus dari pelanggan jika ada (misal: "tanpa bawang"), atur jumlah porsi, lalu tap "Tambah Ke Keranjang".
5. Pilih metode pembayaran: cash, debit, atau e-wallet.
   - **Cash**: ketik nominal uang yang diterima.
   - **Transfer/Debit**: wajib cek mutasi rekening untuk memastikan uang sudah masuk sebelum menyelesaikan pembayaran.
   - **E-Wallet (QRIS, dll)**: pantau notifikasi uang masuk di aplikasi sebelum klik selesai.
6. Tap tombol "Bayar" untuk pelunasan, atau "Simpan" untuk menyimpan tagihan (belum dibayar).

**Catatan:** Pesanan yang dibuat otomatis muncul di halaman Tagihan → Meja Pesanan untuk diproses dapur.

## Mengelola Meja Pesanan
1. Pilih meja yang akan diproses.
2. Tambahkan nama dan nomor meja pelanggan jika belum ada.
3. Tap tombol "Checklist Dapur" di kiri atas cart nota pesanan.
4. Centang produk yang sudah selesai dimasak, lalu tap "Update Dapur".
5. Pilih metode pembayaran dan lanjutkan proses bayar (jika pesanan belum lunas).
6. Tap "Cetak Struk" untuk print fisik, atau tombol "WhatsApp" untuk kirim e-nota ke pelanggan. Tap "Clean Up" setelah pelanggan selesai.

**Catatan:** Jika pelanggan memesan lewat scan barcode dari meja, mereka bisa memantau dan mengunduh nota pesanan secara langsung dari HP mereka sendiri.

## Menambah Nomor Meja
- Untuk menambah banyak meja sekaligus: gunakan tombol "Buat Banyak Meja".
- Untuk menambah satu meja: masukkan nomor meja di kolom "Tambah Satu Meja Baru", lalu tap "Tambah Meja".

**Catatan:** Gunakan salah satu cara di atas secara terpisah (jangan digabung) agar penambahan nomor meja berhasil.

## Riwayat Nota Pesanan
- Gunakan tombol filter untuk melihat semua transaksi pada periode waktu tertentu (termasuk yang sukses, dibatalkan, maupun yang di-void).
- Tombol void di sebelah kanan tabel riwayat berfungsi menghapus pesanan yang sudah selesai. **Hanya bisa digunakan dalam batas waktu 1x24 jam.**

## Cara Void Transaksi
1. Tap tombol void di sebelah kanan tabel riwayat pesanan.
2. Pilih nama akun dan masukkan password.
3. Masukkan alasan void/pembatalan.
4. Tap "Ya, Batalkan" untuk menyelesaikan proses void.
