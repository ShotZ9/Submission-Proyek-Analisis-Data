import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚴‍♂️",
    layout="wide",
)

@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/main_data.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

data = load_data()

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

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Reset Filter"):
        st.session_state.filtered = False
with col2:
    if st.button("Terapkan Filter"):
        st.session_state.filtered = True

# Inisialisasi session state untuk status filter
if 'filtered' not in st.session_state:
    st.session_state.filtered = False

if st.session_state.filtered:
    filtered_data = data[
        (data['dteday'] >= pd.to_datetime(start_date)) &
        (data['dteday'] <= pd.to_datetime(end_date)) &
        (data['season_hour'] == selected_season)
    ]
else:
    filtered_data = data

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
    Dashboard ini menampilkan analisis tren penggunaan sepeda berdasarkan data yang tersedia.
    Gunakan filter di sidebar untuk menyesuaikan data yang ditampilkan.
""")

# Visualisasi 1
st.subheader("📈 Tren Penggunaan Sepeda per Hari")
daily_data = filtered_data.groupby('dteday')['cnt_hour'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x='dteday', y='cnt_hour', data=daily_data, color='blue', linewidth=2.5, ax=ax)
ax.set_title('Tren Penggunaan Sepeda per Hari', fontsize=14)
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig, clear_figure=True)

# Visualisasi 2
st.subheader("📊 Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
workingday_data = filtered_data.groupby('workingday_hour')['cnt_hour'].mean().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x='workingday_hour', y='cnt_hour', data=workingday_data, palette='viridis', ax=ax)
ax.set_title('Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur', fontsize=14)
ax.set_ylabel('Rata-rata Penggunaan Sepeda', fontsize=12)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Hari Libur', 'Hari Kerja'])
st.pyplot(fig, clear_figure=True)

# Tampilkan data yang difilter
if st.sidebar.checkbox("Tampilkan Data yang Difilter"):
    st.subheader("📋 Data Penggunaan Sepeda (Difilter)")
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