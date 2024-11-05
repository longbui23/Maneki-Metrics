import streamlit as st
import pandas as pd
import functions as fs
st.set_page_config(layout="wide")

# Streamlit app
def main():
    st.title("Stock Analysis Dashboard")
    
    # Add input for ticker symbol
    ticker = st.text_input("Enter stock ticker symbol:", "AAPL")
    
    # Add a button to load data
    if st.button("Load Data"):
        # Load data
        data = fs.load_data(ticker)

    # Load data
    data = fs.load_data("")

    # Display charts
    st.subheader("Candlestick Chart")
    st.plotly_chart(fs.create_candlestick_chart(data), use_container_width=True)

    st.subheader("Moving Averages")
    st.pyplot(fs.create_ma_chart(data))

    st.subheader("Relative Strength Index (RSI)")
    st.pyplot(fs.create_rsi_chart(data))

    st.subheader("Moving Average Convergence Divergence (MACD)")
    st.pyplot(fs.create_macd_chart(data))

    st.subheader("Bollinger Bands")
    st.pyplot(fs.create_bollinger_bands_chart(data))

if __name__ == "__main__":
    main()