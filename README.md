# Sistem Absensi Pengenalan Wajah (Face Recognition Attendance System)

Sistem absensi otomatis berbasis Python yang menggunakan pustaka **DeepFace** untuk pengenalan wajah, **OpenCV** untuk pemrosesan video secara real-time, dan **SQLite** untuk manajemen data.

## Fitur Unggulan v2.0

- **Pengenalan Wajah Berulir (Threaded Recognition)**: Proses pengenalan wajah berjalan di thread terpisah, sehingga feed video tetap lancar (60 FPS) tanpa stuttering.
- **Visualisasi Confidence Score**: Menampilkan persentase tingkat keyakinan AI pada setiap wajah yang terdeteksi.
- **Profil Pengguna Lengkap**: Database kini mendukung penyimpanan data Departemen dan Jabatan untuk setiap pengguna.
- **Dashboard Admin Canggih**:
  - **Filter Tanggal**: Melihat laporan kehadiran pada rentang waktu tertentu.
  - **Visualisasi Statistik**: Grafik kehadiran per orang dan per departemen.
  - **Ekspor Data Multi-Format**: Unduh laporan kehadiran langsung ke format **Excel (.xlsx)** atau **CSV**.
  - **Galeri Dataset**: Melihat foto wajah yang telah terdaftar langsung dari dashboard.
- **Integrasi Database (SQLite)**: Manajemen data terpusat dan efisien di `attendance_system.db`.
- **Anti-Duplicate (Cooldown)**: Mencegah pencatatan ganda dalam rentang waktu yang dapat dikonfigurasi.

## Persyaratan Sistem

- Python 3.10+
- Webcam
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

### 2. Menjalankan Sistem Absensi
Jalankan aplikasi utama untuk mulai mengenali wajah:
```bash
python main.py
```
- Feed video akan tetap lancar berkat teknologi threading.
- Status deteksi dan confidence score muncul secara real-time.
- Tekan **'q'** pada jendela video untuk keluar.

### 3. Membuka Dashboard Admin
Lihat laporan dan statistik absensi melalui browser:
```bash
streamlit run dashboard.py
```

## Struktur Proyek

- `main.py`: Aplikasi utama dengan pengenalan wajah threaded.
- `register.py`: Skrip pendaftaran wajah dengan profil lengkap.
- `dashboard.py`: Dashboard admin interaktif dengan fitur ekspor Excel.
- `database.py`: Modul manajemen database SQLite.
- `config.py`: File konfigurasi (Model AI, Cooldown, Direktori).
- `attendance_system.db`: Database SQLite pusat.
- `dataset/`: Folder penyimpanan foto wajah terdaftar.
- `requirements.txt`: Daftar pustaka Python terbaru.

## Catatan
- Gunakan pencahayaan yang cukup untuk mendapatkan tingkat kepercayaan (Confidence Score) yang tinggi.
- Model default yang digunakan adalah **SFace** (~37MB) karena kecepatannya yang optimal untuk real-time.
