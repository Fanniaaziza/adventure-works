import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Membuat engine SQLAlchemy untuk koneksi ke MySQL
engine = create_engine("mysql+pymysql://davis2024irwan:wh451n9m@ch1n3@kubela.id:3306/aw")

# Fungsi untuk menjalankan query dan mengembalikan DataFrame
def run_query(query):
    with engine.connect() as conn:
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

# Query SQL untuk mengambil data penjualan per tahun
query_sales = """
    SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
    FROM dimtime
    JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
    GROUP BY CalendarYear
    ORDER BY CalendarYear
"""

# Menjalankan query untuk data penjualan per tahun
df_sales = run_query(query_sales)

# Menampilkan judul dashboard
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

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
st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan</h2>", unsafe_allow_html=True)
st.pyplot(plt)

# Query data untuk bubble plot
query_bubble = '''
    SELECT 
      st.SalesTerritoryRegion AS Country,
      SUM(fs.SalesAmount) AS TotalSales  
    FROM factinternetsales fs
    JOIN dimsalesterritory st
      ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY Country
'''

# Menjalankan query untuk bubble plot
df_bubble = run_query(query_bubble)

# Membuat bubble plot
plt.figure(figsize=(14, 12))
plt.scatter(x=df_bubble['Country'], 
            y=df_bubble['TotalSales'],
            s=df_bubble['TotalSales'] / 1000,  # Ukuran bubble diatur lebih kecil untuk visibilitas yang lebih baik
            c='b',
            alpha=0.6,  # Menambahkan transparansi untuk visibilitas yang lebih baik
            edgecolors='w',  # Menambahkan border putih pada bubble
            linewidth=0.5)

# Menambahkan label untuk sumbu x dan y serta judul plot
plt.xlabel('Country')
plt.ylabel('Total Sales')  
plt.title('Bubble Plot Hubungan Wilayah dan Penjualan')
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown("<h2 style='text-align: center;'>2. Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
st.pyplot(plt)
