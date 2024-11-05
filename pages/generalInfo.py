import streamlit as st
import pandas as pd

def main():
    st.title("Stock Information Dashboard")

    # Add input for ticker symbol
    ticker = st.text_input("Enter stock ticker symbol:", "AAPL")

    # Load the data
    df = pd.read_csv("Data/sp500_companies.csv")
    df = df[df['Symbol'] == ticker]

    # Display the data in a table
    st.subheader("Stock Information Table")
    st.dataframe(df)

    # Allow users to select a specific stock
    selected_stock = st.selectbox("Select a stock for more details:", df['Symbol'].tolist())

    # Display detailed information for the selected stock
    if selected_stock:
        st.subheader(f"Detailed Information for {selected_stock}")
        stock_info = df[df['Symbol'] == selected_stock].iloc[0]
        for column in df.columns:
            st.write(f"**{column}:** {stock_info[column]}")

        # Fetch real-time stock price (this requires internet connection)
        try:
            stock = yf.Ticker(selected_stock)
            current_price = stock.info['regularMarketPrice']
            st.write(f"**Current Price:** ${current_price:.2f}")
        except:
            st.write("Unable to fetch current price. Please check your internet connection.")

if __name__ == "__main__":
    main()