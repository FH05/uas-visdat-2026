import pandas as pd
import numpy as np
import os

# Memastikan folder penyimpanan data bersih ada
os.makedirs('data/cleaned', exist_ok=True)

# Fungsi fleksibel untuk mendeteksi lokasi file
def find_file(filename):
    if os.path.exists(filename):
        return filename
    elif os.path.exists(os.path.join('data', 'raw', filename)):
        return os.path.join('data', 'raw', filename)
    else:
        raise FileNotFoundError(
            f"File '{filename}' tidak ditemukan! Pastikan file tersebut ada di folder 'UAS_Visdat_2026' "
            f"atau di dalam folder 'data/raw/'."
        )

print("--- Memulai Pra-pemrosesan Data BPS ---")

# ==========================================
# 1. PEMROSESAN DATA MULTIVARIAT (file1.xlsx)
# ==========================================
path1 = find_file('file1.xlsx')
df1 = pd.read_excel(path1)

# Filter baris agregat nasional ('INDONESIA') agar tidak merusak PCA
df1_clean = df1[df1['PROVINSI'] != 'INDONESIA'].copy()
df1_clean.to_csv('data/cleaned/multivariat_clean.csv', index=False)
print(f"[OK] Multivariat: {len(df1_clean)} Provinsi diproses dari '{path1}'.")

# ==========================================
# 2. PEMROSESAN DATA BERHIERARKI (file2.xlsx)
# ==========================================
path2 = find_file('file2.xlsx')
df2 = pd.read_excel(path2)

df2['Level_1'] = 'Bab 30 (Produk Farmasi)'
df2['HS_4Digit'] = 'HS ' + df2['Kode HS'].str.extract(r'\[(\d{4})')
df2['Kode_8Digit'] = df2['Kode HS'].str.extract(r'\[(\d{8})\]')
df2['Deskripsi'] = df2['Kode HS'].str.replace(r'\[\d+\]\s*', '', regex=True)

# Menghitung persentase share sebagai variabel warna
total_nilai = df2['nilai'].sum()
df2['Persentase_Share'] = (df2['nilai'] / total_nilai) * 100

df2.to_csv('data/cleaned/hierarki_clean.csv', index=False)
print(f"[OK] Hierarki: {len(df2)} Komoditas diproses dari '{path2}'.")

# ==========================================
# 3. PEMROSESAN DATA ALIRAN / FLOW (file3.xlsx)
# ==========================================
path3 = find_file('file3.xlsx')
df3 = pd.read_excel(path3)

# Memakai ffill untuk mengisi sel kosong (merged cells) di kolom Negara dan Tahun
df3['Negara'] = df3['Negara/Wilayah/Entitas Tertentu'].ffill()
df3['Tahun'] = df3['Tahun'].ffill()

df3_clean = df3.dropna(subset=['Totals', 'Kode HS']).copy()
df3_clean['HS_4Digit'] = 'HS ' + df3_clean['Kode HS'].str.extract(r'\[(\d{4})')
df3_clean['Deskripsi'] = df3_clean['Kode HS'].str.replace(r'\[\d+\]\s*', '', regex=True)

df3_clean.to_csv('data/cleaned/flow_clean.csv', index=False)
print(f"[OK] Flow Aliran: {df3_clean['Negara'].nunique()} Negara Mitra diproses dari '{path3}'.")

print("\n--- Pra-pemrosesan Data Selesai! File CSV bersih tersimpan di folder 'data/cleaned/' ---")