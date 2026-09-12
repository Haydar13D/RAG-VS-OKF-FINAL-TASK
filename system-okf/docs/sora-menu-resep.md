---
id: DOC-32-SORA-MENU-RESEP
title: Kategori Menu, Menu Baru, Varian, Kemasan, dan Harga Online Food
category: menu
target_role: supervisor
tags:
- menu
- resep
- kategori
- varian
- kemasan
- online food
- HPP
- AI recommendation
prerequisites:
- DOC-11-MENU
related:
- DOC-12-VARIAN
- DOC-13-KEMASAN
- DOC-14-ONLINE-FOOD
---

## Menambah Banyak Menu Sekaligus (Bulk Upload)
1. Tap "Upload File" → pilih "Download Template" → tap "Download".
2. Simpan file "template_import_resep_menu.xlsx", buka di Excel atau aplikasi sejenis.
3. Isi data (Kode, Nama menu, Kategori, Keterangan) mengikuti contoh baris paling atas, lalu simpan.
   - **Penting:** kolom "Kategori" wajib dipilih dari drop-down, jangan diketik manual.
4. Kembali ke aplikasi → tap "Upload File" → pilih "File Data Menu Resep" → tap "Pilih File" → pilih file yang sudah diedit → tap "Import".
5. Menu berhasil masuk secara massal.

**Catatan Penting:** Pastikan kode dan nama produk berbeda dari yang sudah ada agar tidak bentrok. Meski sudah masuk lewat bulk upload, resep tiap menu tetap wajib diedit manual agar menjadi produk yang utuh dan siap jual.

## Membuat Kategori Menu
1. Ketik nama kategori.
2. Pilih warna icon dan icon kategori (bisa upload icon custom format .svg).
3. Tap "Simpan".

**Catatan:** Kategori digunakan untuk mengelompokkan produk makanan, sekaligus jadi opsi tombol pilihan menu di halaman kasir.

## Membuat Menu Baru
1. Ketik nama menu, buat kode menu (atau gunakan kode yang sudah ada), pilih kategori produk.
2. Masukkan deskripsi produk — buat sekreatif dan semenarik mungkin agar fitur AI recommendation lebih mudah merekomendasikan produk ke pelanggan.
3. Atur warna background, upload foto menu (format .png/.jpg, maksimal 200 KB).
4. Masukkan bahan baku untuk resep, ketik jumlah takaran (satuan otomatis mengikuti nama bahan), tap "Tambah". Ulangi sampai semua bahan baku masuk.
5. Tambahkan biaya regulasi jika perlu. Set harga jual — **harus di atas total HPP** yang tertera di tabel paling bawah. Klik "Simpan".

**Catatan:** Hasil bisa dicek di halaman Resep → Rincian → Resep dan halaman Pesanan.

## Membuat Varian Menu
1. Ketik nama varian menu, beri deskripsi yang menarik (agar AI lebih optimal menawarkan varian ini ke pelanggan).
2. Pilih menu yang akan dipasangkan dengan varian ini.
3. Pilih bahan baku, masukkan takaran (satuan otomatis update), tap "Tambah". Ulangi sampai semua bahan resep varian masuk.
4. Tambahkan biaya regulasi jika perlu. Set harga jual varian (wajib di atas total HPP). Tap "Simpan".

**Catatan:** Varian menu berpengaruh terhadap peningkatan pendapatan tiap produk. Hasil bisa dicek di halaman Resep → Rincian → Varian Menu.

## Membuat Kemasan (Packaging)
1. Ketik nama kemasan, pilih menu mana saja yang akan menggunakan kemasan ini.
2. Pilih bahan baku kemasan (misal: paper bag size S), masukkan jumlah takaran, tap "Tambah". Ulangi sampai semua bahan kemasan terinput.
3. Tambahkan biaya regulasi jika perlu. Set harga jual kemasan (di atas total HPP). Tap "Simpan".

**Catatan Penting:** Kemasan wajib disiapkan untuk semua produk sebelum mengaktifkan fitur online food. Hasil bisa dicek di halaman Resep → Rincian → Varian Kemasan.

## Mengatur Harga Khusus Online Food
1. Pilih layanan online food.
2. Pilih produk yang akan dimasukkan ke layanan tersebut, tap "Tambah". (Catatan: hanya produk yang sudah punya kemasan yang bisa dipilih.)
3. Atur biaya layanan (nominal, misal Rp 5.000, atau persentase, misal 20%) — harga produk otomatis menyesuaikan. Tap "Simpan".

**PENTING:**
- Pastikan harga yang diset sama persis dengan yang ada di aplikasi online food, agar rincian nota yang dicetak sesuai dengan versi toko di aplikasi tersebut.
- Sora Seventh tidak bekerja sama dengan pihak ketiga/layanan online food manapun — tetap wajib double-check mutasi rekening/saldo setiap ada transaksi online food sebelum menyelesaikan pembayaran.
