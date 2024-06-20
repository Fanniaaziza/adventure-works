import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat data IMDB
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1').head(10)  # Menggunakan hanya 10 data pertama

# Memuat data IMDB (hanya 10 data pertama)
df_imdb = load_imdb_data()

# Menampilkan judul dan deskripsi aplikasi Streamlit
st.markdown("<h2 style='text-align: center; color: black;'>Data Film IMDB</h2>", unsafe_allow_html=True)
st.dataframe(df_imdb)

# Check if necessary columns exist
expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # Kolom yang diharapkan
if set(expected_columns).issubset(df_imdb.columns):
    # 1. Visualisasi Perbandingan: Jumlah Film per Tahun
    st.subheader("Perbandingan Jumlah Film per Tahun")

    year_counts = df_imdb['tahun'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(year_counts.index.astype(str), year_counts.values, color='skyblue')
    plt.title('Perbandingan Jumlah Film per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Film')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    Visualisasi ini menunjukkan bagaimana jumlah film berubah dari tahun ke tahun berdasarkan dataset IMDB-TOP.csv. Grafik batang
    menampilkan tahun di sumbu x dan jumlah film di sumbu y. Dari visualisasi ini, dapat dilihat pola perubahan jumlah film dari tahun ke tahun.
    """)

    # 2. Visualisasi Hubungan: Bubble Chart Durasi Film vs Rate
    st.subheader("Hubungan Antara Durasi Film dan Rate (Bubble Chart)")

    # Preprocessing rate column
    df_imdb['rate'] = pd.to_numeric(df_imdb['rate'], errors='coerce')  # Convert to numeric, coerce errors to NaN

    # Normalize rate values for marker size
    min_rate = df_imdb['rate'].min()
    max_rate = df_imdb['rate'].max()
    normalized_sizes = 1000 * (df_imdb['rate'] - min_rate) / (max_rate - min_rate)  # Scale to 1000 for marker sizes

    # Check for NaN values in durasi or rate
    if df_imdb[['durasi', 'rate']].isnull().any().any():
        st.error("Ada nilai NaN dalam kolom 'durasi' atau 'rate'. Periksa dan perbaiki data sebelum melanjutkan.")
    else:
        plt.figure(figsize=(10, 6))
        plt.scatter(df_imdb['durasi'], df_imdb['rate'], s=normalized_sizes, alpha=0.5, color='orange')
        plt.title('Hubungan Antara Durasi Film dan Rate')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Rate')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
        Bubble chart ini memvisualisasikan hubungan antara durasi film (di sumbu x) dan rating IMDb (di sumbu y). 
        Ukuran bubble menunjukkan rating IMDb untuk setiap data film dalam dataset, di mana semakin besar bubble, semakin tinggi ratingnya.
        Titik-titik tersebar menunjukkan distribusi durasi film dan rating IMDb untuk setiap data film dalam dataset.
        """)

else:
    st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")
