import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

sns.set(style="whitegrid")

st.set_page_config(page_title="Dashboard Persebaran Wilayah Pelanggan Olist", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "main_data.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


main_df = load_data()

# ============ SIDEBAR ============
st.sidebar.title("Filter Dashboard")
st.sidebar.markdown("Gunakan filter berikut untuk mengeksplorasi persebaran wilayah pelanggan Olist.")

region_options = ["Semua Region"] + sorted(main_df["customer_region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Pilih Region", region_options)

if selected_region != "Semua Region":
    filtered_df = main_df[main_df["customer_region"] == selected_region]
else:
    filtered_df = main_df

state_options = ["Semua State"] + sorted(filtered_df["customer_state"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Pilih State", state_options)

if selected_state != "Semua State":
    filtered_df = filtered_df[filtered_df["customer_state"] == selected_state]

st.sidebar.markdown("---")
st.sidebar.caption("Sumber data: E-Commerce Public Dataset (Olist) — customers & geolocation.")

# ============ HEADER ============
st.title("Dashboard Persebaran Wilayah Pelanggan Olist")
st.markdown(
    "Dashboard ini menyajikan analisis persebaran geografis pelanggan Olist Store "
    "untuk mendukung keputusan ekspansi logistik dan target campaign regional."
)

# ============ METRICS ============
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan (sesuai filter)", f"{filtered_df.shape[0]:,}")
with col2:
    st.metric("Jumlah State Terjangkau", filtered_df["customer_state"].nunique())
with col3:
    st.metric("Jumlah Kota Terjangkau", filtered_df["customer_city"].nunique())

st.markdown("---")

# ============ PERTANYAAN 1 ============
st.subheader("Pertanyaan 1: Distribusi Pelanggan berdasarkan State & Kota")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 State berdasarkan Jumlah Pelanggan**")
    state_counts = (
        filtered_df["customer_state"].value_counts().head(10).reset_index()
    )
    state_counts.columns = ["customer_state", "jumlah_pelanggan"]

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ["#D7263D" if i == 0 else "#2E86AB" for i in range(len(state_counts))]
    ax.barh(state_counts["customer_state"][::-1], state_counts["jumlah_pelanggan"][::-1], color=colors[::-1])
    ax.set_xlabel("Jumlah Pelanggan")
    st.pyplot(fig)

with col2:
    st.markdown("**Top 10 Kota berdasarkan Jumlah Pelanggan**")
    city_counts = (
        filtered_df["customer_city"].value_counts().head(10).reset_index()
    )
    city_counts.columns = ["customer_city", "jumlah_pelanggan"]

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ["#D7263D" if i == 0 else "#2E86AB" for i in range(len(city_counts))]
    ax.barh(city_counts["customer_city"][::-1], city_counts["jumlah_pelanggan"][::-1], color=colors[::-1])
    ax.set_xlabel("Jumlah Pelanggan")
    st.pyplot(fig)

st.markdown("---")

# ============ PERTANYAAN 2 ============
st.subheader("Pertanyaan 2: Kesenjangan Konsentrasi Pelanggan Antar Region")

region_counts = main_df["customer_region"].value_counts().reset_index()
region_counts.columns = ["customer_region", "jumlah_pelanggan"]
region_counts["persentase"] = round(region_counts["jumlah_pelanggan"] / region_counts["jumlah_pelanggan"].sum() * 100, 2)

col1, col2 = st.columns([1, 1])
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors_region = ["#D7263D" if r == "Southeast" else "#B8C4CC" for r in region_counts["customer_region"]]
    explode = [0.06 if r == "Southeast" else 0 for r in region_counts["customer_region"]]
    ax.pie(
        region_counts["jumlah_pelanggan"],
        labels=region_counts["customer_region"],
        autopct="%1.1f%%",
        colors=colors_region,
        explode=explode,
        startangle=90,
    )
    ax.set_title("Proporsi Pelanggan per Region Brazil (seluruh data)")
    st.pyplot(fig)

with col2:
    st.markdown("**Tabel Proporsi Pelanggan per Region**")
    st.dataframe(region_counts, use_container_width=True)
    st.info(
        "Region **Southeast** mendominasi basis pelanggan Olist secara signifikan "
        "dibandingkan region lain, menunjukkan adanya kesenjangan penetrasi pasar antar wilayah."
    )

st.markdown("---")

# ============ GEOSPATIAL ANALYSIS ============
st.subheader("Analisis Lanjutan: Peta Sebaran Pelanggan (Geospatial)")

map_df = filtered_df.dropna(subset=["lat", "lng"])
if map_df.shape[0] > 5000:
    map_df = map_df.sample(n=5000, random_state=42)

if map_df.empty:
    st.warning("Tidak ada data koordinat untuk filter yang dipilih.")
else:
    m = folium.Map(location=[-15.78, -47.93], zoom_start=4, tiles="CartoDB positron")
    heat_data = list(zip(map_df["lat"], map_df["lng"]))
    HeatMap(heat_data, radius=8, blur=6).add_to(m)
    st_folium(m, width=1200, height=500)

st.caption("Dibuat untuk proyek akhir Belajar Analisis Data dengan Python — Dicoding.")