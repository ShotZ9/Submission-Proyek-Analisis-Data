import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚴‍♂️",
    layout="wide",
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('dashboard/main_data.csv')

data = load_data()

# Sidebar
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pilih Visualisasi")

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
    Dashboard ini menampilkan analisis tren penggunaan sepeda berdasarkan data yang tersedia.
    Pilih visualisasi di sidebar untuk melihat lebih detail.
""")

# Visualisasi 1: Tren Penggunaan Sepeda per Hari
if st.sidebar.checkbox("Tren Penggunaan Sepeda per Hari"):
    st.subheader("📈 Tren Penggunaan Sepeda per Hari")
    daily_data = data.groupby('dteday')['cnt_hour'].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='dteday', y='cnt_hour', data=daily_data)
    plt.title('Tren Penggunaan Sepeda per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(plt)
    st.markdown("""
        **Insight:**
        - Tren penggunaan sepeda cenderung meningkat selama periode tertentu.
        - Terlihat pola musiman dalam penggunaan sepeda.
    """)

# Visualisasi 2: Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur
if st.sidebar.checkbox("Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur"):
    st.subheader("📊 Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
    workingday_data = data.groupby('workingday_hour')['cnt_hour'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x='workingday_hour', y='cnt_hour', data=workingday_data)
    plt.title('Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur')
    plt.xlabel('Hari Libur (0) / Hari Kerja (1)')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    st.pyplot(plt)
    st.markdown("""
        **Insight:**
        - Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.
        - Hal ini menunjukkan bahwa sepeda banyak digunakan untuk keperluan komuter.
    """)

# Visualisasi 3: Distribusi Penggunaan Sepeda per Jam
if st.sidebar.checkbox("Distribusi Penggunaan Sepeda per Jam"):
    st.subheader("⏰ Distribusi Penggunaan Sepeda per Jam")
    hourly_data = data.groupby('hr')['cnt_hour'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt_hour', data=hourly_data)
    plt.title('Distribusi Penggunaan Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    st.pyplot(plt)
    st.markdown("""
        **Insight:**
        - Penggunaan sepeda meningkat pada jam sibuk (pagi dan sore).
        - Penggunaan terendah terjadi pada dini hari.
    """)

# Tampilkan data
if st.sidebar.checkbox("Tampilkan Data"):
    st.subheader("📋 Data Penggunaan Sepeda")
    st.write(data)
    st.markdown("""
        **Keterangan Kolom:**
        - `dteday`: Tanggal.
        - `hr`: Jam.
        - `cnt_hour`: Jumlah penyewaan sepeda per jam.
        - `workingday_hour`: Indikator hari kerja (1) atau hari libur (0).
    """)

# Footer
st.markdown("---")
st.markdown("""
    **Dashboard dibuat oleh:**  
    - Nama: Yoel Amadeo Pratomo  
    - Email: yamadeo9@gmail.com / mc006d5y2438@student.devacademy.id  
    - ID Dicoding: MC006D5Y2438  
""")