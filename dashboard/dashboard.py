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
    return products_df, order_reviews_df, order_items_df, order_payments_df

# Load data
products_df, order_reviews_df, order_items_df, order_payments_df = load_data()

# Gabungkan data
products_orders_df = products_df.merge(order_items_df, on='product_id', how='inner')
full_data_df = products_orders_df.merge(order_payments_df, on='order_id', how='inner')

# Sidebar interaktif: Filter berdasarkan metode pembayaran
st.sidebar.title("Filter Data")
payment_type = st.sidebar.multiselect(
    "Pilih Metode Pembayaran:", 
    full_data_df['payment_type'].unique(), 
    default=full_data_df['payment_type'].unique()
)

# Filter data
filtered_data = full_data_df[full_data_df['payment_type'].isin(payment_type)]

# Dashboard Title
st.title("E-commerce Data Analysis Dashboard")

# Visualisasi 1: Kategori produk dengan jumlah penjualan terbanyak dan terendah
st.subheader("Kategori Produk dengan Penjualan Terbanyak dan Terendah")
product_sales = filtered_data.groupby('product_category_name')['order_id'].count().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=product_sales.head(10).index, y=product_sales.head(10).values, ax=ax, palette='viridis')
ax.set_title("Top 10 Kategori Produk Terlaris")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)

# Visualisasi 2: Metode pembayaran yang paling sering dan jarang digunakan
st.subheader("Metode Pembayaran Terpopuler dan Jarang Digunakan")
payment_counts = filtered_data['payment_type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax, palette='pastel')
ax.set_title("Frekuensi Penggunaan Metode Pembayaran")
st.pyplot(fig)

# Visualisasi 3: Distribusi rata-rata review score
st.subheader("Distribusi Rata-rata Review Score")
avg_review_score = order_reviews_df.groupby('review_score')['review_id'].count()
fig, ax = plt.subplots()
sns.lineplot(x=avg_review_score.index, y=avg_review_score.values, marker='o', ax=ax)
ax.set_title("Distribusi Review Score")
ax.set_xlabel("Review Score")
ax.set_ylabel("Jumlah Review")
st.pyplot(fig)

st.write("Dashboard ini menampilkan insight tentang penjualan produk, metode pembayaran, dan review pelanggan. Gunakan filter di sidebar untuk eksplorasi lebih dalam!")


# Jalankan di terminal: streamlit run app.py
# komentar
