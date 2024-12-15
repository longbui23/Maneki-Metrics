import numpy as np
import pandas as pd


##sp500

##stock
def cal_sma_ema_20(df_ticker):
    df_ticker['SMA_20'] = df_ticker.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).mean())
    df_ticker['EMA_20'] = df_ticker.groupby('Ticker')['Close'].transform(lambda x: x.ewm(span=20, adjust=False).mean())

    return df_ticker

def calculate_rsi(df_ticker):
    delta = df_ticker['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df_ticker['RSI'] = rsi

    return df_ticker

def calculate_macd(df_ticker, fast_period=12, slow_period=26, signal_period=9):
    fast_ema = df_ticker['Close'].ewm(span=12, adjust=False).mean()
    slow_ema = df_ticker['Close'].ewm(span=26, adjust=False).mean()
    df_ticker['MACD'] = fast_ema - slow_ema
    df_ticker['Signal'] =  df_ticker['MACD'].ewm(span=9, adjust=False).mean()

    return df_ticker


def calculate_bollinger_bands(df_ticker, window=20):
    df_ticker['middle_band'] = df_ticker['Close'].rolling(window=window).mean()
    df_ticker['std_dev'] = df_ticker['Close'].rolling(window=window).std()

    df_ticker['upper_band'] = df_ticker['middle_band'] + (df_ticker['std_dev'] * 2)
    df_ticker['lower_band'] = df_ticker['middle_band'] - (df_ticker['std_dev'] * 2)

    return df_ticker

def cal_all(df):
    grp = df.groupby('Ticker')

    result = grp.apply(lambda x: calculate_bollinger_bands(
        calculate_macd(
            calculate_rsi(
                cal_sma_ema_20(x)
            )
        )
    ))

    return result