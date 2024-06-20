import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat data IMDB
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1')

# Memuat data IMDB
df_imdb = load_imdb_data()

# Menampilkan judul dan deskripsi aplikasi Streamlit
st.markdown("<h2 style='text-align: center; color: black;'>Data Film IMDB</h2>", unsafe_allow_html=True)
st.dataframe(df_imdb)

# Check if necessary columns exist
if {'Title', 'Year', 'Duration', 'Age', 'Rate'}.issubset(df_imdb.columns):
    # 1. Visualisasi Perbandingan: Jumlah Film per Tahun
    year_counts = df_imdb['Year'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(year_counts.index.astype(str), year_counts.values, color='skyblue')
    plt.title('Perbandingan Jumlah Film per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Film')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    # 2. Visualisasi Hubungan: Scatter Plot Durasi Film vs Rate
    plt.figure(figsize=(10, 6))
    plt.scatter(df_imdb['Duration'], df_imdb['Rate'], alpha=0.5, color='orange')
    plt.title('Hubungan Antara Durasi Film dan Rate')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Rate')
    plt.grid(True)
    st.pyplot(plt)

    # 3. Visualisasi Distribusi: Histogram Distribusi Durasi Film
    plt.figure(figsize=(10, 6))
    plt.hist(df_imdb['Duration'], bins=20, color='green', edgecolor='black')
    plt.title('Distribusi Durasi Film')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Frekuensi')
    plt.grid(True)
    st.pyplot(plt)

    # 4. Visualisasi Komposisi: Pie Chart Jumlah Film per Age Rating
    age_counts = df_imdb['Age'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Komposisi Film Berdasarkan Age Rating')
    plt.axis('equal')
    st.pyplot(plt)

else:
    st.write("Kolom yang diperlukan (Title, Year, Duration, Age, Rate) tidak lengkap dalam dataset.")
