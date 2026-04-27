import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# ==============================
# Title
# ==============================
st.title("🚴 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan waktu dan cuaca")

# ==============================
# Sidebar Filter
# ==============================
st.sidebar.header("Filter")

min_date = df['dteday'].min()
max_date = df['dteday'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date]
)

filtered_df = df[
    (df['dteday'] >= pd.to_datetime(date_range[0])) &
    (df['dteday'] <= pd.to_datetime(date_range[1]))
]

# ==============================
# Metrics
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df['cnt'].sum()))
col2.metric("Average Rentals", int(filtered_df['cnt'].mean()))
col3.metric("Max Rentals", int(filtered_df['cnt'].max()))

# ==============================
# Monthly Trend
# ==============================
st.subheader("📈 Monthly Rental Trend")

filtered_df['month'] = filtered_df['dteday'].dt.to_period('M')
monthly_trend = filtered_df.groupby('month')['cnt'].sum()

st.line_chart(monthly_trend)

# ==============================
# Weather Analysis
# ==============================
st.subheader("🌦️ Rental by Weather Condition")

weather_trend = filtered_df.groupby('weathersit')['cnt'].mean()

fig, ax = plt.subplots()
sns.barplot(
    x=weather_trend.index,
    y=weather_trend.values,
    ax=ax
)

ax.set_xlabel("Weather")
ax.set_ylabel("Average Rentals")

st.pyplot(fig)

# ==============================
# Raw Data (optional)
# ==============================
st.subheader("📄 Raw Data")
st.dataframe(filtered_df.head())