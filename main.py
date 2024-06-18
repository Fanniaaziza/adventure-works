import pymysql
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

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

# Query data dari database
query = "SELECT * from dimpromotion"
data = pd.read_sql(query, conn)

# Menampilkan data dalam bentuk tabel di Streamlit
st.write("Data dari Database:")
st.dataframe(data)
