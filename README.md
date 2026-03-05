# Sistem Absensi Pengenalan Wajah (Face Recognition Attendance System)

Sistem absensi otomatis berbasis Python yang menggunakan pustaka **DeepFace** untuk pengenalan wajah, **OpenCV** untuk pemrosesan video, dan **Flask** untuk antarmuka web yang bisa diakses secara online.

## Fitur Unggulan v3.0 (Web Edition)

- **Akses Web & Online**: Kini hadir dengan antarmuka web menggunakan **Flask**, memungkinkan akses dari browser di perangkat apapun (HP, Laptop, Tablet).
- **Client-Side Camera**: Menggunakan kamera perangkat pengguna (browser) untuk pemrosesan, sehingga server tidak perlu memiliki kamera fisik.
- **Pengenalan Wajah Berulir (Threaded Recognition)**: Proses pengenalan wajah yang efisien di sisi server.
- **Visualisasi Confidence Score**: Menampilkan persentase tingkat keyakinan AI pada setiap wajah yang terdeteksi di browser.
- **Dashboard Admin Canggih (Streamlit)**:
  - **Filter Tanggal**: Melihat laporan kehadiran pada rentang waktu tertentu.
  - **Visualisasi Statistik**: Grafik kehadiran per orang dan per departemen.
  - **Ekspor Data Multi-Format**: Unduh laporan kehadiran langsung ke format **Excel (.xlsx)** atau **CSV**.
- **Integrasi Database (SQLite)**: Manajemen data terpusat dan efisien di `attendance_system.db`.

## Persyaratan Sistem

- Python 3.10+
- Webcam (pada perangkat client/browser)
- Koneksi internet (hanya untuk unduhan model pertama kali)

## Instalasi

1. Clone repositori ini atau ekstrak file proyek.
2. Instal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Penggunaan

### 1. Pendaftaran Wajah Baru
Daftarkan wajah dengan data lengkap:
```bash
python register.py
```
- Masukkan nama, departemen, dan jabatan.
- Tekan **'s'** untuk menyimpan foto.
- Tekan **'q'** untuk batal.

### 2. Menjalankan Aplikasi Web (Untuk Penggunaan Online/Lokal)
Jalankan server Flask:
```bash
python app.py
```
- Buka browser dan akses `http://localhost:5000` atau alamat IP server Anda.
- Izinkan akses kamera pada browser.
- Sistem akan mulai memindai wajah secara otomatis.

### 3. Membuka Dashboard Admin
Lihat laporan dan statistik absensi melalui browser:
```bash
streamlit run dashboard.py
```

## Struktur Proyek

- `app.py`: Server Flask untuk aplikasi web utama.
- `templates/`: Folder berisi file HTML untuk antarmuka web.
- `main.py`: Aplikasi desktop (Legacy/Offline).
- `register.py`: Skrip pendaftaran wajah dengan profil lengkap.
- `dashboard.py`: Dashboard admin interaktif.
- `database.py`: Modul manajemen database SQLite.
- `config.py`: File konfigurasi (Model AI, Cooldown, Direktori).
- `attendance_system.db`: Database SQLite pusat.
- `dataset/`: Folder penyimpanan foto wajah terdaftar.
- `requirements.txt`: Daftar pustaka Python terbaru.

## Catatan
- Untuk penggunaan "Online" di luar jaringan lokal, Anda perlu melakukan *Port Forwarding* atau menggunakan layanan seperti *Ngrok* untuk mengekspos port 5000.
- Pastikan menggunakan HTTPS jika ingin mengakses kamera dari domain publik (persyaratan keamanan browser modern).
