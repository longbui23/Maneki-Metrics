import numpy as np
import pandas as pd
import requests
import json
import yfinance as yf
from datetime import datetime, timedelta
#import fredapi
import yfinance as yf
from datetime import datetime, timedelta

# Set up FRED API
#fred = fredapi.Fred(api_key='YOUR_FRED_API_KEY')

#functions
#stock data
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)[0]
    return table['Symbol'].tolist()

def stock_data_sp500(ticker):
    '''get stock in s&p500'''

    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)

    stock_data = pd.DataFrame()
    stock_data['Ticker'] = ticker

    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)
    

    return stock_data

#market data
def get_sector_performance():
    """
    Retrieves the performance of various market sectors.

    Returns:
    dict: A dictionary with sector tickers as keys and their performance as values.
    """
    sectors = ["XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLC", "XLU"]
    sector_performance = {}

    for sector in sectors:
        ticker = yf.Ticker(sector)
        performance = ticker.info

    return sector_performance


def get_stock_data(ticker):
    """
    Fetch and calculate various stock metrics for a given ticker symbol and date range.

    Args:
    ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
    
    Returns:
    dict: A dictionary containing various stock metrics
    """
    #datetime
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    
    # Create a Ticker object for the given symbol
    stock = yf.Ticker(ticker)
    
    # Fetch historical market data for the specified date range
    hist = stock.history(start=start_date, end=end_date)
    
    # Fetch financial data (income statement)
    financials = stock.financials
    
    # Extract Earnings Per Share (EPS) from stock info
    eps = stock.info.get('trailingEps', None)
    
    # Extract Price to Earnings (P/E) ratio from stock info
    pe_ratio = stock.info.get('trailingPE', None)
    
    # Calculate year-over-year revenue growth
    if len(financials) >= 2:
        recent_revenue = financials.loc['Total Revenue'].iloc[0]
        previous_revenue = financials.loc['Total Revenue'].iloc[1]
        revenue_growth = ((recent_revenue - previous_revenue) / previous_revenue) * 100
    else:
        revenue_growth = None
    
    # Get dividend yield and convert to percentage
    dividend_yield = stock.info.get('dividendYield', None)
    if dividend_yield:
        dividend_yield *= 100
    
    # Return a dictionary with all calculated metrics
    return {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'EPS': eps,
        'P/E Ratio': pe_ratio,
        'Revenue Growth (%)': revenue_growth,
        'Dividend Yield (%)': dividend_yield
    }

def fetch_macroeconomic_indicators(start_date, end_date=None):
    """
    Fetch macroeconomic indicators from FRED.
    
    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str, optional): End date in 'YYYY-MM-DD' format. Defaults to current date.
    
    Returns:
    pandas.DataFrame: DataFrame containing the macroeconomic indicators.
    """
    
    # Convert start_date to datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Set end_date to current date if not provided
    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Define the indicators and their FRED codes
    indicators = {
        'fed_funds_rate': 'FEDFUNDS',
        'cpi': 'CPIAUCSL',
        'unemployment_rate': 'UNRATE',
        'gdp_growth': 'A191RL1Q225SBEA'
    }

    # Fetch data for each indicator
    data = {}
    for name, code in indicators.items():
        data[name] = pdr.get_data_fred(code, start_date, end_date)

    # Combine all indicators into a single DataFrame
    df = pd.concat(data.values(), axis=1, keys=data.keys())

    # Reset index to make date a column
    df.reset_index(inplace=True)

    # Rename columns
    df.columns.name = None
    df.columns = ['date'] + list(indicators.keys())

    # Add an ID column
    df.insert(0, 'id', range(1, len(df) + 1))

    return df

tickers = get_sp500_tickers()
all_tickers_df = []

for ticker in tickers:
    stock_data = get_stock_data(ticker)
    all_tickers_df.append(stock_data)    
    
print(all_tickers_df)
    
    

