# Packages
## Data Processing
import pandas as pd

## Local Packages
import plugins.stock_functions as fs
import plugins.cloud_connection as cc

## Visualization
import plotly.graph_objects as go
import streamlit as st

# Custom CSS for Styling

st.set_page_config(page_title="Makeni.net", layout="wide", page_icon="🐱")

# Styling CSS
with open("dashboard/styling/stock.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#connect to cloud
bigquery_client = cc.connect_bigquery()

# Data-loader
df_sp500 = fs.fetch_company(bigquery_client)

# Sidebar for settings
st.sidebar.header("Dashboard Settings")
selected_stock = st.sidebar.selectbox("Select Stock", df_sp500['Symbol'])
timeframe = st.sidebar.radio("Select Timeframe", ['1D', '1W', '1M'])

# Filter stock
df_filtered = fs.load_stock_data(bigquery_client, selected_stock)

# Row 1: Stock Metrics
with st.container():
    st.subheader("📊 Stock Overview")
    col1, col2 = st.columns(2)
    daily_change = f"{round(df_filtered['Close'].pct_change().iloc[-1] * 100, 2)}%"
    col1.metric(
        "📈 Current Price", 
        f"${df_filtered['Close'].iloc[-1]:.2f}", 
        delta=daily_change, 
        delta_color='normal'
    )

    daily_change = f"{round(df_filtered['Volume'].pct_change().iloc[-1] * 100, 2)}%"
    col2.metric(
        "📉 Volume", 
        f"{df_filtered['Volume'].iloc[-1]:,.0f}",  
        delta=daily_change, 
        delta_color='normal'
    )

# Row 2: Candlestick Chart
st.subheader("📈 Candlestick Chart with Bollinger Band")
st.plotly_chart(fs.create_candlestick_chart(df_filtered), use_container_width=True)

# Row 3: EMA & SMA
st.subheader("📊 Moving Averages")
st.plotly_chart(fs.create_ma_chart(df_filtered))

# Row 4: RSI
st.subheader("📈 Relative Strength Index (RSI)")
st.plotly_chart(fs.create_rsi_chart(df_filtered))

# Row 5: MACD
st.subheader("📉 Moving Average Convergence Divergence (MACD)")
st.plotly_chart(fs.create_macd_chart(df_filtered))

# News and Watchlist
with st.container():
    st.subheader("📜 Watchlist & News")
    col1, col2 = st.columns(2)
    
    # Watchlist
    with col1:
        df_companies= fs.load_companies_data(bigquery_client)
        industry = df_companies[df_companies['Symbol']==selected_stock]['GICS Sector'].values[0]
        stock_lst = df_companies[df_companies['GICS Sector']==industry]['Symbol'].tolist()

        st.write("### ⭐ Watchlist")
        for stck in stock_lst:
            emj = fs.generate_random_emoji_text()
            st.markdown(f"{emj} {stck}")
    
    # Latest News
    with col2:
        st.write("### 📰 Latest News")
        news_items = fs.fetch_news(selected_stock)
        for news in news_items:
            title = news['title']
            summary = news['summary']
            url = news['url']
            st.markdown(f"""
                <div class="news-card">
                    <h4>{title}</h4>
                    <p>{summary}</p>
                    <a href="{url}" target="_blank">Read More</a>
                </div>
                """, unsafe_allow_html=True)
