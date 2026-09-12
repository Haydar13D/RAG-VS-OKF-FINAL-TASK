---
id: DOC-19-SHIFT-KAS
title: Buka/Tutup Shift Kasir & Cash Drawer
category: kasir
target_role: kasir
tags:
- buka kasir
- tutup shift
- cash drawer
- modal kasir
- selisih uang
- petty cash
prerequisites:
- DOC-04-KARYAWAN
related:
- DOC-02-TRANSAKSI
- DOC-17-LAPORAN
---

## Deskripsi
Fitur Buka/Tutup Shift Kasir digunakan untuk mencatat modal uang tunai awal (*starting cash*), mengontrol arus masuk/keluar uang kas (*petty cash*), serta melakukan penghitungan saldo kasir (*cash count*) di akhir shift guna mencegah selisih uang.

## Langkah Operasional
1. **Buka Shift (Start Shift)**:
   - Saat pertama kali login di awal shift, layar modal **Buka Kasir** akan muncul.
   - Masukkan **Modal Uang Tunai Awal** yang ada di laci kasir (misal: Rp 500.000). Klik **Mulai Shift**.
2. **Pencatatan Kas Masuk/Keluar (Petty Cash)**:
   - Jika ada pengeluaran kasir mendadak (misal: beli es batu/gas), buka menu **Kelola Kas** > pilih **Kas Keluar**.
   - Masukkan jumlah uang dan keterangan pengeluaran.
3. **Tutup Shift (End Shift / Closing)**:
   - Di akhir jam kerja, klik menu **Tutup Kasir / End Shift**.
   - Hitung total fisik uang kertas dan koin di laci kasir, lalu input nilainya ke kolom **Jumlah Uang Fisik**.
   - Sistem akan membandingkan uang fisik dengan catatan sistem dan menampilkan **Selisih Kas** (Pas / Lebih / Kurang).
   - Klik **Cetak Laporan Closing Shift**.

## FAQ & Troubleshooting
**Q: Apa yang harus dilakukan jika terjadi Selisih Minus (uang fisik lebih kecil dari catatan sistem) saat Tutup Shift?**
A: Kasir wajib menginput **Alasan Selisih Kas** pada form closing (misal: "Salah Beri Kembalian" atau "Lupa Catat Kas Keluar"). Laporan selisih akan otomatis diteruskan ke Supervisor untuk diaudit.

**Q: Mengapa laci kasir (Cash Drawer) tidak terbuka otomatis saat cetak struk?**
A: Pastikan kabel RJ11 laci kasir sudah terhubung dengan port RJ11 pada printer thermal, dan opsi **Open Cash Drawer** pada menu *Pengaturan Printer* sudah di-centang.
