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

        # Create two columns for the upper row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Candlestick Chart")
            st.plotly_chart(fs.create_candlestick_chart(data), use_container_width=True)

        with col2:
            st.subheader("Moving Averages")
            st.pyplot(fs.create_ma_chart(data))

        with col3:
            st.subheader("Relative Strength Index (RSI)")
            st.pyplot(fs.create_rsi_chart(data))

        # Create two columns for the lower row
        col4, col5 = st.columns(2)

        with col4:
            st.subheader("Moving Average Convergence Divergence (MACD)")
            st.pyplot(fs.create_macd_chart(data))

        with col5:
            st.subheader("Bollinger Bands")
            st.pyplot(fs.create_bollinger_bands_chart(data))

if __name__ == "__main__":
    main()