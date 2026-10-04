# 🏥 Dasbor Visualisasi Data BPS 2026: Ketahanan Kesehatan & Impor Farmasi

Dasbor interaktif ini dibangun menggunakan **Streamlit** dan **Plotly** untuk menyajikan analisis komprehensif mengenai **Ketahanan Kesehatan Provinsi di Indonesia** dan **Struktur Impor Produk Farmasi**, bersumber dari data statistik publikasi **Badan Pusat Statistik (BPS)**.

---

## 👤 Informasi Mahasiswa / Pembuat
* **Nama:** FAIZUL HANIF
* **NIM:** 222313074
* **Kelas:** 3SD1 / Politeknik Statistika STIS
* **Mata Kuliah:** Visualisasi Data dan Informasi (2026)
* **Tautan Live Dashboard:** [Dasbor Ketahanan Kesehatan & Impor Farmasi](https://uas-visdat-2026-fh05.streamlit.app)

---

## 📌 Topik Visualisasi Data

Dasbor ini mencakup 3 dari 6 topik visualisasi data sesuai ketentuan ujian:

### 1. Visualisasi Data Berdimensi Tinggi (Analisis Multivariat)
* **Tujuan:** Pemetaan indikator ketahanan kesehatan antar-34 provinsi di Indonesia.
* **Teknik Visualisasi:**
  * **PCA Scatter Biplot (Reduksi Dimensi):** Meringkas variansi 8 indikator utama ke dalam PC1 dan PC2.
  * **Parallel Coordinates Plot:** Membandingkan pola multi-indikator kesehatan lintas provinsi.
  * **Heatmap Korelasi Pearson:** Analisis hubungan keterikatan antar-indikator kesehatan.

### 2. Visualisasi Data Aliran (*Flow/Movement Data*)
* **Tujuan:** Analisis volume dan arah pergerakan transaksi impor produk farmasi dari negara mitra dagang ke Indonesia.
* **Teknik Visualisasi:**
  * **Diagram Sankey:** Mengkodekan volume nilai transaksi (USD) melalui ketebalan pita (*link width*) dari Negara Asal ke Pos Tarif HS 4-Digit.
  * **Matriks Origin-Destination (OD Heatmap):** Mengkodekan intensitas perdagangan menggunakan skala gradasi warna.
* **Fitur Interaktif:** Slider Top-N Negara Asal dan Multiselect Filter Negara Mitra.

### 3. Visualisasi Data Berhierarki / Berjenjang
* **Tujuan:** Analisis struktur dan proporsi nilai komoditas impor farmasi berdasarkan pengkodean Harmonized System (HS Code).
* **Teknik Visualisasi:**
  * **Treemap Diagram:** Memvisualisasikan proporsi area (*luas kotak*) dan pangsa pasar (*warna*).
  * **Sunburst Diagram:** Struktur radial multi-level dengan fitur interaktif *drill-down* (Bab ➔ HS 4-Digit ➔ Deskripsi 8-Digit).

---

## 📑 Sumber Data Utama (BPS) & Lisensi
Sesuai dengan ketentuan ujian poin 2b, seluruh data utama bersumber dari publikasi dan tabel statistik resmi **Badan Pusat Statistik (BPS)** tahun 2024–2025, antara lain:
* Angka Harapan Hidup (AHH) Menurut Provinsi
* Angka Kesakitan (Morbiditas) Menurut Provinsi
* Akses Air Minum Layak & Sanitasi Layak Rumah Tangga
* Pertolongan Persalinan oleh Tenaga Kesehatan Terlatih
* Persentase Penduduk Memiliki JKN/BPJS
* Jumlah Fasilitas Kesehatan & Penduduk Menurut Provinsi
* Persentase Anak Penerima Imunisasi Dasar Lengkap
* Data Perdagangan Luar Negeri Impor Komoditas Farmasi (HS Code)

---

## 📂 Struktur Direktori Project

```text
UAS_Visdat_2026/
├── .streamlit/
│   └── config.toml          # Konfigurasi tema & style Streamlit
├── data/
│   ├── raw/                 # File dataset mentah BPS (.xlsx)
│   └── cleaned/             # File dataset hasil pre-processing (.csv)
│       ├── flow_clean.csv
│       ├── hierarki_clean.csv
│       └── multivariat_clean.csv
├── app.py                   # File utama aplikasi Streamlit
├── data_prep.py             # Script pembersihan data
├── logo.PNG                 # Logo Politeknik Statistika STIS
├── style.css                # Custom CSS styling dasbor
├── requirements.txt         # Daftar dependency Python
├── .gitignore               # Konfigurasi berkas yang diabaikan Git
└── README.md                # Dokumentasi project