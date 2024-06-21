import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat Adventure Works data
def load_adventure_works_data():
    try:
        conn = pymysql.connect(
            host=st.secrets["database"]["host"],
            port=int(st.secrets["database"]["port"]),
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            db=st.secrets["database"]["db"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        # SQL query untuk mengambil yearly sales data
        query_sales = """
            SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
            FROM dimtime
            JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
            GROUP BY CalendarYear
            ORDER BY CalendarYear
        """
        df_sales = pd.read_sql(query_sales, conn)
        
        # Memastikan kolom year adalah integer
        df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
        
        conn.close()
        return df_sales
    
    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memuat data Adventure Works: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika terjadi kesalahan

# Fungsi memuat IMDB data
def load_imdb_data():
    try:
        fn1 = 'IMDB-TOP.csv'
        return pd.read_csv(fn1, encoding='latin1').head(10)  # Menggunakan hanya 10 baris pertama
        
    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memuat data IMDB: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika terjadi kesalahan

# Streamlit title
st.title("Final Project Mata Kuliah Data Visualisasi")

# Sidebar option untuk memilih data di display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Handling IMDB Top Movies data
if option == 'IMDB Top Movies':
    st.markdown("<h2 style='text-align: center; color: black;'>Data Top Movies dari IMDB</h2>", unsafe_allow_html=True)
    
    df_imdb = load_imdb_data()
    st.write(df_imdb)

    if not df_imdb.empty:
        try:
            # 1. Perbandingan: Jumlah Film per Tahun
            year_counts = df_imdb['tahun'].value_counts().sort_index()

            plt.figure(figsize=(10, 6))
            plt.bar(year_counts.index.astype(str), year_counts.values, color='skyblue')
            plt.title('Perbandingan Jumlah Film per Tahun')
            plt.xlabel('Tahun')
            plt.ylabel('Jumlah Film')
            plt.xticks(rotation=45)
            plt.grid(True)
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
                Analisis: Jumlah film dapat bervariasi setiap tahun, misalnya hanya ada 2 film baru pada tahun 1994, 
                berbeda dengan tahun sebelumnya yang hanya memiliki 1 film.</p> 
            """, unsafe_allow_html=True)
            
            # 2. Hubungan: Scatter Plot Durasi Film vs Rate
            plt.figure(figsize=(10, 6))
            plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
            plt.title('Hubungan Antara Durasi Film dan Rate')
            plt.xlabel('Durasi Film (Menit)')
            plt.ylabel('Rate')
            plt.grid(True)
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
                Analisis: Terdapat hubungan antara durasi film dan rating yang tercermin dalam pola tren.</p>  
            """, unsafe_allow_html=True)
                
            # 3. Distribusi: Histogram Distribusi Durasi Film
            plt.figure(figsize=(10, 6))
            plt.hist(df_imdb['durasi'], bins=20, color='green', edgecolor='black')
            plt.title('Distribusi Durasi Film')
            plt.xlabel('Durasi Film (Menit)')
            plt.ylabel('Frekuensi')
            plt.grid(True)
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
                Analisis: Distribusi durasi film menunjukkan frekuensi yang seragam untuk setiap durasi.</p>
            """, unsafe_allow_html=True)
            
            # 4. Komposisi: Pie Chart Jumlah Film per Age Rating
            age_counts = df_imdb['age'].value_counts()

            plt.figure(figsize=(8, 8))
            plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
            plt.title('Komposisi Film Berdasarkan Age Rating')
            plt.axis('equal')
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
                Analisis: Film-film ditonton oleh berbagai kelompok usia, dengan kelompok remaja menonton sebagian besar.</p> 
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Terjadi kesalahan dalam visualisasi IMDB: {e}")

    else:
        st.warning('Data IMDB tidak tersedia.')

# Handling Adventure Works data
else:
    st.markdown("<h2 style='text-align: center; color: black;'>Dashboard Adventure Works</h2>", unsafe_allow_html=True)
    
    df_sales = load_adventure_works_data()
    st.markdown("<p style='color: black; font-size: 18px;'>Data Penjualan Tahunan</p>", unsafe_allow_html=True)
    st.dataframe(df_sales)

    if not df_sales.empty:
        try:
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            plt.figure(figsize=(12, 6))
            plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
            plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
            plt.xlabel('Tahun', fontsize=14)
            plt.ylabel('Total Penjualan', fontsize=14)
            plt.grid(True)
            st.pyplot(plt)

            st.markdown(f"<p style='color: black;'>Analisis: Kenaikan tertinggi dalam penjualan terjadi di tahun 2003, sedangkan penurunan terjadi di tahun 2004.</p>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam visualisasi Adventure Works: {e}")

    else:
        st.warning('Data penjualan Adventure Works tidak tersedia.')

# Informasi data diri
st.markdown("""
    <p style='text-align: left; color: black; font-size: 14px;'>
    Nama : Fannia Nur Aziza<br>
    NPM : 21082010170<br>
    Mata Kuliah : Data Visualisasi<br>
    Paralel : B
    </p>
""", unsafe_allow_html=True)
