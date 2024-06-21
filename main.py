import pymysql
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

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

# Streamlit title
st.title("Final Project Mata Kuliah Data Visualisasi")

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

# Sidebar option untuk memilih data di display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Handling IMDB Top Movies data
if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.title("Scraping Website IMDB")
    st.write(df_imdb)

    # Check keberadaan kolom
    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # kolom yang diharapkan
    if set(expected_columns).issubset(df_imdb.columns):
        # 1. Comparison: Number of Movies per Year
        year_counts = df_imdb['tahun'].value_counts().sort_index()

        # Create a bar chart with Plotly
        fig1 = px.bar(
            x=year_counts.index.astype(str), 
            y=year_counts.values, 
            labels={'x': 'Tahun', 'y': 'Jumlah Film'}, 
            title='Perbandingan Jumlah Film per Tahun',
            color=year_counts.values,  # Color by the number of movies
            color_continuous_scale='Blues'  # Use a color scale for better visualization
        )

        # Customize the appearance
        fig1.update_layout(
            xaxis_title='Tahun',
            yaxis_title='Jumlah Film',
            xaxis_tickangle=-45,
            template='plotly_white'
        )

        # Display the interactive plot in Streamlit
        st.plotly_chart(fig1)

        st.markdown("""
        Dari visualisasi tersebut dapat di analisis bahwa jumlah film dapat berubah tiap tahunnya, 
        seperti pada tahun 1994 film baru mencapai 2 film. Berbeda dengan tahun sebelumnya yang hanya ada 1 film. 
        """)

        # 2. Relationship Visualization: Scatter Plot of Film Duration vs Rate
        fig2 = px.scatter(df_imdb, x='durasi', y='rate', title='Hubungan Antara Durasi Film dan Rate',
                          labels={'durasi': 'Durasi Film (Menit)', 'rate': 'Rate'},
                          color='rate', color_continuous_scale='Viridis')
        st.plotly_chart(fig2)

        st.markdown("""
         Dari visualisasi tersebut dapat di analisis bahwa terdapat hubungan antara durasi film dan rating 
         yang digambarkan dengan terbentuknya pola tren.  
        """)

        # 3. Distribution Visualization: Histogram of Film Duration Distribution
        fig3 = px.histogram(df_imdb, x='durasi', nbins=20, title='Distribusi Durasi Film',
                            labels={'durasi': 'Durasi Film (Menit)'}, color_discrete_sequence=['green'])
        st.plotly_chart(fig3)

        st.markdown("""
        Dari visualisasi tersebut menggambarkan distribusi durasi film yang ada, 
        dari visualisasi tersebut dapat disimpulkan frekuensi dari masing-masing durasi film yang ada adalah sama, yakni memiliki 1 frekuensi.
        """)

        # 4. Composition Visualization: Pie Chart of Movie Count per Age Rating
        age_counts = df_imdb['age'].value_counts()
        fig4 = px.pie(values=age_counts.values, names=age_counts.index, title='Komposisi Film Berdasarkan Age Rating',
                      labels={'index': 'Age Rating', 'values': 'Jumlah Film'})
        st.plotly_chart(fig4)

        st.markdown("""
        Dari visualisasi tersebut dapat di analisis bahwa film-film ditonton dari berbagai kalangan usia, 
        pada pie chart tersebut dapat disimpulkan kalangan yang menonton film rata-rata adalah usia remaja. 
        """)

    else:
        st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")

# Handling Adventure Works data
else:
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Load Adventure Works data
    df_sales = load_adventure_works_data()

    # Display DataFrame in Streamlit as a table
    st.subheader('1. Data Penjualan Tahunan')
    st.dataframe(df_sales)

    # Check if the DataFrame is not empty
    if not df_sales.empty:
        try:
            # Ensure Year column is of integer type
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            # Option to select year range using a slider
            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            # Filter data based on selected year range
            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            # Plot comparison of total sales per year using Plotly
            fig5 = px.line(df_filtered, x='Year', y='TotalSales', title=f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}',
                           labels={'Year': 'Tahun', 'TotalSales': 'Total Penjualan'}, markers=True)
            st.plotly_chart(fig5)

            st.markdown("""
            Dari visualisasi di atas dapat dilihat adanya kenaikan penjualan tertinggi di tahun 2003 dan penjualan yang menurun di tahun 2004.
            """)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

    # Query data for bubble plot
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

    # Display DataFrame in Streamlit as a table
    st.subheader('2. Hubungan Penjualan berdasarkan region')
    st.dataframe(df_bubble)

    # Create a bubble chart using Plotly
    fig6 = px.scatter(df_bubble, x='Country', y='TotalSales', size='TotalSales', title='Bubble Plot Hubungan Wilayah dan Penjualan',
                      labels={'Country': 'Wilayah', 'TotalSales': 'Total Penjualan'}, color='TotalSales',
                      color_continuous_scale='Blues')
    st.plotly_chart(fig6)

    st.markdown("""
        Dari visualisasi di atas dapat dilihat adanya hubungan antara jumlah penjualan dengan region penjualan, region yang memiliki 
        daerah yang luas dan lebih besar cenderung menghasilkan penjualan produk yang besar pula.
    """)

    # Query data for pie chart
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

    # Display DataFrame in Streamlit as a table
    st.subheader('3. Proporsi Penjualan Berdasarkan Wilayah atau Region')
    st.dataframe(df_sales_by_region)

    # Create a pie chart using Plotly
    fig7 = px.pie(df_sales_by_region, values='TotalSales', names='SalesTerritoryRegion', title='Proporsi Penjualan per Wilayah atau Region')
    st.plotly_chart(fig7)

    st.markdown("""
        Dari visualisasi di atas dapat dilihat prosentase penjualan produk dari berbagai region Australia dan southwest memiliki 
        prosentase penjualan tertinggi.
    """)

    # Query data for bar chart
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

    # Display DataFrame in Streamlit as a table
    st.subheader('4. Komposisi Penjualan Berdasarkan Kategori Produk')
    st.dataframe(df_bar)

    # Create bar chart using Plotly
    fig8 = px.bar(df_bar, x='ProductCategory', y='TotalSales', title='Komposisi Penjualan per Kategori Produk',
                  labels={'ProductCategory': 'Kategori Produk', 'TotalSales': 'Total Penjualan'},
                  color='TotalSales', color_continuous_scale='Blues')
    st.plotly_chart(fig8)

    st.markdown("""
        Dari visualisasi di atas dapat dilihat distribusi penjualan berdasarkan dari jenis produknya, penjualan terbesar berasal dari produk sepeda.
    """)

    # Close connection after usage
    conn.close()

# Menampilkan informasi data diri
st.markdown("""<p style='text-align: left; color: black; font-size: 14px;'>Nama : Fannia Nur Aziza<br>
                NPM : 21082010170<br>
                Mata Kuliah : Data Visualisasi<br>
                Paralel : B</p>""", unsafe_allow_html=True)
