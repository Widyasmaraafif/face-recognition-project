# 🤖 Sistem Absensi Pengenalan Wajah (Face Recognition Attendance System)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![DeepFace](https://img.shields.io/badge/AI-DeepFace-orange.svg)](https://github.com/serengil/deepface)
[![Flask](https://img.shields.io/badge/Web-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)

Sistem absensi otomatis berbasis Python yang menggabungkan kecanggihan **DeepFace** untuk pengenalan wajah, **OpenCV** untuk pemrosesan video *real-time*, dan **Flask** untuk antarmuka web modern yang responsif.

## 🚀 Fitur Unggulan v3.0 (Web Edition)

- **🖥️ Akses Web & Multi-Device**: Antarmuka berbasis web menggunakan **Flask**, memungkinkan akses dari browser di berbagai perangkat (Smartphone, Laptop, Tablet).
- **📸 Client-Side Camera**: Menggunakan kamera perangkat pengguna melalui browser, mengurangi beban server dan tidak memerlukan kamera fisik yang terhubung ke server.
- **⚡ Threaded Recognition**: Pemrosesan pengenalan wajah dilakukan secara *asynchronous* (berulir) di sisi server untuk performa yang optimal dan tanpa jeda.
- **📊 Visualisasi Confidence Score**: Menampilkan persentase tingkat keyakinan AI secara langsung pada setiap wajah yang terdeteksi.
- **🛡️ Dashboard Admin Canggih (Streamlit)**:
  - **Filter Cerdas**: Lihat laporan berdasarkan rentang tanggal tertentu.
  - **Statistik Visual**: Grafik interaktif untuk melihat tren kehadiran per individu atau departemen.
  - **Ekspor Data**: Unduh laporan langsung ke format **Excel (.xlsx)** atau **CSV**.
- **🗄️ Integrasi Database (SQLite)**: Manajemen data terpusat dan aman menggunakan `attendance_system.db`.

## 🛠️ Persyaratan Sistem

- **Python**: Versi 3.10 atau lebih baru.
- **Hardware**: Kamera/Webcam pada perangkat klien (browser).
- **Koneksi**: Diperlukan saat pertama kali menjalankan untuk mengunduh model AI (seperti SFace).

## ⚙️ Instalasi

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/username/face-recognition-project.git
   cd face-recognition-project
   ```

2. **Buat Virtual Environment (Disarankan)**:
   ```bash
   python -m venv venv
   # Aktifkan di Windows:
   .\venv\Scripts\activate
   # Aktifkan di Linux/Mac:
   source venv/bin/activate
   ```

3. **Instal Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Cara Penggunaan

### 1. Registrasi Wajah Baru
Daftarkan profil dan wajah karyawan/pengguna sebelum melakukan absensi:
```bash
python register.py
```
- Ikuti instruksi di terminal (Nama, Departemen, Jabatan).
- Tekan **'s'** untuk menangkap dan menyimpan foto wajah.
- Tekan **'q'** untuk membatalkan proses.

### 2. Jalankan Aplikasi Absensi (Web Server)
Jalankan server Flask untuk mulai menerima absensi:
```bash
python app.py
```
- Akses melalui browser di `http://localhost:5000` atau alamat IP server Anda.
- Pastikan memberikan izin akses kamera pada browser.

### 3. Dashboard Admin (Laporan & Statistik)
Lihat dan kelola data kehadiran melalui dashboard interaktif:
```bash
streamlit run dashboard.py
```

## 📁 Struktur Proyek

- `app.py`: Server utama Flask untuk antarmuka web absensi.
- `dashboard.py`: Aplikasi Streamlit untuk visualisasi data dan laporan.
- `register.py`: Skrip untuk mendaftarkan wajah dan data profil baru.
- `main.py`: Aplikasi desktop berbasis OpenCV (Legacy/Offline).
- `config.py`: Pengaturan pusat (Model AI, Waktu Jeda, Direktori).
- `database.py`: Modul logika untuk interaksi dengan SQLite.
- `templates/`: File HTML untuk tampilan antarmuka web.
- `dataset/`: Folder penyimpanan foto wajah yang telah terdaftar.
- `attendance_system.db`: Database SQLite tempat semua data disimpan.
- `requirements.txt`: Daftar pustaka Python yang diperlukan.

## 🔧 Konfigurasi (`config.py`)

Anda dapat menyesuaikan sistem melalui file `config.py`:
- `MODEL_NAME`: Pilih model AI (Default: `SFace` - Ringan & Cepat).
- `ATTENDANCE_COOLDOWN`: Waktu tunggu (dalam detik) sebelum seseorang bisa absen lagi (Default: 60 detik).
- `DETECTOR_BACKEND`: Backend deteksi wajah (Default: `opencv`).

## ⚠️ Catatan Penting
- **HTTPS**: Browser modern mewajibkan koneksi HTTPS untuk mengakses kamera jika diakses dari luar `localhost`. Gunakan layanan seperti **Ngrok** untuk pengujian publik yang aman.
- **Pencahayaan**: Pastikan pencahayaan cukup saat pendaftaran dan absensi untuk hasil pengenalan yang maksimal.

## 🤝 Kontribusi
Kontribusi selalu terbuka! Silakan lakukan *Fork* repositori ini, buat *Branch* baru, dan kirimkan *Pull Request*.

## 📄 Lisensi
Proyek ini dilisensikan di bawah MIT License.
