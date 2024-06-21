import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat Adventure Works data
def load_adventure_works_data():
    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
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

# Streamlit title
st.markdown("""
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #4b4b4b;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #fc466b, #3f5efb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <h1 class="title">Final Project Mata Kuliah Data Visualisasi</h1>
    """, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1, h2 {
        color: #4b4b4b;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .css-1aumxhk {
        color: #4b4b4b;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# Fungsi memuat IMDB data
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1').head(10)  # Using only the first 10 rows

# Fungsi untuk menampilkan data Adventure Works
def show_adventure_works_data(df_sales):
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.subheader('1. Data Penjualan Tahunan')
    st.dataframe(df_sales)

    # cek DataFrame memastikan tidak kosong 
    if not df_sales.empty:
        try:
            # Memastikan kolom Year merupakan integer
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            # Pilihan untuk select year range menggunakan slider
            year_range = st.slider('Pilih Rentang Tahun Penjualan Adventure Works:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            # Tambahkan teks penjelasan di bawah slider
            if year_range[0] == year_range[1]:
                st.write(f"Anda memilih tahun {year_range[0]} untuk analisis.")
            else:
                st.write(f"Anda memilih rentang tahun {year_range[0]} hingga {year_range[1]} untuk analisis.")

            # Filter data berdasarkan year range
            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            # Plot comparison of total sales per year using Matplotlib
            plt.figure(figsize=(12, 6))
            plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
            plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
            plt.xlabel('Tahun', fontsize=14)
            plt.ylabel('Total Penjualan', fontsize=14)
            plt.grid(True)

            # Display plot in Streamlit
            st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan Tahun {year_range[0]}-{year_range[1]}</h2>", unsafe_allow_html=True)
            st.pyplot(plt)

            # Tambahkan penjelasan dinamis sesuai dengan rentang tahun yang dipilih
            if year_range[0] == year_range[1]:
                st.markdown(f"""
                Dari visualisasi di atas, Anda dapat melihat bagaimana penjualan berfluktuasi dari tahun ke tahun di tahun {year_range[0]}. 
                """)
            else:
                st.markdown(f"""
                Dari visualisasi di atas, Anda dapat melihat bagaimana penjualan berfluktuasi dari tahun {year_range[0]} hingga {year_range[1]}. 
                """)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

# Handling IMDB Top Movies data
def show_imdb_data():
    df_imdb = load_imdb_data()
    st.write("<h1 style='text-align: center; color: black;'>Scraping Website IMDB</h1>", unsafe_allow_html=True)
    st.write(df_imdb)

    # Check keberadaan kolom
    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # kolom yang diharapkan
    if set(expected_columns).issubset(df_imdb.columns):
        # 1. Comparison : Number of Movies per Year
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
        Dari visualisasi tersebut dapat di analisis bahwa jumlah film dapat berubah tiap tahunnya, 
        seperti pada tahun 1994 film baru mencapai 2 film. Berbeda dengan tahun sebelumnya yang hanya ada 1 film. 
        """)
        
        # 2. Relationship : Scatter Plot of Film Duration vs Rate
        plt.figure(figsize=(10, 6))
        plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
        plt.title('Hubungan Antara Durasi Film dan Rate')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Rate')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
         Dari visualisasi tersebut dapat di analisis bahwa terdapat hubungan antara durasi film dan rating 
         yang digambarkan dengan terbentuknya pola tren.  
        """)
            
        # 3. Distribution : Histogram of Film Duration Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df_imdb['durasi'], bins=20, color='green', edgecolor='black')
        plt.title('Distribusi Durasi Film')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Frekuensi')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
        Dari visualisasi tersebut menggambarkan distribusi durasi film yang ada, 
        dari visualisasi tersebut dapat disimpulkan frekuensi dari masing-masing durasi film yang ada adalah sama, yakni memiliki 1 frekuensi.
        """)
            
        # 4. Composition : Pie Chart of Movie Count per Age Rating
        age_counts = df_imdb['age'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Komposisi Film Berdasarkan Age Rating')
        plt.axis('equal')
        st.pyplot(plt)

        st.markdown("""
        Dari visualisasi tersebut dapat di analisis bahwa film-film ditonton dari berbagai kalangan usia, 
        pada pie chart tersebut dapat disimpulkan kalangan yang menonton film rata-rata adalah usia remaja. 
        """)

    else:
        st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")

# Sidebar option untuk memilih data di display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Memuat dan menampilkan data berdasarkan opsi yang dipilih
if option == 'IMDB Top Movies':
    show_imdb_data()
else:
    df_sales = load_adventure_works_data()
    show_adventure_works_data(df_sales)

# Menampilkan informasi data diri
st.markdown("""<p style='text-align: left; color: black; font-size: 14px;'>Nama : Fannia Nur Aziza<br>
                NPM : 21082010170<br>
                Mata Kuliah : Data Visualisasi<br>
                Paralel : B</p>""", unsafe_allow_html=True)
