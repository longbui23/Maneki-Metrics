#packages
##data processing
import yfinance as yf
import datetime as dt
import pandas as pd

##visualizations
import streamlit as st

import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

#cloud
import boto3 #AWS
import io
import certifi
import urllib

from google.oauth2 import service_account #GCP
from google.cloud import bigquery 

from pymongo.mongo_client import MongoClient #MongoDB
from pymongo.server_api import ServerApi
    
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

#credentials = service_account.Credentials.from_service_account_file('gcp_key.json')
client = bigquery.Client(credentials=credentials)

ca = certifi.where()
uri = f"mongodb+srv://longb8186:longlong32@sp500comp.rnqta.mongodb.net/?retryWrites=true&w=majority&appName=SP500comp"

# Create a new client and connect to the server
mongo_client = MongoClient(uri, tlsCAFile=ca)

#fetch data mongodb
#def fetch_news(ticker):
    #db = mongo_client['sp500']
    #collection = db['news']

    #all_news = collection.find_one({'Symbol':ticker})


# Function to load data sp500
def load_sp500():
    qury = '''
        SELECT * FROM  axial-sight-443417-a6.sp500.sp500_market_history
    '''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw]).sort_values(by='Date')

    return df

def fetch_sp500():
    qury = '''
        SELECT DISTINCT Symbol FROM axial-sight-443417-a6.sp500.companies
    '''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])

    return df

def load_stock_data(ticker, today=None):
    if today == None:
        qury = f'''
            SELECT * FROM  axial-sight-443417-a6.sp500.stock_historical WHERE Ticker = '{ticker}'
        '''
    else:
        qury = f'''
            SELECT * FROM  axial-sight-443417-a6.sp500.stock_historical
            WHERE DATE =  (SELECT MAX(DATE) FROM axial-sight-443417-a6.sp500.stock_historical)
        '''

    query_job = client.query(qury)
    rows_raw = query_job.result()

    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', ascending=True, inplace=True)

    return df

# Function to create candlestick chart
def create_candlestick_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name = 'Candle'
    ))

    #fig.add_trace(go.Scatter(x=data['Date'], y=data['Upper_Band'], name='Upper Band', line=dict(color='grey', dash='dot')))
    #fig.add_trace(go.Scatter(x=data['Date'], y=data['Lower_Band'], name='Lower Band', line=dict(color='grey', dash='dot')))

    fig.update_layout(
        title='Stock Price',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=True
    )

    return fig

# Function to create SMA and EMA chart
def create_ma_chart(data):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['SMA_20'], name='20-Day SMA', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['EMA_20'], name='20-Day EMA', line=dict(color='green')))
    
    fig.update_layout(
        title = 'Close Price with 20-Day SMA and EMA',
        xaxis_title = 'Date',
        yaxis_title= 'Price (USD)',
    )

    return fig


# Function to create RSI chart
def create_rsi_chart(data):
    fig = go.Figure()

    # Add RSI line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='purple')
    ))

    # Add overbought line
    fig.add_trace(go.Scatter(
        x=[data['Date'].iloc[0], data['Date'].iloc[-1]],
        y=[70, 70],
        mode='lines',
        name='Overbought (70)',
        line=dict(color='red', dash='dash')
    ))

    # Add oversold line
    fig.add_trace(go.Scatter(
        x=[data['Date'].iloc[0], data['Date'].iloc[-1]],
        y=[30, 30],
        mode='lines',
        name='Oversold (30)',
        line=dict(color='green', dash='dash')
    ))

    # Update layout
    fig.update_layout(
        title='Relative Strength Index (RSI)',
        xaxis_title='Date',
        yaxis_title='RSI',
        yaxis=dict(range=[0, 100]),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig

# Function to create MACD chart
def create_macd_chart(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], name="MACD", line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Signal'], name="Signal Line", line=dict(color='blue')))

    data['Histogram'] = data['MACD'] - data['Signal']
    fig.add_trace(go.Bar(x=data['Date'], y=data['Histogram'], name="Histogram", marker_color='gray', opacity=0.3), secondary_y=True)

    # Set figure layout
    fig.update_layout(
        title_text="MACD",
        xaxis_title="Date",
        yaxis_title="MACD",
        legend=dict(x=0, y=1, orientation="h"),
        hovermode="x unified"
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="MACD", secondary_y=False)
    fig.update_yaxes(title_text="Histogram", secondary_y=True)

    return fig

# Function to create Bollinger Bands chart
def create_bollinger_bands_chart(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Date'], data['Close'], label='Close', color='blue')
    ax.plot(data['Date'], data['Upper_Band'], label='Upper Band', color='red', linestyle='--')
    ax.plot(data['Date'], data['Middle_Band'], label='Middle Band', color='green', linestyle='-')
    ax.plot(data['Date'], data['Lower_Band'], label='Lower Band', color='red', linestyle='--')
    ax.fill_between(data['Date'], data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.1)
    
    ax.set_title('Bollinger Bands')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    ax.grid(True)
    plt.tight_layout()

    return fig


#Function to create stock returns histogram
def plot_histogram(df):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(x=df['Log_Returns'],
                     name='Histogram')
    )

    fig.update_layout(
         title='Log Returns Distribution',
    xaxis_title='Log Returns',
    yaxis_title='Frequency',
    width=1000,
    height=600
    )

    return fig

#fetch the latest news for sp500
def fetch_news(ticker):
    ticker = yf.Ticker(ticker)
    news = ticker.news

    latest_news = []
    for article in news[:5]:  # Limit to 5 articles
        title = article.get("title", "No Title")
        summary = article.get("publisher", "No Summary Provided")
        link = article.get("link", "#")
        image = article.get("thumbnail", {}).get("resolutions", [{}])[0].get("url", None)

        # Append formatted news data to the list
        latest_news.append({
            "title": title,
            "summary": summary,
            "url": link,
            "image": image
        })

    return latest_news