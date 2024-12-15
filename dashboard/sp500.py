import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plugins.functions as fs  # Custom local module

st.set_page_config(page_title="Makeni.net", layout="wide", page_icon="🐱")


def main():
    # Styling CSS
    with open("styling/general.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Page Title
    st.markdown('<h1 class="title">📈 Makeni Metrics: SP500 Stock Dashboard</h1>', unsafe_allow_html=True)

    # Data Loading
    df = fs.load_sp500()
    df_today = fs.load_stock_data(ticker=None, today=1)

    # Navigation Buttons in a Container 
    with st.container() as c1:

        st.markdown("### Navigation")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Stock Dashboard"):
                st.experimental_set_query_params(page="Stock.py")
        with col2:
            if st.button("💬 Chat Bot"):
                st.experimental_set_query_params(page="MakeniTalks.py")
        with col3:
            if st.button("🏢 Company Info"):
                st.experimental_set_query_params(page="company.py")


    # Market Overview in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("📈 Market Overview")
        col1, col2, col3 = st.columns(3)

        daily_change = f"{round(df['Close'].pct_change().iloc[-1] * 100, 2)}%"
        col1.markdown(f"""
        <div class="metric-card">
            <h3><center>Current Value</center></h3>
            <p>${round(df['Close'].iloc[-1], 0)}</p>
            <span>{daily_change}</span>
        </div>
        """, unsafe_allow_html=True)

        daily_volume_change = f"{round(df['Volume'].pct_change().iloc[-1] * 100, 2)}%"
        col2.markdown(f"""
        <div class="metric-card">
            <h3><center>Total Volume</center></h3>
            <p>{df['Volume'].iloc[-1]:,.0f}</p>
            <span>{daily_volume_change}</span>
        </div>
        """, unsafe_allow_html=True)

        overbought = sum(df_today['Close'] > df_today['Upper_Band'].fillna(0))
        col3.markdown(f"""
        <div class="metric-card">
            <h3><center>Overbought</center></h3>
            <p>{overbought}</p>
            <span>-</span>
        </div>
        """, unsafe_allow_html=True)

    # Stock Metrics in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("📊 Stock Metrics")
        col1, col2, col3 = st.columns(3)

        # Maximum Stock
        max_stock = df_today[df_today['Close'] == df_today['Close'].max()]
        stock_price_max = round(max_stock['Close'].values[0], 0)
        stock_name_max = max_stock['Ticker'].values[0]
        col1.markdown(f"""
            <div class="metric-card">
                <h3><center>Highest Stock Close Price</center></h3>
                <p>${stock_price_max}</p>
                <span>{stock_name_max}</span>
            </div>
            """, unsafe_allow_html=True)

        # Minimum Stock
        min_stock = df_today[df_today['Close'] == df_today['Close'].min()]
        stock_price_min = round(min_stock['Close'].values[0], 0)
        stock_name_min = min_stock['Ticker'].values[0]
        col2.markdown(f"""
            <div class="metric-card">
                <h3><center>Lowest Stock Close Price</center></h3>
                <p>${stock_price_min}</p>
                <span>{stock_name_min}</span>
            </div>
            """, unsafe_allow_html=True)

        # Oversold Stocks
        oversold = sum(df_today['Close'] < df_today['Lower_Band'].fillna(0))
        col3.markdown(f"""
            <div class="metric-card">
                <h3><center>Oversold Stocks<center></h3>
                <p>{oversold}</p>
                <span>-</span>
            </div>
            """, unsafe_allow_html=True)

    # Investment Trends in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("📈 Investment Trends")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Close'], name='Close Price',
                       line=dict(color='blue', width=2)))
        fig.update_layout(
            title="S&P 500 Intraday Chart",
            xaxis_title="Time",
            yaxis_title="Price",
            template="plotly_white",
            plot_bgcolor="rgba(240, 240, 240, 1)",
            paper_bgcolor="rgba(245, 245, 245, 1)",
            xaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.5)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.5)")
        )
        st.plotly_chart(fig, use_container_width=True)

    # News Section in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("📰 Latest News")
        news_items = fs.fetch_news("^GPSC")
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


if __name__ == "__main__":
    main()
