import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
@st.cache_data
def load_data():
    products_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_products_dataset.csv")
    order_reviews_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_order_reviews_dataset.csv")
    order_items_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_order_items_dataset.csv")
    order_payments_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_order_payments_dataset.csv")
    orders_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_orders_dataset.csv")
    customers_df = pd.read_csv("https://raw.githubusercontent.com/Evameivina/proyek_data/refs/heads/main/data/olist_customers_dataset.csv")
    return products_df, order_reviews_df, order_items_df, order_payments_df, orders_df, customers_df

products_df, order_reviews_df, order_items_df, order_payments_df, orders_df, customers_df = load_data()

# Sidebar navigation
st.sidebar.title("Dashboard Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Home", "EDA", "Advanced Analysis", "Conclusion"])

# Home Page
if page == "Home":
    st.title("E-commerce Data Analysis Dashboard")
    st.write("""
    Dashboard ini menyajikan hasil eksplorasi data, analisis lanjutan, dan insight terkait data transaksi e-commerce.
    """)

# EDA Page
elif page == "EDA":
    st.title("Exploratory Data Analysis (EDA)")

    # Kategori produk dengan jumlah penjualan terbanyak
    st.subheader("Kategori Produk Terlaris dan Terendah")
    product_sales = order_items_df.groupby('product_id')['order_id'].count().reset_index()
    top_selling = product_sales.sort_values(by='order_id', ascending=False).head(10)
    st.bar_chart(top_selling.set_index('product_id'))

    # Metode pembayaran paling sering digunakan
    st.subheader("Metode Pembayaran Terpopuler")
    payment_methods = order_payments_df['payment_type'].value_counts()
    st.bar_chart(payment_methods)

    # Distribusi rata-rata review score
    st.subheader("Distribusi Rata-rata Review Score")
    avg_review_score = order_reviews_df.groupby('review_score')['review_id'].count()
    st.line_chart(avg_review_score)

# Advanced Analysis Page
elif page == "Advanced Analysis":
    st.title("Advanced Analysis")

    # RFM Analysis
    st.subheader("RFM Analysis")
    orders_per_customer = orders_df.groupby('customer_id')['order_id'].nunique().reset_index()
    orders_per_customer.columns = ['customer_id', 'total_orders']
    st.write(orders_per_customer.head())

    # Manual Clustering - Grouping berdasarkan jumlah order
    st.subheader("Manual Clustering: Grouping Berdasarkan Jumlah Order")
    orders_per_customer['order_group'] = pd.cut(orders_per_customer['total_orders'], bins=[0, 1, 3, 5, 10, 100], labels=["1x", "2-3x", "4-5x", "6-10x", "10x+"])
    st.bar_chart(orders_per_customer['order_group'].value_counts())

# Conclusion Page
elif page == "Conclusion":
    st.title("Conclusion & Insights")
    st.write("""
    **1. Kategori produk terlaris:** Produk kategori 'cama_mesa_banho' menjadi yang paling banyak terjual.  
    **2. Metode pembayaran terpopuler:** 'Credit card' adalah metode pembayaran yang paling sering digunakan pelanggan.  
    **3. Distribusi review score:** Sebagian besar produk mendapatkan review score tinggi (4 dan 5).  
    **4. Customer behavior (RFM Analysis):** Sebagian besar pelanggan hanya melakukan satu kali transaksi.  
    **5. Clustering pelanggan:** Manual grouping menunjukkan pelanggan dengan frekuensi pembelian tinggi cukup jarang.  
    """)

# Jalankan di terminal: streamlit run app.py
