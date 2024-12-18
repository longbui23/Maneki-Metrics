import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plugins.market_plot as mp 
import plugins.cloud_connection as cc

st.set_page_config(page_title="Makeni.net", layout="wide", page_icon="🐱")

def main():
    #cloud connection
    bigquery_client =cc.connect_bigquery()
    
    # Styling CSS
    with open("../styling/general.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Page Title
    st.markdown('<h1 class="title">📈 Makeni Metrics: SP500 Stock Real Time Dashboard</h1>', unsafe_allow_html=True)

    # Data Loading
    df = mp.load_sp500(bigquery_client)
    df_today = mp.load_today_data(bigquery_client)
    company_df = mp.load_companies_data(bigquery_client)

    sector_symbol = {
        "Information Technology": "XLK",
        "Financials": "XLF",
        "Healthcare": "XLV",
        "Energy": "XLE",
        "Consumer Discretionary": "XLY",
        "Consumer Staples": "XLP",
        "Utilities": "XLU",
        "Industrials": "XLI",
        "Real Estate": "XLRE",
        "Materials": "XLB",
        "Communication Services": "XLC"
    }

    # Navigation Buttons in a Container 
    with st.container() as c1:
        st.markdown("### Navigation Bar")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("📈 Market Dashboard"):
                st.experimental_set_query_params(page="../pages/stock.py")
        with col2:
            if st.button("📊 Stock Dashboard"):
                st.experimental_set_query_params(page="../pages/stock.py")
        with col3:
            if st.button("💬 Talk with Makeni AI"):
                st.experimental_set_query_params(page="../pages/MakeniTalks.py")
        with col4:
            if st.button("🏢 Company Financial Portfolio"):
                st.experimental_set_query_params(page="../pages/company.py")
        with col5:
            if st.button("🏢 Stock Prediction"):
                st.experimental_set_query_params(page="../stock_prediction.py")


    # Market Overview in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("🏛️ Market Overview")
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
        st.subheader("📈 Today Stock Trends")
        col1, col2 = st.columns([2,1])
        #Divided by Sector
        with col1:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            switch_state = st.toggle("Number of Companies/Volume", key="companies_volume_toggle")
            if not switch_state:
                st.plotly_chart(mp.sector_trend(company_df))
            else:
                merge_df = pd.merge(df_today, company_df, left_on='Ticker', right_on='Symbol', how='inner')
                st.plotly_chart(mp.sector_volume(merge_df))
        #Market Overall Performance
        with col2:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            with st.container():
                st.plotly_chart(mp.investment_trend(df))
            with st.container():
                st.plotly_chart(mp.candlestick_chart(df))

    #Divided by Sector
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("💹 Sector Breakdown")
        option = st.selectbox(
            f"Sector to analyze?",company_df['GICS Sector'].unique())
        df_filtered = company_df[company_df["GICS Sector"]==option]
        
        col1, col2 = st.columns([1,2])
        
        #pie chart for subindustry
        with col1:
            st.plotly_chart(mp.gauge_sector(sector_symbol[option]))
            st.plotly_chart(mp.subindustry_trend(df_filtered))
        with col2:
            filtered_merge_df = pd.merge(df_today, df_filtered, left_on='Ticker', right_on='Symbol', how='inner')
            st.plotly_chart(mp.subindustry_volume(filtered_merge_df))
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(mp.companies_volumes(filtered_merge_df))
            with col2:
                temp_df = filtered_merge_df[['Security','Close']]
                temp_df['Close'] = round(temp_df['Close'],0)
                st.plotly_chart(mp.table_map(temp_df))

    # News Section in a Container
    with st.container():
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("📰 Latest News")
        news_items = mp.fetch_news("^GPSC")
        for news in news_items:
            title = news['title']
            summary = news['summary']
            url = news['url']
            image = news['image']
            st.markdown(f"""
                <div class="news-card">
                    <h4>{title}</h4>
                    <p>{summary}</p>
                    <a href="{url}" target="_blank">Read More</a>
                    <img src="{image} alt='New Image' class='new-images'/>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
