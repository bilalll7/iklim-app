import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Perubahan Iklim",
    layout="wide"
)


st.title("Dashboard Analisis Perubahan Iklim")
st.markdown(
    "Dashboard ini menyajikan visualisasi dan analisis data perubahan iklim "
    "untuk mendukung pengambilan keputusan berbasis data."
)

# =========================
# LOAD & PREPARE DATA
# =========================
df = pd.read_csv("climate_change_dataset.csv")
df = df.dropna()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter Data")

selected_country = st.sidebar.multiselect(
    "Pilih Negara",
    options=sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())[:5]
)

year_range = st.sidebar.slider(
    "Pilih Rentang Tahun",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

df_filtered = df[
    (df["Country"].isin(selected_country)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# =========================
# KPI
# =========================
st.subheader("Key Performance Indicators (KPI)")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Rata-rata Suhu (°C)",
    round(df_filtered["Avg Temperature (°C)"].mean(), 2)
)

kpi2.metric(
    "Rata-rata Emisi CO₂",
    round(df_filtered["CO2 Emissions (Tons/Capita)"].mean(), 2)
)

kpi3.metric(
    "Rata-rata Cuaca Ekstrem",
    round(df_filtered["Extreme Weather Events"].mean(), 2)
)

# =========================
# AGREGASI TAHUNAN
# =========================
df_yearly = (
    df_filtered
    .groupby("Year")
    .mean(numeric_only=True)
    .reset_index()
)

# =========================
# VISUALISASI
# =========================
col_left, col_right = st.columns(2)

# ----- LINE CHART -----
with col_left:
    st.subheader("Tren Emisi CO₂ dan Suhu")

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(df_yearly["Year"], df_yearly["CO2 Emissions (Tons/Capita)"], label="CO₂ Emissions")
    ax1.plot(df_yearly["Year"], df_yearly["Avg Temperature (°C)"], label="Avg Temperature")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Value")
    ax1.legend()

    st.pyplot(fig1)

# ----- BAR CHART -----
with col_right:
    st.subheader("Perbandingan Emisi CO₂ Antar Negara")

    country_emission = (
        df_filtered
        .groupby("Country")["CO2 Emissions (Tons/Capita)"]
        .mean()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    country_emission.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Country")
    ax2.set_ylabel("CO₂ Emissions")

    st.pyplot(fig2)

# =========================
# BARIS KEDUA
# =========================
col_left2, col_right2 = st.columns(2)

# ----- SCATTER PLOT -----
with col_left2:
    st.subheader("Hubungan Emisi CO₂ dan Suhu")

    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.scatter(
        df_filtered["CO2 Emissions (Tons/Capita)"],
        df_filtered["Avg Temperature (°C)"]
    )
    ax3.set_xlabel("CO₂ Emissions")
    ax3.set_ylabel("Avg Temperature (°C)")

    st.pyplot(fig3)

# ----- BOXPLOT -----
with col_right2:
    st.subheader("Distribusi Cuaca Ekstrem")

    fig4, ax4 = plt.subplots(figsize=(4, 4))
    ax4.boxplot(df_filtered["Extreme Weather Events"])
    ax4.set_ylabel("Jumlah Kejadian")

    st.pyplot(fig4)

# =========================
# TABEL DATA
# =========================
st.subheader("Data yang Digunakan")
st.dataframe(df_filtered)
