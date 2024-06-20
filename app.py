import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat data Adventure Works
def load_adventure_works_data(conn):
    # Query SQL untuk mengambil data penjualan per tahun
    query_sales = """
        SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
        FROM dimtime
        JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
        GROUP BY CalendarYear
        ORDER BY CalendarYear
    """
    df_sales = pd.read_sql(query_sales, conn)

    # Ensure Year column is of integer type
    df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)

    return df_sales

# Fungsi untuk memuat data IMDB
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1')

# Koneksi Database MySQL
conn = pymysql.connect(
    host="kubela.id",
    port=3306,
    user="davis2024irwan",
    password="wh451n9m@ch1n3",
    database="aw"
)

# Memuat data Adventure Works
df_sales = load_adventure_works_data(conn)

# Memuat data IMDB
df_imdb = load_imdb_data()

# Menghitung rata-rata peringkat IMDb untuk setiap genre
avg_rating_genre = df_imdb.groupby('Genre')['IMDB Rating'].mean().sort_values(ascending=False)

# Plot bar untuk perbandingan rata-rata peringkat IMDb antara genre
plt.figure(figsize=(10, 6))
avg_rating_genre.plot(kind='bar', color='skyblue')
plt.title('Perbandingan Rata-Rata Peringkat IMDb antara Genre Film')
plt.xlabel('Genre')
plt.ylabel('Rata-Rata Peringkat IMDb')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Menampilkan judul dan deskripsi aplikasi Streamlit
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works & IMDB</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Data Penjualan & Data Film IMDB</h2>", unsafe_allow_html=True)

# Menu dropdown untuk memilih data yang akan ditampilkan
data_choice = st.selectbox("Pilih Data:", ("Data Penjualan Adventure Works", "Data Film IMDB"))

if data_choice == "Data Film IMDB":
    st.subheader('Data Film IMDB')
    st.dataframe(df_imdb)

elif data_choice == "Data Penjualan Adventure Works":
    st.subheader('Data Penjualan Adventure Works')
    st.dataframe(df_sales)

    # Ensure Year column is of integer type
    df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
    tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

    # Pilihan untuk memilih rentang tahun menggunakan slider
    year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

    # Filter data berdasarkan rentang tahun yang dipilih
    df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

    # Plot perbandingan total penjualan per tahun dengan Matplotlib
    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
    plt.xlabel('Tahun', fontsize=14)
    plt.ylabel('Total Penjualan', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

    # Query data untuk bubble plot
    query_bubble = '''
    SELECT 
      st.SalesTerritoryRegion AS Country,
      SUM(fs.SalesAmount) AS TotalSales  
    FROM factinternetsales fs
    JOIN dimsalesterritory st
      ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY Country
    '''

    df_bubble = pd.read_sql(query_bubble, conn)

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('Hubungan Wilayah dan Penjualan')
    st.dataframe(df_bubble)

    # Menambahkan bubble plot
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
    plt.grid(True)

    # Menampilkan plot di Streamlit
    st.pyplot(plt)

    # Query data untuk pie chart
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

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('Proporsi Penjualan per Wilayah atau Region')
    st.dataframe(df_sales_by_region)

    # Buat visualisasi proporsi penjualan per wilayah atau region
    plt.figure(figsize=(10, 6))
    plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
    plt.title('Proporsi Penjualan per Wilayah atau Region')
    plt.axis('equal')  # Membuat pie chart menjadi lingkaran

    # Menampilkan plot di Streamlit
    st.pyplot(plt)

    # Query data untuk bar plot
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

    # Menutup koneksi setelah selesai digunakan
    conn.close()

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('Komposisi Penjualan per Kategori Produk')
    st.dataframe(df_bar)

    # Buat figure dan axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bar (lebih cocok daripada histogram untuk kategori)
    ax.bar(df_bar['ProductCategory'], df_bar['TotalSales'], color='blue')

    # Setting label        
    ax.set(title='Komposisi Penjualan per Kategori Produk',
           ylabel='Total Penjualan',   
           xlabel='Kategori Produk')

    # Rotasi label x untuk lebih baik
    plt.xticks(rotation=45)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
