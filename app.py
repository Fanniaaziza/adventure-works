import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membuat koneksi ke database MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    database='dump-dw_aw'
)

# Cek koneksi berhasil
if connection.is_connected():
    print('Connected to MySQL database')

# Membuat cursor
cursor = connection.cursor()

# Query SQL untuk mengambil data penjualan per tahun
query = """
    SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
    FROM dimtime
    JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
    GROUP BY CalendarYear
    ORDER BY CalendarYear
"""

# Eksekusi query
cursor.execute(query)
data = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
connection.close()

# Menampilkan judul dashboard
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# Membuat DataFrame dari hasil query
df_sales = pd.DataFrame(data, columns=['Year', 'TotalSales'])

# Konversi kolom 'Year' ke tipe data integer
df_sales['Year'] = df_sales['Year'].astype(int)

# Menampilkan DataFrame di Streamlit dalam bentuk tabel
st.subheader('1. Data Penjualan Tahunan')
st.dataframe(df_sales)

# Rentang tahun yang tersedia
tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

# Pilihan untuk memilih rentang tahun menggunakan slider
year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

# Filter data berdasarkan rentang tahun yang dipilih
df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

# Plot perbandingan total penjualan per tahun dengan Matplotlib
plt.figure(figsize=(12, 6))
plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
plt.xlabel('Tahun', fontsize=14)
plt.ylabel('Total Penjualan', fontsize=14)
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan </h2>", unsafe_allow_html=True)
st.pyplot(plt)
