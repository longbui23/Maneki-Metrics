import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('Data/combined_financials.csv')
    df.set_index('Ticker', inplace=True)
    return df

df = load_data()

st.title('Financial Data by Ticker')

# Sidebar for ticker selection
ticker = st.sidebar.selectbox('Select a Ticker', df.index.unique())

if ticker:
    st.header(f'Financial Data for {ticker}')
    
    # Display the data for the selected ticker
    ticker_data = df.loc[ticker]
    
    # Convert to DataFrame if it's a Series (in case there's only one row for the ticker)
    if isinstance(ticker_data, pd.Series):
        ticker_data = ticker_data.to_frame().T
    
    # Display basic info
    st.subheader('Basic Information')
    basic_info = ticker_data[['Basic EPS', 'Diluted EPS', 'Net Income', 'Total Revenue']].T
    st.dataframe(basic_info)
    
    # Display profitability metrics
    st.subheader('Profitability Metrics')
    profitability = ticker_data[['Gross Profit', 'Operating Income', 'EBIT', 'EBITDA', 'Normalized EBITDA']].T
    st.dataframe(profitability)
    
    # Display balance sheet items
    st.subheader('Balance Sheet Items')
    balance_sheet = ticker_data[['Total Assets', 'Total Liabilities', 'Total Equity']].T
    st.dataframe(balance_sheet)
    
    # Display cash flow items
    st.subheader('Cash Flow Items')
    cash_flow = ticker_data[['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Free Cash Flow']].T
    st.dataframe(cash_flow)
    
    # Visualizations
    st.subheader('Visualizations')
    
    # Revenue vs Net Income
    st.bar_chart(ticker_data[['Total Revenue', 'Net Income']])
    
    # Profitability Ratios
    if 'Total Revenue' in ticker_data.columns and ticker_data['Total Revenue'].iloc[0] != 0:
        profit_margins = pd.DataFrame({
            'Gross Margin': ticker_data['Gross Profit'] / ticker_data['Total Revenue'],
            'Operating Margin': ticker_data['Operating Income'] / ticker_data['Total Revenue'],
            'Net Margin': ticker_data['Net Income'] / ticker_data['Total Revenue']
        })
        st.line_chart(profit_margins.T)

else:
    st.write('Please select a ticker from the sidebar to view its financial data.')