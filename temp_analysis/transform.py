#technical indicators
def sma(data, period=20):
    """Calculate Simple Moving Average"""
    return data['Close'].rolling(window=period).mean()

def ema(data, period=20):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period, adjust=False).mean()

def rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(data, fast_period=12, slow_period=26, signal_period=9):
    """Calculate MACD, Signal Line, and MACD Histogram"""
    ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def bollinger_bands(data, period=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = data['Close'].rolling(window=period).mean()
    std = data['Close'].rolling(window=period).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band


import pandas as pd

df = pd.read_csv('data/stock_data_sp500.csv')

new_df = pd.DataFrame()

new_df['Ticker'] = df['Ticker']

#technical indicators
def sma(data, period=20):
    """Calculate Simple Moving Average"""
    return data['Close'].mean()

def ema(data, period=20):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period, adjust=False).mean()

def rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(data, fast_period=12, slow_period=26, signal_period=9):
    """Calculate MACD, Signal Line, and MACD Histogram"""
    ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def bollinger_bands(data, period=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = data['Close'].mean()
    std = data['Close'].std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band


import pandas as pd

df = pd.read_csv('data/stock_data_sp500.csv')

new_df = pd.DataFrame()

new_df['Ticker'] = df['Ticker']

def calculate_indicators(stock_data):
    close_prices = stock_data['Close']
    
    sma_20 = sma(close_prices, 20).iloc[-1]
    ema_20 = ema(close_prices, 20).iloc[-1]
    rsi_14 = rsi(close_prices, 14).iloc[-1]
    macd_line, signal_line, _ = macd(close_prices)
    macd_value = macd_line.iloc[-1]
    signal_value = signal_line.iloc[-1]
    upper, middle, lower = bollinger_bands(close_prices)
    
    return {
        'SMA_20': sma_20,
        'EMA_20': ema_20,
        'RSI_14': rsi_14,
        'MACD': macd_value,
        'Signal': signal_value,
        'BB_Upper': upper.iloc[-1],
        'BB_Middle': middle.iloc[-1],
        'BB_Lower': lower.iloc[-1]
    }