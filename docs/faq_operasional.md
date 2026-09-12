# Kumpulan FAQ Operasional POS Sora Seventh

## 1. Transaksi & Pembayaran Kasir

### Q: Bagaimana cara melakukan Void Nota / Pembatalan Transaksi?
Untuk membatalkan transaksi yang sudah tercetak, gunakan fitur **Void Nota**:
1. Masuk ke menu **Daftar Transaksi** di bilah navigasi kiri.
2. Cari dan klik **Nomor Nota** yang ingin dibatalkan.
3. Klik tombol **Atur Transaksi** > pilih **Void Nota**.
4. Masukkan **Alasan Pembatalan** dan **PIN Supervisor/Manager**.
5. Klik **Konfirmasi Void**.

⚠️ **Catatan Penting:**
- Fitur Void Nota memerlukan otorisasi akun bertipe **Supervisor** atau **Owner**.
- Transaksi yang sudah di-void akan otomatis mengembalikan stok barang ke inventaris (*auto-return inventory*).

---

### Q: Bagaimana cara membagi tagihan (Split Bill) untuk pelanggan?
Untuk memisahkan item pesanan menjadi beberapa nota pembayaran berbeda:
1. Pada layar transaksi pembayaran, klik tombol **Split Bill** di pojok kanan bawah.
2. Pilih mode pembagian: **Berdasarkan Item** atau **Berdasarkan Nominal**.
3. Pindahkan item pesanan ke kelompok **Tagihan 1**, **Tagihan 2**, dst.
4. Selesaikan proses pembayaran untuk masing-masing tagihan satu per satu.
5. Klik **Cetak Semua Struk**.

---

### Q: Apakah transaksi bisa dilakukan jika koneksi internet terputus (Offline Mode)?
Ya, Sora Seventh POS mendukung **Offline Mode**:
- Transaksi tunai tetap dapat dilakukan seperti biasa.
- Data transaksi akan disimpan secara lokal di memori browser/perangkat kasir.
- Setelah koneksi internet kembali terhubung, sistem akan otomatis melakukan **Sync Data** ke cloud server.

⚠️ **Catatan:** Transaksi non-tunai (QRIS & Kartu Debit) membutuhkan koneksi internet aktif.

---

## 2. Inventaris, Stok & Bahan Baku

### Q: Bagaimana cara melakukan Stok Opname (Penyesuaian Stok)?
Untuk mencocokkan jumlah stok fisik di toko dengan stok di aplikasi:
1. Buka menu **Inventaris** > **Stok Opname**.
2. Klik tombol **+ Buat Sesi Opname Baru**.
3. Pilih **Kategori Produk** atau **Bahan Baku** yang ingin dihitung.
4. Input jumlah **Stok Fisik** hasil perhitungan nyata.
5. Sistem akan menampilkan **Selisih Stok** (Plus/Minus).
6. Masukkan **Keterangan Selisih** (misal: *Barang Rusak / Kadaluarsa*), lalu klik **Simpan & Sesuaikan**.

---

### Q: Apakah satuan bahan baku yang sudah dibuat bisa diubah?
Satuan dasar bahan baku (seperti *Gram*, *Ml*, *Pcs*) diisi pada saat pembuatan bahan baku pertama kali. 
- **Jika bahan baku belum pernah digunakan dalam resep:** Anda dapat mengubahnya via menu **Inventaris** > **Bahan Baku** > **Edit**.
- **Jika bahan baku sudah memiliki riwayat transaksi/resep:** Satuan dasar **tidak disarankan untuk diubah** secara langsung karena akan merusak histori HPP. Solusinya: Buat item bahan baku baru dengan satuan yang benar, lalu nonaktifkan bahan baku lama.

---

## 3. Hardware & Perangkat Tambahan

### Q: Bagaimana cara menghubungkan Printer Thermal Struk?
1. Pastikan printer thermal sudah terhubung via Bluetooth, USB, atau LAN network.
2. Pada aplikasi POS, buka menu **Pengaturan** > **Perangkat & Printer**.
3. Klik **Cari Perangkat Baru**.
4. Pilih nama printer thermal Anda (contoh: *Epson TM-T82* atau *PRINTER-58MM*).
5. Atur **Ukuran Kertas** (58mm atau 80mm).
6. Klik **Uji Cetak (Test Print)** untuk memastikan koneksi berhasil.


4. Fitur Utama (sudah terdokumentasi, siap pakai)
Bahan Baku

Q: Bagaimana cara menambah bahan baku baru? A: Buka menu Bahan Baku, pilih Kategori, klik "Buat Bahan Baku", isi Kode, Nama, Minimum Stok, Total Stok, Satuan, dan Harga Satuan. Harga satuan penting diisi presisi (misal per gram) karena jadi acuan perhitungan biaya resep. (sumber: fitur-bahan-baku.md)

Stok

Q: Bagaimana cara menambah/mengurangi stok bahan baku? A: Buka menu Bahan Baku → Riwayat Stok Bahan Baku, pilih "Tambah Stok" atau "Kurangi Stok", pilih bahan baku, isi jumlah dan harga total. Untuk restock banyak sekaligus, gunakan fitur Import File. (sumber: fitur-atur-stok-bahan.md)

Regulasi / Service Charge

Q: Apa itu regulasi di Sora Seventh? A: Regulasi adalah aturan biaya tambahan berupa persentase (misal service charge) yang bisa dibebankan ke pembeli atau ditanggung penjual sendiri sebagai biaya operasional. Dibuat lewat Pengaturan → Regulasi. (sumber: fitur-regulasi.md — catatan: mekanisme pasti pengaruh ke Harga Jual masih perlu verifikasi tim)


# Kumpulan FAQ Operasional POS Sora Seventh

## 1. Transaksi & Pembayaran Kasir

### Q: Bagaimana cara melakukan Void Nota / Pembatalan Transaksi?
Untuk membatalkan transaksi yang sudah tercetak, gunakan fitur **Void Nota**:
1. Masuk ke menu **Daftar Transaksi** di bilah navigasi kiri.
2. Cari dan klik **Nomor Nota** yang ingin dibatalkan.
3. Klik tombol **Atur Transaksi** > pilih **Void Nota**.
4. Masukkan **Alasan Pembatalan** dan **PIN Supervisor/Manager**.
5. Klik **Konfirmasi Void**.

⚠️ **Catatan Penting:**
- Fitur Void Nota memerlukan otorisasi akun bertipe **Supervisor** atau **Owner**.
- Transaksi yang sudah di-void akan otomatis mengembalikan stok barang ke inventaris (*auto-return inventory*).

---

### Q: Bagaimana cara membagi tagihan (Split Bill) untuk pelanggan?
Untuk memisahkan item pesanan menjadi beberapa nota pembayaran berbeda:
1. Pada layar transaksi pembayaran, klik tombol **Split Bill** di pojok kanan bawah.
2. Pilih mode pembagian: **Berdasarkan Item** atau **Berdasarkan Nominal**.
3. Pindahkan item pesanan ke kelompok **Tagihan 1**, **Tagihan 2**, dst.
4. Selesaikan proses pembayaran untuk masing-masing tagihan satu per satu.
5. Klik **Cetak Semua Struk**.

---

### Q: Apakah transaksi bisa dilakukan jika koneksi internet terputus (Offline Mode)?
Ya, Sora Seventh POS mendukung **Offline Mode**:
- Transaksi tunai tetap dapat dilakukan seperti biasa.
- Data transaksi akan disimpan secara lokal di memori browser/perangkat kasir.
- Setelah koneksi internet kembali terhubung, sistem akan otomatis melakukan **Sync Data** ke cloud server.

⚠️ **Catatan:** Transaksi non-tunai (QRIS & Kartu Debit) membutuhkan koneksi internet aktif.

---

## 2. Inventaris, Stok & Bahan Baku

### Q: Bagaimana cara melakukan Stok Opname (Penyesuaian Stok)?
Untuk mencocokkan jumlah stok fisik di toko dengan stok di aplikasi:
1. Buka menu **Inventaris** > **Stok Opname**.
2. Klik tombol **+ Buat Sesi Opname Baru**.
3. Pilih **Kategori Produk** atau **Bahan Baku** yang ingin dihitung.
4. Input jumlah **Stok Fisik** hasil perhitungan nyata.
5. Sistem akan menampilkan **Selisih Stok** (Plus/Minus).
6. Masukkan **Keterangan Selisih** (misal: *Barang Rusak / Kadaluarsa*), lalu klik **Simpan & Sesuaikan**.

---

### Q: Apakah satuan bahan baku yang sudah dibuat bisa diubah?
Satuan dasar bahan baku (seperti *Gram*, *Ml*, *Pcs*) diisi pada saat pembuatan bahan baku pertama kali. 
- **Jika bahan baku belum pernah digunakan dalam resep:** Anda dapat mengubahnya via menu **Inventaris** > **Bahan Baku** > **Edit**.
- **Jika bahan baku sudah memiliki riwayat transaksi/resep:** Satuan dasar **tidak disarankan untuk diubah** secara langsung karena akan merusak histori HPP. Solusinya: Buat item bahan baku baru dengan satuan yang benar, lalu nonaktifkan bahan baku lama.

---

## 3. Hardware & Perangkat Tambahan

### Q: Bagaimana cara menghubungkan Printer Thermal Struk?
1. Pastikan printer thermal sudah terhubung via Bluetooth, USB, atau LAN network.
2. Pada aplikasi POS, buka menu **Pengaturan** > **Perangkat & Printer**.
3. Klik **Cari Perangkat Baru**.
4. Pilih nama printer thermal Anda (contoh: *Epson TM-T82* atau *PRINTER-58MM*).
5. Atur **Ukuran Kertas** (58mm atau 80mm).
6. Klik **Uji Cetak (Test Print)** untuk memastikan koneksi berhasil.   