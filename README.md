# JournalHub

**JournalHub** adalah aplikasi web berbasis Flask yang menerapkan arsitektur Model-View-Controller (MVC). Aplikasi ini dirancang untuk mengelola jurnal, artikel, atau catatan secara online dengan fitur CRUD (Create, Read, Update, Delete).

## Daftar Isi

- [Fitur](#fitur)
- [Struktur Proyek](#struktur-proyek)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Konfigurasi](#konfigurasi)
- [Penggunaan](#penggunaan)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## Fitur

- Manajemen jurnal/artikel (tambah, lihat, edit, hapus)
- Autentikasi pengguna (opsional, jika diimplementasikan)
- Pencarian dan filter jurnal
- Tampilan responsif dan mudah digunakan
- Arsitektur MVC yang terstruktur

## Struktur Proyek

```
journal_website/
│
├── app/
│   ├── __init__.py
│   ├── models/         # Model (ORM/database)
│   ├── views/          # View (route & controller)
│   ├── templates/      # Template HTML (Jinja2)
│   └── static/         # File statis (CSS, JS, gambar)
│
├── run.py              # Entry point aplikasi
├── requirements.txt    # Daftar dependensi Python
└── README.md           # Dokumentasi proyek
```

## Persyaratan Sistem

- Python 3.7 atau lebih baru
- pip (Python package manager)
- (Opsional) virtualenv untuk lingkungan virtual

## Instalasi

1. **Clone repository:**
   ```bash
   git clone <url-repo-anda>
   cd journal_website
   ```

2. **Buat dan aktifkan virtual environment (opsional tapi disarankan):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi

Jalankan aplikasi dengan perintah berikut:

```bash
python run.py
```

Aplikasi akan berjalan di `http://127.0.0.1:5000/` secara default.

## Konfigurasi

- Konfigurasi aplikasi dapat diatur di file `app/__init__.py` atau file konfigurasi lain yang digunakan.
- Untuk mengubah mode debug, edit bagian berikut di `run.py`:
  ```python
  app.run(debug=True)
  ```

## Penggunaan

1. Buka browser dan akses `http://127.0.0.1:5000/`
2. Gunakan fitur yang tersedia untuk mengelola jurnal/artikel.
3. Ikuti petunjuk pada halaman utama aplikasi.# journalhub
