import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

main_data = pd.read_csv('main_data.csv')
main_data['dteday'] = pd.to_datetime(main_data['dteday']) 

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}

main_data['season'] = main_data['season'].map(season_mapping)
main_data['weekday'] = main_data['weekday'].map(weekday_mapping)

st.set_page_config(layout="wide")
st.title("Bike Sharing Dashboard")

st.sidebar.subheader("Filter Tanggal")

start_date = pd.to_datetime('2011-01-01')
end_date = pd.to_datetime('2012-12-31')

date_range = st.sidebar.date_input(
    "Rentang Waktu:",
    [start_date, end_date],
    min_value=start_date,
    max_value=main_data['dteday'].max()
)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered_data = main_data[(main_data['dteday'] >= start_date) & (main_data['dteday'] <= end_date)]

option = st.sidebar.radio(
    "Visualisasi:",
    ("Distribusi penggunaan sepeda untuk setiap musim", 
     "Rata-rata pengguna terdaftar per hari dalam seminggu")
)

if option == "Distribusi penggunaan sepeda untuk setiap musim":
    st.subheader("Distribusi penggunaan sepeda untuk setiap musim")

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='season', y='cnt', data=filtered_data, ax=ax1)
    ax1.set_title('Distribusi Penggunaan Sepeda per Musim')
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Jumlah penggunaan sepeda')
    st.pyplot(fig1)

elif option == "Rata-rata pengguna terdaftar per hari dalam seminggu":
    st.subheader("Rata-rata pengguna terdaftar per hari dalam seminggu")

    weekday_avg_registered = filtered_data.groupby('weekday')['registered'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weekday', y='registered', data=weekday_avg_registered, ax=ax2)
    ax2.set_title('Rata-rata pengguna terdaftar per hari dalam seminggu')
    ax2.set_xlabel('Hari dalam satu minggu')
    ax2.set_ylabel('Rata-rata pengguna terdaftar')
    st.pyplot(fig2)
