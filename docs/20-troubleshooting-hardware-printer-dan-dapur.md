---
type: fitur
title: Troubleshooting Hardware, Printer Struk & Kitchen Printer
category: pengaturan
tags: [hardware, printer thermal, printer dapur, bluetooth, lan, paper jam, troubleshooting]
---

## Deskripsi
Dokumen ini merupakan panduan penanganan kendala teknis pada perangkat keras (Hardware), seperti printer struk kasir, printer pesanan dapur (*Kitchen Printer*), pemindai barcode, dan koneksi jaringan thermal printer.

## Langkah Operasional
1. **Menghubungkan Printer Struk Kasir / Dapur**:
   - Buka menu **Pengaturan** > **Perangkat & Printer**.
   - Klik **Cari Perangkat Baru**. Pilih jenis koneksi: *Bluetooth*, *USB*, atau *Ethernet LAN (IP Address)*.
   - Atur fungsi printer: pilih **Printer Kasir (Struk)** atau **Printer Dapur (Kitchen Checker)**.
   - Pilih ukuran kertas (*58mm* atau *80mm*) dan klik **Test Print**.
2. **Pengaturan Printer Dapur Terpisah**:
   - Daftarkan IP Address printer dapur (misal: `192.168.1.200`).
   - Hubungkan kategori menu makanan ke Printer Dapur 1 (Koki) dan menu minuman ke Printer Dapur 2 (Barista).

## FAQ & Troubleshooting
**Q: Printer thermal tiba-tiba tidak mau mencetak struk padahal lampu indikator menyala biru/hijau?**
A: Lakukan langkah penanganan berikut:
   1. Cek roll kertas thermal: pastikan kertas tidak terbalik (sisi licin menghadap pemanas) dan tidak *Paper Jam*.
   2. Jika menggunakan Bluetooth: matikan dan nyalakan kembali Bluetooth tablet/HP kasir, lalu hubungkan ulang (*pair*).
   3. Jika menggunakan LAN: pastikan kabel LAN printer colok ke router yang sama dengan tablet kasir.

**Q: Mengapa struk pesanan makanan tidak keluar di printer dapur saat kasir checkout?**
A: Pastikan kategori menu makanan tersebut sudah di-mapping ke nama *Kitchen Printer* pada menu **Pengaturan Perangkat**, dan status printer dapur dalam keadaan *Online*.
