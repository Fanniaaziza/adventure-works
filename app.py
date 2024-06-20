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

    # 2. Visualisasi Hubungan: Scatter Plot Durasi Film vs Rate
    st.subheader("Hubungan Antara Durasi Film dan Rate")

    plt.figure(figsize=(10, 6))
    plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
    plt.title('Hubungan Antara Durasi Film dan Rate')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Rate')
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    Scatter plot ini memvisualisasikan hubungan antara durasi film (di sumbu x) dan rating IMDb (di sumbu y). 
    Titik-titik tersebar menunjukkan distribusi durasi film dan rating IMDb untuk setiap data film dalam dataset.
    """)

    # 3. Visualisasi Distribusi: Histogram Distribusi Durasi Film
    st.subheader("Distribusi Durasi Film")

    # Plot line histogram untuk distribusi durasi film
    plt.figure(figsize=(10, 6))
    plt.hist(df_imdb_subset['Duration'], bins=10, color='green', edgecolor='black', linewidth=1.2, alpha=0.7)
    plt.title('Distribusi Durasi Film')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Frekuensi')
    plt.grid(True)
    plt.show()

    # 4. Visualisasi Komposisi: Pie Chart Jumlah Film per Age Rating
    st.subheader("Komposisi Film Berdasarkan Age Rating")

    age_counts = df_imdb['age'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Komposisi Film Berdasarkan Age Rating')
    plt.axis('equal')
    st.pyplot(plt)

    st.markdown("""
    Pie chart ini memvisualisasikan komposisi jumlah film berdasarkan rating usia (Age Rating). 
    Setiap sektor dalam pie chart menunjukkan persentase jumlah film dalam kategori rating usia yang berbeda.
    """)

else:
    st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")
