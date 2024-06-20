import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Fungsi untuk memuat data IMDB
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1')

# Memuat data IMDB
df_imdb = load_imdb_data()

# Menampilkan judul dan deskripsi aplikasi Streamlit
st.markdown("<h2 style='text-align: center; color: black;'>Visualisasi Data Film IMDB</h2>", unsafe_allow_html=True)

# Menu dropdown untuk memilih jenis visualisasi
visual_choice = st.selectbox("Pilih Jenis Visualisasi:", ["Perbandingan", "Hubungan", "Distribusi", "Komposisi"])

# Visualisasi Perbandingan: Bar plot rata-rata peringkat IMDb antara genre film
if visual_choice == "Perbandingan":
    avg_rating_genre = df_imdb.groupby('Genre')['IMDB Rating'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    avg_rating_genre.plot(kind='bar', color='skyblue')
    plt.title('Perbandingan Rata-Rata Peringkat IMDb antara Genre Film')
    plt.xlabel('Genre')
    plt.ylabel('Rata-Rata Peringkat IMDb')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

# Visualisasi Hubungan: Scatter plot durasi film (Minutes) vs IMDB Rating
elif visual_choice == "Hubungan":
    plt.figure(figsize=(10, 6))
    plt.scatter(df_imdb['Minutes'], df_imdb['IMDB Rating'], alpha=0.5, color='orange')
    plt.title('Hubungan Antara Durasi Film dan Peringkat IMDb')
    plt.xlabel('Durasi Film (Menit)')
    plt.ylabel('IMDB Rating')
    plt.grid(True)
    st.pyplot(plt)

# Visualisasi Distribusi: Histogram distribusi peringkat IMDb
elif visual_choice == "Distribusi":
    plt.figure(figsize=(10, 6))
    plt.hist(df_imdb['IMDB Rating'], bins=20, color='green', edgecolor='black')
    plt.title('Distribusi Peringkat IMDb')
    plt.xlabel('IMDB Rating')
    plt.ylabel('Frekuensi')
    plt.grid(True)
    st.pyplot(plt)

# Visualisasi Komposisi: Pie chart komposisi film berdasarkan genre
elif visual_choice == "Komposisi":
    genre_counts = df_imdb['Genre'].value_counts()
    
    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Komposisi Film Berdasarkan Genre')
    plt.axis('equal')
    st.pyplot(plt)
