# Sistem Absensi Pengenalan Wajah (Face Recognition Attendance System)

Sistem absensi otomatis berbasis Python yang menggunakan pustaka **DeepFace** untuk pengenalan wajah dan **OpenCV** untuk pemrosesan video secara real-time.

## Fitur Utama

- **Pengenalan Wajah Real-time**: Mendeteksi dan mengenali wajah dari webcam.
- **Visualisasi UI**: Menampilkan kotak pembatas, nama pengguna, dan bar status pada video feed.
- **Model Ringan (SFace)**: Menggunakan model SFace (~37MB) untuk proses inisialisasi yang lebih cepat.
- **Pendaftaran Wajah Mudah**: Skrip khusus untuk mendaftarkan pengguna baru ke dalam dataset.
- **Log Absensi Otomatis**: Mencatat nama dan waktu kehadiran ke file `attendance.csv`.
- **Anti-Duplicate (Cooldown)**: Mencegah pencatatan ganda untuk orang yang sama dalam rentang waktu 60 detik.

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
Sebelum menjalankan sistem absensi, Anda perlu mendaftarkan wajah ke dalam dataset:
```bash
python register.py
```
- Masukkan nama saat diminta.
- Posisikan wajah di depan kamera.
- Tekan **'s'** untuk menyimpan foto.
- Tekan **'q'** untuk batal.

### 2. Menjalankan Sistem Absensi
Setelah wajah terdaftar, jalankan aplikasi utama:
```bash
python main.py
```
- Sistem akan memuat model AI (SFace).
- Wajah yang dikenali akan otomatis tercatat di `attendance.csv`.
- Tekan **'q'** pada jendela video untuk keluar.

## Struktur Proyek

- `main.py`: Aplikasi utama untuk pengenalan wajah dan absensi.
- `register.py`: Skrip untuk mendaftarkan wajah baru ke folder `dataset/`.
- `attendance.csv`: File log hasil absensi.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.
- `dataset/`: Folder penyimpanan foto wajah terdaftar.

## Catatan
- Pastikan pencahayaan cukup saat pendaftaran dan proses absensi untuk hasil yang maksimal.
- Foto di dalam folder `dataset/` harus dinamai dengan format `nama_orang.jpg` (otomatis dilakukan oleh `register.py`).
