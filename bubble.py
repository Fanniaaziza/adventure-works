import pymysql
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

# Membuat koneksi ke database MySQL
conn = pymysql.connect(
    host="kubela.id",
    port=3306,
    user="davis2024irwan",
    password="wh451n9m@ch1n3",
    database="aw"
)

# Cek koneksi berhasil
if conn:
    print('Connected to MySQL database')

# Query data untuk bubble plot
query = '''
SELECT 
  st.SalesTerritoryRegion AS Country,
  SUM(fs.SalesAmount) AS TotalSales  
FROM factinternetsales fs
JOIN dimsalesterritory st
  ON fs.SalesTerritoryKey = st.SalesTerritoryKey
GROUP BY Country
'''

# Membuat DataFrame dari hasil query
df_bubble = pd.read_sql(query, engine)

# Tambahkan argumen s untuk ukuran bubble
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

# Menambahkan grid untuk memudahkan pembacaan plot
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown("<h2 style='text-align: center;'>2. Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
st.pyplot(plt)
