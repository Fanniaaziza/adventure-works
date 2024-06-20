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
    Visualisasi ini menggunakan grafik batang untuk menunjukkan bagaimana jumlah film berubah dari tahun ke tahun dalam dataset IMDB-TOP.csv. 
    Grafik ini memberikan gambaran tentang seberapa aktifnya industri film dalam periode waktu yang dianalisis.
    """)
    
    # 2. Visualisasi Hubungan: Scatter Plot Durasi Film vs Rate
    plt.figure(figsize=(10, 6))
    plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
    plt.title('Hubungan Antara Durasi Film dan Rate')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Rate')
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    Scatter plot ini memvisualisasikan hubungan antara durasi film (sumbu x) dan rating IMDb (sumbu y). 
    Setiap titik merepresentasikan satu film dalam dataset. Pada plot ini, kita dapat melihat pola atau tren umum antara durasi film dengan rating IMDb, 
    meskipun tidak terlalu jelas dalam 10 data pertama yang ditampilkan.
    """)
        
    # 3. Visualisasi Distribusi: Histogram Distribusi Durasi Film
    plt.figure(figsize=(10, 6))
    plt.hist(df_imdb['durasi'], bins=20, color='green', edgecolor='black')
    plt.title('Distribusi Durasi Film')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('Frekuensi')
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    Histogram ini menunjukkan distribusi frekuensi durasi film dalam dataset. 
    Dengan membagi durasi film ke dalam beberapa bin, plot ini memberikan gambaran visual tentang sebaran durasi film yang ada. 
    Warna hijau digunakan untuk menyoroti distribusi ini, sementara garis tepi hitam menambahkan detail visual.
    """)
        
    # 4. Visualisasi Komposisi: Pie Chart Jumlah Film per Age Rating
    age_counts = df_imdb['age'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Komposisi Film Berdasarkan Age Rating')
    plt.axis('equal')
    st.pyplot(plt)

    st.markdown("""
    Pie chart ini memvisualisasikan komposisi jumlah film berdasarkan rating usia (Age Rating) dalam dataset. 
    Setiap sektor dalam pie chart mewakili persentase dari jumlah total film dalam kategori rating usia yang berbeda. 
    Chart ini membantu kita melihat seberapa beragam usia target penonton untuk film-film dalam dataset.
    """)

else:
    st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")
