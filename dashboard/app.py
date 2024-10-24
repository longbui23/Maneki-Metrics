import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Stock Data Visualization")

## Stock Selection
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

## Fetch Data
@st.cache_data
def load_data(ticker):
    data = pd.read_csv('../temp_analysis/data/stock_data_sp500.csv')
    data['Ticker'] = ticker
    return data

data = load_data(ticker)

if data.empty:
    st.error("No data available for the selected stock and date range.")
else:
    ## Display Raw Data
    st.subheader("Raw Data")
    st.dataframe(data.head())

    ## Candlestick Chart
    st.subheader("Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    ## Moving Averages
    st.subheader("Moving Averages")
    ma_periods = st.multiselect("Select MA periods", [10, 20, 50, 100, 200], default=[20, 50])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
    
    for period in ma_periods:
        ma_column = f'MA_{period}'
        data[ma_column] = data['Close'].rolling(window=period).mean()
        fig.add_trace(go.Scatter(x=data.index, y=data[ma_column], name=f'{period}-day MA'))
    
    fig.update_layout(title=f"{ticker} Stock Price with Moving Averages",
                      xaxis_title="Date",
                      yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

    ## Volume Chart
    st.subheader("Volume Chart")
    fig = go.Figure(data=[go.Bar(x=data.index, y=data['Volume'])])
    fig.update_layout(title=f"{ticker} Trading Volume",
                      xaxis_title="Date",
                      yaxis_title="Volume")
    st.plotly_chart(fig, use_container_width=True)

    ## Summary Statistics
    st.subheader("Summary Statistics")
    summary = data['Close'].describe()
    st.table(summary)