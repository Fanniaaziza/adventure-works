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

# Fungsi memuat IMDB data
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1').head(10)  # Using only the first 10 rows

# Custom CSS for styling
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
        margin-bottom: 0;
    }
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
    .chart-container {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 10px;
        background-color: white;
        padding: 20px;
        margin: 20px 0;
    }
    .chart-container:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit title
st.markdown("<h1 class='title'>Final Project Mata Kuliah Data Visualisasi</h1>", unsafe_allow_html=True)

# Sidebar option untuk memilih data di display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Handling IMDB Top Movies data
if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.markdown("<h1 style='text-align: center; color: black;'>Scraping Website IMDB</h1>", unsafe_allow_html=True)
    st.dataframe(df_imdb)

    # Check keberadaan kolom
    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # kolom yang diharapkan
    if set(expected_columns).issubset(df_imdb.columns):
        # 1. Comparison: Number of Movies per Year
        year_counts = df_imdb['tahun'].value_counts().sort_index()

        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
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
            st.markdown("</div>", unsafe_allow_html=True)

        # 2. Relationship: Scatter Plot of Film Duration vs Rate
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
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
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 3. Distribution: Histogram of Film Duration Distribution
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
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
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 4. Composition: Pie Chart of Movie Count per Age Rating
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
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
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")

# Handling Adventure Works data
else:
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Memuat Adventure Works data
    df_sales = load_adventure_works_data()

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
            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            # Filter data berdasarkan year range
            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            # Plot comparison of total sales per year using Matplotlib
            with st.container():
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                plt.figure(figsize=(12, 6))
                plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
                plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
                plt.xlabel('Tahun', fontsize=14)
                plt.ylabel('Total Penjualan', fontsize=14)
                plt.grid(True)
                st.pyplot(plt)
                st.markdown("""
                Dari visualisasi di atas dapat dilihat adanya kenaikan penjualan tertinggi di tahun 2003 dan penjualan yang menurun di tahun 2004.
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

    # Query data bubble plot
    query_bubble = '''
    SELECT 
      st.SalesTerritoryRegion AS Country,
      SUM(fs.SalesAmount) AS TotalSales  
    FROM factinternetsales fs
    JOIN dimsalesterritory st
      ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY Country
    '''

    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )

    df_bubble = pd.read_sql(query_bubble, conn)

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.subheader('2. Hubungan Penjualan berdasarkan region')
    st.dataframe(df_bubble)

    # Adjust bubble size for better visibility
    with st.container():
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        plt.figure(figsize=(14, 12))
        plt.scatter(x=df_bubble['Country'], 
                    y=df_bubble['TotalSales'],
                    s=df_bubble['TotalSales'] / 1000,  # Adjust bubble size smaller for better visibility
                    c='b',
                    alpha=0.6,  # Add transparency for better visibility
                    edgecolors='w',  # Add white border to bubbles
                    linewidth=0.5)
        plt.xlabel('Country')
        plt.ylabel('Total Sales')  
        plt.title('Bubble Plot Hubungan Wilayah dan Penjualan')
        plt.grid(True)
        st.pyplot(plt)
        st.markdown("""
        Dari visualisasi di atas dapat dilihat adanya hubungan antara jumlah penjualan dengan region penjualan, region yang memiliki 
        daerah yang luas dan lebih besar cenderung menghasilkan penjualan produk yang besar pula.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Query data pie chart
    query_pie = '''
    SELECT
        st.SalesTerritoryRegion,
        SUM(fs.SalesAmount) AS TotalSales
    FROM
        factinternetsales fs
    JOIN
        dimsalesterritory st ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY
        st.SalesTerritoryRegion
    '''

    df_sales_by_region = pd.read_sql(query_pie, conn)

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.subheader('3. Proporsi Penjualan Berdasarkan Wilayah atau Region')
    st.dataframe(df_sales_by_region)

    # Create visualization of sales proportion per region
    with st.container():
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        plt.figure(figsize=(10, 6))
        plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
        plt.title('Proporsi Penjualan per Wilayah atau Region')
        plt.axis('equal')
        st.pyplot(plt)
        st.markdown("""
        Dari visualisasi di atas dapat dilihat prosentase penjualan produk dari berbagai region Australia dan southwest memiliki 
        prosentase penjualan tertinggi.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Query data bar chart
    query_bar = '''
    SELECT
        pc.EnglishProductCategoryName AS ProductCategory,
        SUM(fs.SalesAmount) AS TotalSales
    FROM
        factinternetsales fs
    JOIN
        dimproduct p ON fs.ProductKey = p.ProductKey
    JOIN
        dimproductsubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey
    JOIN
        dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
    GROUP BY
        pc.EnglishProductCategoryName
    '''

    df_bar = pd.read_sql(query_bar, conn)

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.subheader('4. Komposisi Penjualan Berdasarkan Kategori Produk')
    st.dataframe(df_bar)

    # Membuat figure and axes
    with st.container():
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df_bar['ProductCategory'], df_bar['TotalSales'], color='blue')
        ax.set(title='Komposisi Penjualan per Kategori Produk',
               ylabel='Total Penjualan',   
               xlabel='Kategori Produk')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown("""
        Dari visualisasi di atas dapat dilihat distribusi penjualan berdasarkan dari jenis produknya, penjualan terbesar berasal dari produk sepeda.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Menutup koneksi setelah digunakan
    conn.close()

# Menampilkan informasi data diri
st.markdown("""
    <p style='text-align: left; color: black; font-size: 14px;'>
    Nama : Fannia Nur Aziza<br>
    NPM : 21082010170<br>
    Mata Kuliah : Data Visualisasi<br>
    Paralel : B
    </p>
    """, unsafe_allow_html=True)
