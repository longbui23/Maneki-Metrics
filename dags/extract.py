import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime, timedelta


#fetch sp500 companies
def fetch_sp500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})
    sp500_comp_df = pd.read_html(str(table))[0]
    sp500_comp_df.columns = sp500_comp_df.columns.str.replace('\n', ' ')
    
    return sp500_comp_df

def fetch_sp500_info():
    info = yFinance.info

#fetch stock data
def fetch_stock_data(sp500_comp_df):
    tickers = sp500_comp_df['Symbol'].tolist()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365*5)

    all_stock_data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(start=start_date, end=end_date)
        stock_data.reset_index(inplace=True)
        stock_data['Ticker'] = ticker

        all_stock_data.append(stock_data)

    combined_stock_data = pd.concat(all_stock_data, ignore_index=True)

    final_stock_data = combined_stock_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'Ticker']]
    final_stock_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits', 'ticker']

    print("Stock data successfully fetched and stored in DataFrame!")

    return final_stock_data

def change_stock_data(sp500_comp_df):
    tickers = sp500_comp_df['Symbol'].tolist()

    today = datetime.now().date()
    list = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        update_data = stock.history(start=today, end=today)
        list.append(update_data)
        
    return update_data

#fetch financial data
def track_stock_statistics(ticker_symbol, days_to_track):
    def get_stock_data(ticker_symbol, start_date, end_date):
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(start=start_date, end=end_date)
        financials = stock.financials
        
        eps = stock.info.get('trailingEps', None)
        pe_ratio = stock.info.get('trailingPE', None)
        
        if len(financials) >= 2:
            recent_revenue = financials.loc['Total Revenue'].iloc[0]
            previous_revenue = financials.loc['Total Revenue'].iloc[1]
            revenue_growth = ((recent_revenue - previous_revenue) / previous_revenue) * 100
        else:
            revenue_growth = None
        
        dividend_yield = stock.info.get('dividendYield', None)
        if dividend_yield:
            dividend_yield *= 100
        
        return {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'EPS': eps,
            'P/E Ratio': pe_ratio,
            'Revenue Growth (%)': revenue_growth,
            'Dividend Yield (%)': dividend_yield
        }
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_to_track)
    
    data = []
    current_date = start_date
    while current_date <= end_date:
        print(f"Fetching data for {current_date.strftime('%Y-%m-%d')}...")
        stock_data = get_stock_data(ticker_symbol, current_date, current_date + timedelta(days=1))
        data.append(stock_data)
        current_date += timedelta(days=1)
    
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    
    return df