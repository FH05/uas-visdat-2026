import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ------------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN & CSS
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Dasbor Visdat BPS 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. SIDEBAR NAVIGATION & LOGO
# ------------------------------------------------------------------------------
col_l1, col_l2, col_l3 = st.sidebar.columns([1, 2, 1])
with col_l2:
    st.image("logo.PNG", use_container_width=True)

st.sidebar.title("Dasbor Ketahanan Kesehatan & Impor Farmasi")
st.sidebar.caption("Faizul Hanif | 3SD1 | 222313074 | UAS Visualisasi Data 2026")
st.sidebar.markdown("---")

st.sidebar.subheader("Pilih Topik Visualisasi")
topik = st.sidebar.radio(
    "Topik Data:",
    ["1. Multivariat Kesehatan (PCA)", "2. Data Aliran Impor", "3. Data Berhierarki"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Sumber Data Utama: **Badan Pusat Statistik (BPS)**")

# ------------------------------------------------------------------------------
# 3. LOAD DATASET FILE 1 (MULTIVARIAT CLEAN)
# ------------------------------------------------------------------------------
@st.cache_data
def load_multivariate_data():
    return pd.read_csv('data/cleaned/multivariat_clean.csv')

@st.cache_data
def load_flow_data():
    df = pd.read_csv('data/cleaned/flow_clean.csv')
    df['Totals'] = pd.to_numeric(df['Totals'], errors='coerce').fillna(0)
    # Bersihkan nama negara dari nilai kosong
    df['Negara'] = df['Negara'].astype(str).str.strip()
    df = df[df['Negara'] != 'nan']
    return df

@st.cache_data
def load_hierarki_data():
    df = pd.read_csv('data/cleaned/hierarki_clean.csv')
    df['nilai'] = pd.to_numeric(df['nilai'], errors='coerce').fillna(0)
    df['Persentase_Share'] = pd.to_numeric(df['Persentase_Share'], errors='coerce').fillna(0)
    return df

df_multi = load_multivariate_data()
df_flow = load_flow_data()
df_hierarki = load_hierarki_data()

# ------------------------------------------------------------------------------
# TOPIK 1: MULTIVARIAT KESEHATAN (3 TEKNIK SESUAI LAMPIRAN A UJIAN)
# ------------------------------------------------------------------------------
if topik == "1. Multivariat Kesehatan (PCA)":
    
    st.title("🏥 Pemetaan Ketahanan Kesehatan Provinsi di Indonesia")
    st.markdown("---")
    
    # A. PREPROCESSING & PCA
    kolom_prov = 'PROVINSI' if 'PROVINSI' in df_multi.columns else df_multi.columns[0]
    kolom_numerik = df_multi.select_dtypes(include=[np.number]).columns.tolist()
    
    X = df_multi[kolom_numerik].copy()
    
    # Standarisasi data (Z-Score Scaling)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA 2 Komponen
    pca = PCA(n_components=2)
    pca_res = pca.fit_transform(X_scaled)
    
    df_pca = df_multi.copy()
    df_pca['PC1'] = pca_res[:, 0]
    df_pca['PC2'] = pca_res[:, 1]
    
    var_pc1 = pca.explained_variance_ratio_[0] * 100
    var_pc2 = pca.explained_variance_ratio_[1] * 100

    # Dictionary Label Rapi untuk Variabel
    MAPPING_LABEL = {
        'AHH': 'AHH (Tahun)',
        'Morbiditas (persen)': 'Morbiditas (%)',
        'RT AirMinum Layak (Persen)': 'Air Minum Layak (%)',
        'RT Sanitasi Layak (Persen)': 'Sanitasi Layak (%)',
        'Penolong Persalinan TenagaKesehatan Terlatih (Persen)': 'Persalinan Nakes (%)',
        'Penduduk Memiliki JKN (Persen)': 'Peserta JKN (%)',
        'Rasio Faskes per100rbPenduduk': 'Rasio Faskes (/100rb)',
        'Anak Penerima ImunisasiDasarLengkap (Persen)': 'Imunisasi Lengkap (%)'
    }

    # ==========================================================================
    # TEKNIK 1: REDUKSI DIMENSI (PCA BIPLOT)
    # ==========================================================================
    st.subheader("1. Reduksi Dimensi: Pemetaan Komposit Provinsi (PCA Scatter Plot)")
    
    fig1 = px.scatter(
        df_pca,
        x='PC1',
        y='PC2',
        text=kolom_prov,
        color='PC1',
        color_continuous_scale='Viridis',
        hover_name=kolom_prov,
        hover_data=kolom_numerik,
        labels={
            'PC1': f'Komponen Utama 1 ({var_pc1:.1f}% Varians) [Satuan: Skor Z]',
            'PC2': f'Komponen Utama 2 ({var_pc2:.1f}% Varians) [Satuan: Skor Z]',
        },
        title="<b>Peta Sebaran 38 Provinsi Berdasarkan Komponen Utama (PC1 vs PC2)</b>"
    )

    fig1.update_traces(
        textposition='top center',
        marker=dict(size=11, line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate="<b>%{hovertext}</b><br><br>Skor PC1: %{x:.2f}<br>Skor PC2: %{y:.2f}<extra></extra>"
    )
    
    fig1.add_vline(x=0, line_dash="dash", line_color="#888888", opacity=0.6)
    fig1.add_hline(y=0, line_dash="dash", line_color="#888888", opacity=0.6)

    fig1.update_layout(
        height=500,
        margin=dict(l=30, r=30, t=50, b=30),
        plot_bgcolor='#F8F9FA',
        coloraxis_colorbar=dict(title="Skor PC1", ticks="outside")
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 1. Catatan Ringkas Langsung di Bawah Grafik
    st.caption(
        " Sumber: Badan Pusat Statistik (BPS) | Tahun Data: 2024 | *Detail 9"
        " Tabel BPS dapat dibuka pada menu metadata di bawah.*"
    )

    # 2. Expander Metadata Lengkap (Memenuhi Syarat 2b tanpa Merusak Tampilan Dasbor)
    with st.expander("📄 Detail Sumber Data & Metadata BPS"):
        st.markdown("""
        **Ketentuan Sumber Data Utama (BPS):**
        * **Penyedia Data:** Badan Pusat Statistik (BPS)
        * **Tanggal Akses Data:** 4 Oktober 2026
    
        | Indikator / Kolom | Judul Tabel / Publikasi Resmi BPS | Tahun | URL Sumber Data BPS |
        |---|---|---|---|
        | **AHH** | Angka Harapan Hidup (AHH) Menurut Provinsi dan Jenis Kelamin (Tahun), 2024 | 2024 | [Tautan BPS AHH](https://www.bps.go.id/id/statistics-table/2/NTAxIzI%3D/angka-harapan-hidup--ahh--menurut-provinsi-dan-jenis-kelamin) |
        | **Morbiditas** | Persentase Penduduk yang Mempunyai Keluhan Kesehatan dalam Sebulan Terakhir Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Morbiditas](https://www.bps.go.id/assets/statistics-table/2/MjIyIzI=/persentase-penduduk-yang-mempunyai-keluhan-kesehatan-dalam-sebulan-terakhir-menurut-provinsi.html) |
        | **Air Minum Layak** | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Air Minum](https://www.bps.go.id/id/statistics-table/2/ODQ1IzI=/persentase-rumah-tangga-yang-memiliki-akses-terhadap-sumber-air-minum-layak-menurut-provinsi--persen-.html) |
        | **Sanitasi Layak** | Persentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak (Persen), 2024 | 2024 | [Tautan BPS Sanitasi](https://www.bps.go.id/id/statistics-table/2/ODQ3IzI=/persentase-rumah-tangga-menurut-provinsi-dan-memiliki-akses-terhadap-sanitasi-layak.html) |
        | **Persalinan Nakes** | Persentase Perempuan Pernah Kawin Berumur 15-49 Tahun yang Melahirkan Anak Lahir Hidup (ALH) dalam 2 Tahun Terakhir menurut Provinsi dan Penolong Persalinan ALH yang Terakhir adalah Tenaga Kesehatan Terlatih (Persen), 2024 | 2024 | [Tautan BPS Nakes](https://www.bps.go.id/id/statistics-table/2/MTM0NSMy/persentase-perempuan-pernah-kawin-berumur-15-49-tahun-yang-melahirkan-anak-lahir-hidup--alh--dalam-2-tahun-terakhir-menurut-provinsi-dan-penolong-persalinan-alh-yang-terakhir-adalah-tenaga-kesehatan-terlatih--persen-.html) |
        | **Peserta JKN** | Persentase Penduduk yang Memiliki Jaminan Kesehatan Nasional (JKN) Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS JKN](https://www.bps.go.id/id/statistics-table/2/MjI3OSMy/persentase%20penduduk-yang-memiliki-jaminan-kesehatan-nasional--jkn--menurut-provinsi.html) |
        | **Rasio Faskes** | Jumlah Rumah Sakit Umum, Rumah Sakit Khusus, Puskesmas Rawat Inap, dan Puskesmas Non Rawat Inap Menurut Provinsi, 2025 & Jumlah Penduduk menurut Provinsi dan Jenis Kelamin, 2025 | 2024 | [Tautan BPS Faskes](https://www.bps.go.id/id/statistics-table/3/YmlzemNGUkNVblZLVVhOblREWnZXbkEzWld0eVVUMDkjMyMwMDAw/jumlah-rumah-sakit-umum--rumah-sakit-khusus--puskesmas--klinik-pratama--dan-posyandu-menurut-provinsi.html?year=2025)&[Tautan BPS Jumlah penduduk](https://www.bps.go.id/id/statistics-table/2/Mjc4MSMy/jumlah-penduduk-menurut-provinsi-dan-jenis-kelamin.html) |
        | **Imunisasi Lengkap** | Persentase Anak Umur 12-23 Bulan yang Menerima Imunisasi Dasar Lengkap Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Imunisasi](https://www.bps.go.id/id/statistics-table/2/MjI4MCMy/persentase-anak-umur-12-23-bulan-yang-menerima-imunisasi-dasar-lengkap-menurut-provinsi--persen-.html) |
        """)

    c1_1, c1_2 = st.columns(2)
    with c1_1:
        st.caption("📌 **Encoding Visual & Satuan:** Sumbu X & Y merepresentasikan Skor Z terstandardisasi dari PCA. Warna titik mewakili tingkatan kelayakan komposit (Skala Viridis).")
    with c1_2:
        st.caption(f"ℹ️ Total varians dijelaskan oleh PC1 & PC2: **{(var_pc1 + var_pc2):.1f}%**.")

    st.markdown("---")

    # ==========================================================================
    # TEKNIK 2: PARALLEL COORDINATES PLOT
    # ==========================================================================
    st.subheader("2. Profil Multi-Indikator Kesehatan & Sanitasi per Provinsi")
    
    # KUSUS NAMA VARIABEL: PEMETAAN SINGKATAN RAPI DAN TERSUSUN KE BAWAH (<br>)
    # Ini mencegah teks saling berbenturan di bagian atas sumbu
    MAPPING_LABEL = {
        'AHH': 'AHH<br>(Tahun)',
        'Morbiditas (persen)': 'Morbiditas<br>(%)',
        'RT AirMinum Layak (Persen)': 'Air Minum<br>Layak (%)',
        'RT Sanitasi Layak (Persen)': 'Sanitasi<br>Layak (%)',
        'Penolong Persalinan TenagaKesehatan Terlatih (Persen)': 'Persalinan<br>Nakes (%)',
        'Penduduk Memiliki JKN (Persen)': 'Peserta<br>JKN (%)',
        'Rasio Faskes per100rbPenduduk': 'Rasio Faskes<br>(/100rb)',
        'Anak Penerima ImunisasiDasarLengkap (Persen)': 'Imunisasi<br>Lengkap (%)'
    }

    dimensions_list = []
    
    for col in kolom_numerik:
        min_val = float(df_pca[col].min())
        max_val = float(df_pca[col].max())
        
        # Ambil label rapi dari mapping, jika tidak ada baru otomatis dibuat 2 baris
        if col in MAPPING_LABEL:
            label_clean = MAPPING_LABEL[col]
        else:
            words = col.replace('_', ' ').split()
            label_clean = f"{' '.join(words[:2])}<br>{' '.join(words[2:])}" if len(words) > 2 else col

        dimensions_list.append(
            dict(
                range=[min_val, max_val],
                label=label_clean,
                values=df_pca[col],
                tickvals=[min_val, max_val], # Hanya angka Min & Max di ujung sumbu
                tickformat='.1f'
            )
        )

    # Dibuat 1 Warna Netral (Hijau Sehat) Persis Slide 13 Materi
    fig2 = go.Figure(data=
        go.Parcoords(
            line=dict(
                color='#2E7D32', # Warna hijau netral khas visualisasi BPS/materi
            ),
            labelfont=dict(size=11, color='#111111'),
            tickfont=dict(size=10, color='#444444'),
            dimensions=dimensions_list
        )
    )

    fig2.update_layout(
        title="<b>Perbandingan Nilai Indikator Kesehatan Antar-Provinsi (Parallel Coordinates)</b>",
        height=500,
        margin=dict(l=50, r=50, t=110, b=30), # Margin t=110 memberi ruang luas bagi label 2 baris
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 1. Catatan Ringkas Langsung di Bawah Grafik
    st.caption(
            " Sumber: Badan Pusat Statistik (BPS) | Tahun Data: 2024 | *Detail 9"
            " Tabel BPS dapat dibuka pada menu metadata di bawah.*"
        )
    
        # 2. Expander Metadata Lengkap (Memenuhi Syarat 2b tanpa Merusak Tampilan Dasbor)
    with st.expander("📄 Detail Sumber Data & Metadata BPS"):
            st.markdown("""
            **Ketentuan Sumber Data Utama (BPS):**
            * **Penyedia Data:** Badan Pusat Statistik (BPS)
            * **Tanggal Akses Data:** 4 Oktober 2026
        
            | Indikator / Kolom | Judul Tabel / Publikasi Resmi BPS | Tahun | URL Sumber Data BPS |
            |---|---|---|---|
            | **AHH** | Angka Harapan Hidup (AHH) Menurut Provinsi dan Jenis Kelamin (Tahun), 2024 | 2024 | [Tautan BPS AHH](https://www.bps.go.id/id/statistics-table/2/NTAxIzI%3D/angka-harapan-hidup--ahh--menurut-provinsi-dan-jenis-kelamin) |
            | **Morbiditas** | Persentase Penduduk yang Mempunyai Keluhan Kesehatan dalam Sebulan Terakhir Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Morbiditas](https://www.bps.go.id/assets/statistics-table/2/MjIyIzI=/persentase-penduduk-yang-mempunyai-keluhan-kesehatan-dalam-sebulan-terakhir-menurut-provinsi.html) |
            | **Air Minum Layak** | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Air Minum](https://www.bps.go.id/id/statistics-table/2/ODQ1IzI=/persentase-rumah-tangga-yang-memiliki-akses-terhadap-sumber-air-minum-layak-menurut-provinsi--persen-.html) |
            | **Sanitasi Layak** | Persentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak (Persen), 2024 | 2024 | [Tautan BPS Sanitasi](https://www.bps.go.id/id/statistics-table/2/ODQ3IzI=/persentase-rumah-tangga-menurut-provinsi-dan-memiliki-akses-terhadap-sanitasi-layak.html) |
            | **Persalinan Nakes** | Persentase Perempuan Pernah Kawin Berumur 15-49 Tahun yang Melahirkan Anak Lahir Hidup (ALH) dalam 2 Tahun Terakhir menurut Provinsi dan Penolong Persalinan ALH yang Terakhir adalah Tenaga Kesehatan Terlatih (Persen), 2024 | 2024 | [Tautan BPS Nakes](https://www.bps.go.id/id/statistics-table/2/MTM0NSMy/persentase-perempuan-pernah-kawin-berumur-15-49-tahun-yang-melahirkan-anak-lahir-hidup--alh--dalam-2-tahun-terakhir-menurut-provinsi-dan-penolong-persalinan-alh-yang-terakhir-adalah-tenaga-kesehatan-terlatih--persen-.html) |
            | **Peserta JKN** | Persentase Penduduk yang Memiliki Jaminan Kesehatan Nasional (JKN) Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS JKN](https://www.bps.go.id/id/statistics-table/2/MjI3OSMy/persentase%20penduduk-yang-memiliki-jaminan-kesehatan-nasional--jkn--menurut-provinsi.html) |
            | **Rasio Faskes** | Jumlah Rumah Sakit Umum, Rumah Sakit Khusus, Puskesmas Rawat Inap, dan Puskesmas Non Rawat Inap Menurut Provinsi, 2025 & Jumlah Penduduk menurut Provinsi dan Jenis Kelamin, 2025 | 2024 | [Tautan BPS Faskes](https://www.bps.go.id/id/statistics-table/3/YmlzemNGUkNVblZLVVhOblREWnZXbkEzWld0eVVUMDkjMyMwMDAw/jumlah-rumah-sakit-umum--rumah-sakit-khusus--puskesmas--klinik-pratama--dan-posyandu-menurut-provinsi.html?year=2025)&[Tautan BPS Jumlah penduduk](https://www.bps.go.id/id/statistics-table/2/Mjc4MSMy/jumlah-penduduk-menurut-provinsi-dan-jenis-kelamin.html) |
            | **Imunisasi Lengkap** | Persentase Anak Umur 12-23 Bulan yang Menerima Imunisasi Dasar Lengkap Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Imunisasi](https://www.bps.go.id/id/statistics-table/2/MjI4MCMy/persentase-anak-umur-12-23-bulan-yang-menerima-imunisasi-dasar-lengkap-menurut-provinsi--persen-.html) |
            """)

    # Keterangan Grafik 2
    c2_1, c2_2 = st.columns(2)
    with c2_1:
        st.caption("📌 **Encoding Visual & Satuan:** Garis tegak menunjukkan sumbu indikator dengan nilai Minimum (bawah) dan Maksimum (atas). Garis horizontal menghubungkan indikator milik 1 provinsi[cite: 19].")
    with c2_2:
        st.caption("ℹ️ **Fitur Interaktif (Brushing):** Klik dan drag kursor pada sumbu vertikal manapun untuk menyeleksi (*brushing*) kelompok provinsi tertentu.")

    # ==========================================================================
    # TEKNIK 3: HEATMAP TERKLASTER (STANDARDIZED HEATMAP MATRIX)
    # ==========================================================================
    st.subheader("3. Matriks Profil Indikator: Standardized Heatmap Matrix")
    
    # Menyiapkan DataFrame terstandarisasi untuk Heatmap
    df_heatmap = pd.DataFrame(X_scaled, columns=[MAPPING_LABEL.get(c, c) for c in kolom_numerik])
    df_heatmap.index = df_multi[kolom_prov]

    fig3 = px.imshow(
        df_heatmap.T, # Transpose agar variabel di sumbu Y, provinsi di sumbu X
        labels=dict(x="Provinsi", y="Indikator Kesehatan", color="Skor Z (Standardized)"),
        x=df_heatmap.index,
        y=df_heatmap.columns,
        color_continuous_scale='Viridis',
        aspect="auto",
        title="<b>Matriks Skor Terstandardisasi Indikator Kesehatan per Provinsi</b>"
    )

    fig3.update_layout(
        height=480,
        margin=dict(l=50, r=30, t=60, b=80),
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=10)),
        coloraxis_colorbar=dict(title="Skor Z", ticks="outside")
    )

    st.plotly_chart(fig3, use_container_width=True)

    # 1. Catatan Ringkas Langsung di Bawah Grafik
    st.caption(
        " Sumber: Badan Pusat Statistik (BPS) | Tahun Data: 2024 | *Detail 9"
        " Tabel BPS dapat dibuka pada menu metadata di bawah.*"
    )

    # 2. Expander Metadata Lengkap (Memenuhi Syarat 2b tanpa Merusak Tampilan Dasbor)
    with st.expander("📄 Detail Sumber Data & Metadata BPS"):
        st.markdown("""
        **Ketentuan Sumber Data Utama (BPS):**
        * **Penyedia Data:** Badan Pusat Statistik (BPS)
        * **Tanggal Akses Data:** 4 Oktober 2026
    
        | Indikator / Kolom | Judul Tabel / Publikasi Resmi BPS | Tahun | URL Sumber Data BPS |
        |---|---|---|---|
        | **AHH** | Angka Harapan Hidup (AHH) Menurut Provinsi dan Jenis Kelamin (Tahun), 2024 | 2024 | [Tautan BPS AHH](https://www.bps.go.id/id/statistics-table/2/NTAxIzI%3D/angka-harapan-hidup--ahh--menurut-provinsi-dan-jenis-kelamin) |
        | **Morbiditas** | Persentase Penduduk yang Mempunyai Keluhan Kesehatan dalam Sebulan Terakhir Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Morbiditas](https://www.bps.go.id/assets/statistics-table/2/MjIyIzI=/persentase-penduduk-yang-mempunyai-keluhan-kesehatan-dalam-sebulan-terakhir-menurut-provinsi.html) |
        | **Air Minum Layak** | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Air Minum](https://www.bps.go.id/id/statistics-table/2/ODQ1IzI=/persentase-rumah-tangga-yang-memiliki-akses-terhadap-sumber-air-minum-layak-menurut-provinsi--persen-.html) |
        | **Sanitasi Layak** | Persentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak (Persen), 2024 | 2024 | [Tautan BPS Sanitasi](https://www.bps.go.id/id/statistics-table/2/ODQ3IzI=/persentase-rumah-tangga-menurut-provinsi-dan-memiliki-akses-terhadap-sanitasi-layak.html) |
        | **Persalinan Nakes** | Persentase Perempuan Pernah Kawin Berumur 15-49 Tahun yang Melahirkan Anak Lahir Hidup (ALH) dalam 2 Tahun Terakhir menurut Provinsi dan Penolong Persalinan ALH yang Terakhir adalah Tenaga Kesehatan Terlatih (Persen), 2024 | 2024 | [Tautan BPS Nakes](https://www.bps.go.id/id/statistics-table/2/MTM0NSMy/persentase-perempuan-pernah-kawin-berumur-15-49-tahun-yang-melahirkan-anak-lahir-hidup--alh--dalam-2-tahun-terakhir-menurut-provinsi-dan-penolong-persalinan-alh-yang-terakhir-adalah-tenaga-kesehatan-terlatih--persen-.html) |
        | **Peserta JKN** | Persentase Penduduk yang Memiliki Jaminan Kesehatan Nasional (JKN) Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS JKN](https://www.bps.go.id/id/statistics-table/2/MjI3OSMy/persentase%20penduduk-yang-memiliki-jaminan-kesehatan-nasional--jkn--menurut-provinsi.html) |
        | **Rasio Faskes** | Jumlah Rumah Sakit Umum, Rumah Sakit Khusus, Puskesmas Rawat Inap, dan Puskesmas Non Rawat Inap Menurut Provinsi, 2025 & Jumlah Penduduk menurut Provinsi dan Jenis Kelamin, 2025 | 2024 | [Tautan BPS Faskes](https://www.bps.go.id/id/statistics-table/3/YmlzemNGUkNVblZLVVhOblREWnZXbkEzWld0eVVUMDkjMyMwMDAw/jumlah-rumah-sakit-umum--rumah-sakit-khusus--puskesmas--klinik-pratama--dan-posyandu-menurut-provinsi.html?year=2025)&[Tautan BPS Jumlah penduduk](https://www.bps.go.id/id/statistics-table/2/Mjc4MSMy/jumlah-penduduk-menurut-provinsi-dan-jenis-kelamin.html) |
        | **Imunisasi Lengkap** | Persentase Anak Umur 12-23 Bulan yang Menerima Imunisasi Dasar Lengkap Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Imunisasi](https://www.bps.go.id/id/statistics-table/2/MjI4MCMy/persentase-anak-umur-12-23-bulan-yang-menerima-imunisasi-dasar-lengkap-menurut-provinsi--persen-.html) |
        """)
    c3_1, c3_2 = st.columns(2)
    with c3_1:
        st.caption("📌 **Encoding Visual & Satuan:** Warna blok merepresentasikan nilai Z-score terstandardisasi (Satuan: Standar Deviasi dari Rata-rata Nasional). Warna kuning/terang = di atas rata-rata, warna ungu/gelap = di bawah rata-rata.")
    with c3_2:
        st.caption("ℹ️ **Interaksi:** Hover kursor ke kotak matriks untuk melihat detail provinsi, nama indikator, dan nilai Z-score.")

    # ==========================================================================
    # TEKNIK 3: HEATMAP KORELASI (8 VARIABEL VS 8 VARIABEL)
    # ==========================================================================
    st.subheader("4. Hubungan Antar-Indikator: Matriks Korelasi (Heatmap)")
    
    # Hitung matriks korelasi Pearson antar 8 variabel
    df_corr = df_multi[kolom_numerik].corr()
    
    # Ubah nama kolom/indeks dengan label yang rapi
    labels_clean = [MAPPING_LABEL.get(c, c) for c in df_corr.columns]
    df_corr.columns = labels_clean
    df_corr.index = labels_clean

    fig3 = px.imshow(
        df_corr,
        text_auto=".2f", # Menampilkan angka korelasi di dalam kotak
        labels=dict(color="Koefisien Korelasi"),
        color_continuous_scale='RdBu_r', # Scale biru (positif) ke merah (negatif)
        zmin=-1, zmax=1,
        title="<b>Matriks Korelasi Pearson Antar-Indikator Kesehatan</b>"
    )

    fig3.update_layout(
        height=500,
        margin=dict(l=50, r=30, t=60, b=80),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10))
    )

    st.plotly_chart(fig3, use_container_width=True)

    # 1. Catatan Ringkas Langsung di Bawah Grafik
    st.caption(
        " Sumber: Badan Pusat Statistik (BPS) | Tahun Data: 2024 | *Detail 9"
        " Tabel BPS dapat dibuka pada menu metadata di bawah.*"
    )

    # 2. Expander Metadata Lengkap (Memenuhi Syarat 2b tanpa Merusak Tampilan Dasbor)
    with st.expander("📄 Detail Sumber Data & Metadata BPS"):
        st.markdown("""
        **Ketentuan Sumber Data Utama (BPS):**
        * **Penyedia Data:** Badan Pusat Statistik (BPS)
        * **Tanggal Akses Data:** 4 Oktober 2026
    
        | Indikator / Kolom | Judul Tabel / Publikasi Resmi BPS | Tahun | URL Sumber Data BPS |
        |---|---|---|---|
        | **AHH** | Angka Harapan Hidup (AHH) Menurut Provinsi dan Jenis Kelamin (Tahun), 2024 | 2024 | [Tautan BPS AHH](https://www.bps.go.id/id/statistics-table/2/NTAxIzI%3D/angka-harapan-hidup--ahh--menurut-provinsi-dan-jenis-kelamin) |
        | **Morbiditas** | Persentase Penduduk yang Mempunyai Keluhan Kesehatan dalam Sebulan Terakhir Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Morbiditas](https://www.bps.go.id/assets/statistics-table/2/MjIyIzI=/persentase-penduduk-yang-mempunyai-keluhan-kesehatan-dalam-sebulan-terakhir-menurut-provinsi.html) |
        | **Air Minum Layak** | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Air Minum](https://www.bps.go.id/id/statistics-table/2/ODQ1IzI=/persentase-rumah-tangga-yang-memiliki-akses-terhadap-sumber-air-minum-layak-menurut-provinsi--persen-.html) |
        | **Sanitasi Layak** | Persentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak (Persen), 2024 | 2024 | [Tautan BPS Sanitasi](https://www.bps.go.id/id/statistics-table/2/ODQ3IzI=/persentase-rumah-tangga-menurut-provinsi-dan-memiliki-akses-terhadap-sanitasi-layak.html) |
        | **Persalinan Nakes** | Persentase Perempuan Pernah Kawin Berumur 15-49 Tahun yang Melahirkan Anak Lahir Hidup (ALH) dalam 2 Tahun Terakhir menurut Provinsi dan Penolong Persalinan ALH yang Terakhir adalah Tenaga Kesehatan Terlatih (Persen), 2024 | 2024 | [Tautan BPS Nakes](https://www.bps.go.id/id/statistics-table/2/MTM0NSMy/persentase-perempuan-pernah-kawin-berumur-15-49-tahun-yang-melahirkan-anak-lahir-hidup--alh--dalam-2-tahun-terakhir-menurut-provinsi-dan-penolong-persalinan-alh-yang-terakhir-adalah-tenaga-kesehatan-terlatih--persen-.html) |
        | **Peserta JKN** | Persentase Penduduk yang Memiliki Jaminan Kesehatan Nasional (JKN) Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS JKN](https://www.bps.go.id/id/statistics-table/2/MjI3OSMy/persentase%20penduduk-yang-memiliki-jaminan-kesehatan-nasional--jkn--menurut-provinsi.html) |
        | **Rasio Faskes** | Jumlah Rumah Sakit Umum, Rumah Sakit Khusus, Puskesmas Rawat Inap, dan Puskesmas Non Rawat Inap Menurut Provinsi, 2025 & Jumlah Penduduk menurut Provinsi dan Jenis Kelamin, 2025 | 2024 | [Tautan BPS Faskes](https://www.bps.go.id/id/statistics-table/3/YmlzemNGUkNVblZLVVhOblREWnZXbkEzWld0eVVUMDkjMyMwMDAw/jumlah-rumah-sakit-umum--rumah-sakit-khusus--puskesmas--klinik-pratama--dan-posyandu-menurut-provinsi.html?year=2025)&[Tautan BPS Jumlah penduduk](https://www.bps.go.id/id/statistics-table/2/Mjc4MSMy/jumlah-penduduk-menurut-provinsi-dan-jenis-kelamin.html) |
        | **Imunisasi Lengkap** | Persentase Anak Umur 12-23 Bulan yang Menerima Imunisasi Dasar Lengkap Menurut Provinsi (Persen), 2024 | 2024 | [Tautan BPS Imunisasi](https://www.bps.go.id/id/statistics-table/2/MjI4MCMy/persentase-anak-umur-12-23-bulan-yang-menerima-imunisasi-dasar-lengkap-menurut-provinsi--persen-.html) |
        """)
    c3_1, c3_2 = st.columns(2)
    with c3_1:
        st.caption("📌 **Encoding Visual:** Warna mengindikasikan kekuatan korelasi (Biru = Korelasi Positif, Merah = Korelasi Negatif). Angka di dalam kotak adalah nilai r-Pearson (-1 hingga +1).")
    with c3_2:
        st.caption("ℹ️ **Interaksi:** Hover kursor pada kotak matriks untuk melihat detail pasangan variabel dan nilai korelasinya.")

# ------------------------------------------------------------------------------
# TOPIK 2: DATA ALIRAN / PERGERAKAN (FLOW DATA)
# ------------------------------------------------------------------------------
elif topik == "2. Data Aliran Impor":
    
    st.title("🚢 Visualisasi Aliran Impor Produk Farmasi Menurut Negara Mitra")
    st.markdown("---")
    
    # Sidebar Filters (Memenuhi Ketentuan: Filter Asal / Tujuan)
    st.sidebar.subheader("🎛️ Filter Aliran Impor")
    
    top_n = st.sidebar.slider("Tampilkan Top-N Negara Asal (Berdasarkan Total Impor):", min_value=5, max_value=30, value=15)
    
    # Hitung Top Negara Asal
    top_countries = df_flow.groupby('Negara')['Totals'].sum().nlargest(top_n).index.tolist()
    
    selected_countries = st.sidebar.multiselect(
        "Pilih Negara Asal (Mitra Dagang):",
        options=sorted(df_flow['Negara'].unique().tolist()),
        default=top_countries
    )
    
    # Filter Dataframe
    df_filtered_flow = df_flow[df_flow['Negara'].isin(selected_countries)].copy()
    
    # Grouping Data untuk Visualisasi Aliran (Negara -> HS_4Digit)
    flow_grouped = df_filtered_flow.groupby(['Negara', 'HS_4Digit'])['Totals'].sum().reset_index()
    flow_grouped = flow_grouped[flow_grouped['Totals'] > 0]

    # ==========================================================================
    # TEKNIK 1: SANKEY DIAGRAM (FLOW VOLUME & DIRECTION ENCODING)
    # ==========================================================================
    st.subheader("1. Teknik 1: Diagram Sankey (Aliran Perdagangan Negara Asal ➔ Kategori HS)")
    
    if len(flow_grouped) > 0:
        # Menyiapkan Label Unik Node (Source + Target)
        sources = flow_grouped['Negara'].unique().tolist()
        targets = flow_grouped['HS_4Digit'].unique().tolist()
        all_nodes = sources + targets
        
        node_map = {node: i for i, node in enumerate(all_nodes)}
        
        # Mapping Source, Target, & Value ke Index
        source_indices = flow_grouped['Negara'].map(node_map).tolist()
        target_indices = flow_grouped['HS_4Digit'].map(node_map).tolist()
        values = flow_grouped['Totals'].tolist()
        
        # Warna Node
        source_colors = ['#1f77b4'] * len(sources)
        target_colors = ['#2ca02c'] * len(targets)
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=source_colors + target_colors
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values,
                color="rgba(180, 180, 180, 0.4)" # Ketebalan pita mewakili volume aliran
            )
        )])
        
        fig_sankey.update_layout(
            title=f"<b>Diagram Aliran Sankey (Total Aliran dari {len(sources)} Negara Mitra)</b>",
            font_size=11,
            height=600,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        st.plotly_chart(fig_sankey, use_container_width=True)

        # 1. Catatan Ringkas Langsung di Bawah Grafik
        st.caption(
                " Sumber: Badan Pusat Statistik (BPS) | Data Ekspor Impor Nasional | Tahun Data: 2024 | [Tautan BPS ekspor-impor](https://www.bps.go.id/id/exim)"
            )
        
        c_sk1, c_sk2 = st.columns(2)
        with c_sk1:
            st.caption("📌 **Encoding Visual:** **Ketebalan Pita (Link Width)** mengkodekan *Volume/Nilai Impor (USD)*. **Sisi Kiri:** Negara Asal | **Sisi Kanan:** Pos Tarif HS 4-Digit.")
        with c_sk2:
            st.caption("ℹ️ **Interaksi Filter:** Gunakan multiselect di sidebar untuk memilih negara mitra spesifik atau ubah slider Top-N.")
    else:
        st.warning("Tidak ada data aliran impor untuk filter negara yang dipilih.")

    st.markdown("---")

    # ==========================================================================
    # TEKNIK 2: MATRIKS OD / ORIGIN-DESTINATION HEATMAP
    # ==========================================================================
    st.subheader("2. Teknik 2: Matriks OD (Origin-Destination Heatmap)")
    
    # Pivot Table untuk Matriks OD
    od_matrix = flow_grouped.pivot_table(index='Negara', columns='HS_4Digit', values='Totals', fill_value=0)
    
    fig_od = px.imshow(
        od_matrix,
        labels=dict(x="Tujuan (Pos HS 4-Digit)", y="Asal (Negara Mitra)", color="Nilai Impor (USD)"),
        color_continuous_scale='YlGnBu',
        aspect="auto",
        title="<b>Matriks Intensitas Perdagangan Aliran Impor (Origin vs Destination)</b>"
    )
    
    fig_od.update_layout(
        height=550,
        margin=dict(l=50, r=30, t=60, b=80),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        coloraxis_colorbar=dict(title="Nilai (USD)", ticks="outside")
    )
    
    st.plotly_chart(fig_od, use_container_width=True)

    st.caption(
        " Sumber: Badan Pusat Statistik (BPS) | Data Ekspor Impor Nasional | Tahun Data: 2024 | [Tautan BPS ekspor-impor](https://www.bps.go.id/id/exim)"
    )

    c_od1, c_od2 = st.columns(2)
    with c_od1:
        st.caption("📌 **Encoding Visual:** Intensitas warna mengkodekan besarnya nilai impor dari Negara Asal ke Pos Komoditas HS tertentu.")
    with c_od2:
        st.caption("ℹ️ **Keunggulan:** Menyajikan matriks konsentrasi impor secara komprehensif tanpa bahaya overlapping visual.")

# ------------------------------------------------------------------------------
# TOPIK 3: DATA BERHIERARKI (TREEMAP & SUNBURST WITH DRILL-DOWN)
# ------------------------------------------------------------------------------
elif topik == "3. Data Berhierarki":
    
    st.title("📦 Struktur Hirarki Komoditas Impor Produk Farmasi (HS Code)")
    st.markdown("---")
    
    # Menentukan 3 Level Hirarki yang Tersedia
    path_hirarki = ['Level_1', 'HS_4Digit', 'Deskripsi']
    
    # ==========================================================================
    # REPRESENTASI 1: TREEMAP CHART (WITH BREADCRUMB & DRILL-DOWN)
    # ==========================================================================
    st.subheader("1. Representasi 1: Treemap Diagram (Proporsi & Hirarki Komoditas)")
    
    fig_tree = px.treemap(
        df_hierarki,
        path=path_hirarki,
        values='nilai',
        color='Persentase_Share',
        color_continuous_scale='Blues',
        hover_data=['Kode_8Digit', 'nilai', 'Persentase_Share'],
        title="<b>Struktur Impor Farmasi: Level 1 (HS 2-Digit) ➔ Level 2 (HS 4-Digit) ➔ Level 3 (Deskripsi 8-Digit)</b>"
    )
    
    fig_tree.update_traces(
        hovertemplate="<b>%{label}</b><br>Nilai Impor: USD %{value:,.0f}<br>Pangsa Pasar (Share): %{color:.2f}%<extra></extra>",
        marker=dict(cornerradius=3)
    )
    
    fig_tree.update_layout(
        height=550,
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(title="Pangsa Share (%)", ticks="outside")
    )
    
    st.plotly_chart(fig_tree, use_container_width=True)

    st.caption(
                    " Sumber: Badan Pusat Statistik (BPS) | Data Ekspor Impor Nasional | Tahun Data: 2024 | [Tautan BPS ekspor-impor](https://www.bps.go.id/id/exim)"
                )
    
    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.caption("📌 **Encoding Visual:** **Luas Kotak** mengkodekan *Nilai Impor (USD)*. **Warna Kotak** mengkodekan *Pangsa Share (%)*.")
    with c_t2:
        st.caption("ℹ️ **Interaksi Drill-Down:** Klik pada kotak manapun untuk masuk/zoom ke hirarki di bawahnya (*drill-down*). Klik *breadcrumb* di bagian atas grafik untuk kembali.")

    st.markdown("---")

    # ==========================================================================
    # REPRESENTASI 2: SUNBURST CHART (INTERACTIVE RADIAL DRILL-DOWN)
    # ==========================================================================
    st.subheader("2. Representasi 2: Sunburst Diagram (Radial Hierarchical Structure)")
    
    fig_sun = px.sunburst(
        df_hierarki,
        path=path_hirarki,
        values='nilai',
        color='Persentase_Share',
        color_continuous_scale='Viridis',
        hover_data=['Kode_8Digit', 'nilai', 'Persentase_Share'],
        title="<b>Visualisasi Struktur Radial Komoditas Impor Farmasi</b>"
    )
    
    fig_sun.update_traces(
        hovertemplate="<b>%{label}</b><br>Nilai Impor: USD %{value:,.0f}<br>Pangsa Pasar (Share): %{color:.2f}%<extra></extra>"
    )
    
    fig_sun.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(title="Pangsa Share (%)", ticks="outside")
    )
    
    st.plotly_chart(fig_sun, use_container_width=True)

    st.caption(
                    " Sumber: Badan Pusat Statistik (BPS) | Data Ekspor Impor Nasional | Tahun Data: 2024 | [Tautan BPS ekspor-impor](https://www.bps.go.id/id/exim)"
                )
    
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.caption("📌 **Encoding Visual:** **Sudut/Ukuran Busur Radial** mengkodekan *Nilai Impor (USD)*. **Warna Ring** mengkodekan *Pangsa Share (%)*.")
    with c_s2:
        st.caption("ℹ️ **Interaksi Drill-Down:** Klik sektor lingkaran untuk fokus pada kategori tersebut. Klik lingkaran tengah untuk kembali ke level sebelumnya.")
