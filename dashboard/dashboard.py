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
    data = pd.read_csv('dashboard/main_data.csv')
    # Ubah kolom 'dteday' ke format datetime
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

data = load_data()

# Sidebar untuk filtering
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Filter Data")

# Filter berdasarkan tanggal
min_date = data['dteday'].min()
max_date = data['dteday'].max()
start_date = st.sidebar.date_input("Tanggal Mulai", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

# Filter berdasarkan musim (season)
season_options = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
selected_season = st.sidebar.selectbox("Pilih Musim", options=list(season_options.keys()), format_func=lambda x: season_options[x])

# Filter data berdasarkan tanggal dan musim
filtered_data = data[
    (data['dteday'] >= pd.to_datetime(start_date)) &
    (data['dteday'] <= pd.to_datetime(end_date)) &
    (data['season'] == selected_season)
]

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
    Dashboard ini menampilkan analisis tren penggunaan sepeda berdasarkan data yang tersedia.
    Gunakan filter di sidebar untuk menyesuaikan data yang ditampilkan.
""")

# Visualisasi 1: Tren Penggunaan Sepeda per Hari
st.subheader("📈 Tren Penggunaan Sepeda per Hari")
daily_data = filtered_data.groupby('dteday')['cnt_hour'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x='dteday', y='cnt_hour', data=daily_data, color='blue', linewidth=2.5, ax=ax)
ax.set_title('Tren Penggunaan Sepeda per Hari', fontsize=14)
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig, clear_figure=True)
st.markdown("""
    **Insight:**
    - Tren penggunaan sepeda cenderung meningkat selama periode tertentu.
    - Terlihat pola musiman dalam penggunaan sepeda.
""")

# Visualisasi 2: Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur
st.subheader("📊 Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
workingday_data = filtered_data.groupby('workingday_hour')['cnt_hour'].mean().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x='workingday_hour', y='cnt_hour', data=workingday_data, palette='viridis', ax=ax)
ax.set_title('Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur', fontsize=14)
ax.set_xlabel('Hari Libur (0) / Hari Kerja (1)', fontsize=12)
ax.set_ylabel('Rata-rata Penggunaan Sepeda', fontsize=12)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Hari Libur', 'Hari Kerja'], fontsize=12)
plt.tight_layout()
st.pyplot(fig, clear_figure=True)
st.markdown("""
    **Insight:**
    - Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.
    - Hal ini menunjukkan bahwa sepeda banyak digunakan untuk keperluan komuter.
""")

# Visualisasi 3: Distribusi Penggunaan Sepeda per Jam
st.subheader("⏰ Distribusi Penggunaan Sepeda per Jam")
hourly_data = filtered_data.groupby('hr')['cnt_hour'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x='hr', y='cnt_hour', data=hourly_data, color='green', linewidth=2.5, ax=ax)
ax.set_title('Distribusi Penggunaan Sepeda per Jam', fontsize=14)
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Rata-rata Penggunaan Sepeda', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig, clear_figure=True)
st.markdown("""
    **Insight:**
    - Penggunaan sepeda meningkat pada jam sibuk (pagi dan sore).
    - Penggunaan terendah terjadi pada dini hari.
""")

# Tampilkan data
if st.checkbox("Tampilkan Data yang Difilter"):
    st.subheader("📋 Data Penggunaan Sepeda yang Difilter")
    st.write(filtered_data)
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