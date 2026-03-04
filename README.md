# Sistem Absensi Pengenalan Wajah (Face Recognition Attendance System)

Sistem absensi otomatis berbasis Python yang menggunakan pustaka **DeepFace** untuk pengenalan wajah, **OpenCV** untuk pemrosesan video secara real-time, dan **SQLite** untuk manajemen data.

## Fitur Utama

- **Pengenalan Wajah Real-time**: Mendeteksi dan mengenali wajah dari webcam dengan visualisasi kotak pembatas dan nama.
- **Integrasi Database (SQLite)**: Menyimpan data pengguna dan log absensi secara terstruktur, menggantikan CSV tradisional.
- **Dashboard Admin (Streamlit)**: Antarmuka web modern untuk melihat statistik absensi, daftar pengguna, dan galeri foto dataset.
- **Visualisasi UI Baru**: Menampilkan riwayat absensi terbaru (Recent Logs) langsung pada layar feed video.
- **Model Ringan (SFace)**: Menggunakan model SFace (~37MB) untuk proses inisialisasi yang lebih cepat dan efisien.
- **Pendaftaran Wajah Mudah**: Skrip pendaftaran terintegrasi langsung dengan database.
- **Anti-Duplicate (Cooldown)**: Mencegah pencatatan ganda dalam rentang waktu tertentu (default 60 detik).
- **File Konfigurasi Terpusat**: Pengaturan model, cooldown, dan direktori dapat diubah dengan mudah di `config.py`.

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
Daftarkan wajah ke dalam database dan dataset:
```bash
python register.py
```
- Masukkan nama saat diminta.
- Tekan **'s'** untuk menyimpan foto.
- Tekan **'q'** untuk batal.

### 2. Menjalankan Sistem Absensi
Jalankan aplikasi utama untuk mulai mengenali wajah:
```bash
python main.py
```
- Wajah yang dikenali akan otomatis tercatat di database `attendance_system.db`.
- Riwayat singkat akan muncul di pojok kanan bawah layar.
- Tekan **'q'** pada jendela video untuk keluar.

### 3. Membuka Dashboard Admin
Lihat laporan dan statistik absensi melalui browser:
```bash
streamlit run dashboard.py
```

## Struktur Proyek

- `main.py`: Aplikasi utama pengenalan wajah.
- `register.py`: Skrip pendaftaran wajah baru.
- `dashboard.py`: Dashboard admin berbasis Streamlit.
- `database.py`: Modul untuk interaksi dengan database SQLite.
- `config.py`: File konfigurasi sistem.
- `attendance_system.db`: Database SQLite (otomatis dibuat).
- `dataset/`: Folder penyimpanan foto wajah terdaftar.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.

## Catatan
- Pastikan pencahayaan cukup saat pendaftaran dan proses absensi.
- Jika ingin mengganti model (misal ke VGG-Face atau Facenet), ubah nilai `MODEL_NAME` di `config.py`.
