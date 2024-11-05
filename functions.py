import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Function to load data
def load_data(ticker, start_date, end_date):
    df = pd.read_csv("Data/all_stock_data.csv")
    df = df[df['Tickers'] == ticker]
    return df

# Function to create candlestick chart
def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(
        title='Stock Price',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )
    return fig

# Function to create SMA and EMA chart
def create_ma_chart(data):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Close Price', color='blue')
    ax.plot(data.index, data['SMA_20'], label='20-Day SMA', color='red')
    ax.plot(data.index, data['EMA_20'], label='20-Day EMA', color='green')
    
    ax.set_title('Close Price with 20-Day SMA and EMA')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

# Function to create RSI chart
def create_rsi_chart(data):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['RSI'], label='RSI', color='purple')
    ax.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    
    ax.set_title('Relative Strength Index (RSI)')
    ax.set_xlabel('Date')
    ax.set_ylabel('RSI')
    ax.legend()
    ax.grid(True)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    return fig

# Function to create MACD chart
def create_macd_chart(data):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['MACD'], label='MACD', color='blue')
    ax.plot(data.index, data['Signal'], label='Signal Line', color='red')
    ax.bar(data.index, data['Histogram'], label='Histogram', color='gray', alpha=0.3)
    
    ax.set_title('MACD')
    ax.set_xlabel('Date')
    ax.set_ylabel('MACD')
    ax.legend(loc='upper left')
    ax.grid(True)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    return fig

# Function to create Bollinger Bands chart
def create_bollinger_bands_chart(data):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Close', color='blue')
    ax.plot(data.index, data['Upper_Band'], label='Upper Band', color='red', linestyle='--')
    ax.plot(data.index, data['Middle_Band'], label='Middle Band', color='green', linestyle='-')
    ax.plot(data.index, data['Lower_Band'], label='Lower Band', color='red', linestyle='--')
    ax.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.1)
    
    ax.set_title('Bollinger Bands')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    ax.grid(True)
    plt.tight_layout()
    return fig