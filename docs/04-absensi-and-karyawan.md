---
type: fitur
title: Absensi & Manajemen Karyawan
category: absensi
tags: [absensi, karyawan, presensi, clock in, shift, hak akses, role]
---

## Deskripsi
Fitur Absensi & Karyawan digunakan untuk mencatat presensi masuk/pulang staf, menghitung keterlambatan otomatis berdasarkan jam kerja (shift), serta mengelola hak akses akun pengguna sesuai jabatan.

## Langkah Operasional
1. **Pengaturan Hak Akses Jabatan**: Buka menu **Absensi** > tab **Aksesibilitas** > klik **Tambah Jabatan**. Centang fitur yang boleh diakses (misal: Kasir hanya bisa transaksi, Manager bisa lihat laporan).
2. **Tambah Akun Karyawan**: Buka tab **Karyawan** > klik **Tambah Karyawan**. Isi NIP, Nama, Email, Username, Password, Jabatan, dan Jam Kerja Shift.
3. **Melakukan Presensi (Clock In / Clock Out)**: 
   - Karyawan membuka menu **Absensi** > tab **Presensi**.
   - Pilih **Nama Akun**, masukkan **PIN/Password**, lalu klik **Absen Masuk** saat datang atau **Absen Pulang** saat selesai shift.
4. **Export Laporan Absensi**: Klik tombol **Export Data Absensi** di pojok kanan atas > tentukan periode tanggal > unduh file Excel.

## FAQ & Troubleshooting
**Q: Bagaimana jika karyawan lupa melakukan Absen Pulang saat selesai shift?**
A: Admin/Owner dapat melakukan penyesuaian manual melalui menu **Absensi** > **Riwayat Presensi** > klik **Edit Jam Pulang** pada baris nama karyawan yang bersangkutan.

**Q: Apakah sistem bisa mendeteksi jika karyawan datang terlambat?**
A: Ya, sistem secara otomatis menghitung selisih menit keterlambatan (*Auto Late Detection*) jika waktu **Absen Masuk** melebihi jam mulai shift yang telah dikonfigurasi.