# 🧵 Fashion Studio ETL Pipeline

ETL (Extract, Transform, Load) pipeline sederhana untuk mengambil data produk dari situs [Fashion Studio Dicoding](https://fashion-studio.dicoding.dev), memprosesnya, dan menyimpannya secara otomatis ke Google Sheets.

Proyek ini dibuat sebagai bagian dari pembelajaran fundamental pemrosesan data, dengan fokus pada penulisan kode modular dan implementasi unit testing.

---

## 🚀 Fitur Utama

- ✅ Scraping data produk (nama, kategori, harga, stok) dari website Fashion Studio
- 🔧 Pembersihan dan transformasi data untuk validasi dan konsistensi
- 📤 Penyimpanan otomatis ke Google Sheets menggunakan Google Sheets API
- 🧪 Unit testing dengan cakupan >90% untuk memastikan pipeline berjalan stabil
- 📁 Struktur modular: `extract.py`, `transform.py`, `load.py`

---

## ⚙️ Cara Menjalankan

1. **Install dependencies**

```bash
pip install -r requirements.txt

2. **Siapkan kredensial Google Sheets**
  - Buat Service Account di Google Cloud Console
  - Aktifkan Google Sheets API
  - Unduh file JSON kredensial dan simpan sebagai config/creds.json
  - Share Google Sheets kamu ke email service account (dengan akses Editor)

3. **Jalankan ETL pipeline**
```bash
python extract.py
python transform.py
python load.py

# Menjalankan skrip
python main.py

# Menjalankan unit test pada folder tests
python -m pytest tests

# Menjalankan test coverage pada folder tests
coverage run -m pytest tests

# Detail unit test dan coverage
pytest --cov=utils
pytest --cov=utils tests/

# Url Google Sheets:
https://docs.google.com/spreadsheets/d/1bYSconAsDjXMf9Qhp1KgRlk7wGw9I1jNzxPd_GeFdbQ/edit?usp=sharing

## 🛠️ Tools dan Teknologi
- Python
- BeautifulSoup – Web scraping
- gspread & Google Sheets API – Penyimpanan ke spreadsheet
- unittest – Unit testing
- pandas – Manipulasi data


