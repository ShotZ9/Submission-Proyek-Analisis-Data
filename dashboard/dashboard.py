import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('main_data.csv')

data = load_data()

# Sidebar
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pilih Visualisasi")

# Visualisasi 1: Tren Penggunaan Sepeda per Hari
if st.sidebar.checkbox("Tren Penggunaan Sepeda per Hari"):
    st.subheader("Tren Penggunaan Sepeda per Hari")
    daily_data = data.groupby('dteday')['cnt_hour'].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='dteday', y='cnt_hour', data=daily_data)
    plt.title('Tren Penggunaan Sepeda per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(plt)

# Visualisasi 2: Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur
if st.sidebar.checkbox("Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur"):
    st.subheader("Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
    workingday_data = data.groupby('workingday_hour')['cnt_hour'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x='workingday_hour', y='cnt_hour', data=workingday_data)
    plt.title('Pola Penggunaan Sepeda antara Hari Kerja dan Hari Libur')
    plt.xlabel('Hari Kerja (1) / Hari Libur (0)')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    st.pyplot(plt)

# Visualisasi 3: Distribusi Penggunaan Sepeda per Jam
if st.sidebar.checkbox("Distribusi Penggunaan Sepeda per Jam"):
    st.subheader("Distribusi Penggunaan Sepeda per Jam")
    hourly_data = data.groupby('hr')['cnt_hour'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt_hour', data=hourly_data)
    plt.title('Distribusi Penggunaan Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    st.pyplot(plt)

# Tampilkan data
if st.sidebar.checkbox("Tampilkan Data"):
    st.subheader("Data Penggunaan Sepeda")
    st.write(data)