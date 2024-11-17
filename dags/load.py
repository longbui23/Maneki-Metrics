import pandas as pd
import psycopg2
import os
from psycopg2 import sql


# Database connection parameters
db_params = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': os.environ.get('DB_PORT', 5432)
}

#connect with sql server
def conn_db():
    conn = psycopg2.connect(
        **db_params
    )

    cur = conn.cursor()

    return cur

def create_stock_table(cur, df):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS stock_data (
        date DATE,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        dividends FLOAT,
        stock_splits FLOAT,
        ticker VARCHAR(10),
        SMA_20 FLOAT,
        EMA_20 FLOAT,
        RSI FLOAT,
        MACD FLOAT,
        Signal FLOAT,
        middle_band FLOAT,
        std_dev FLOAT,
        upper_band FLOAT,
        lower_band FLOAT
    )
    """
    cur.execute(create_table_query)
    
    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO stock_data (date, open, high, low, close, volume, dividends, stock_splits, ticker, 
                                SMA_20, EMA_20, RSI, MACD, Signal, middle_band, std_dev, upper_band, lower_band)
        VALUES ('{row['date']}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {row['volume']}, 
                {row['dividends']}, {row['stock_splits']}, '{row['ticker']}', {row['SMA_20']}, {row['EMA_20']}, 
                {row['RSI']}, {row['MACD']}, {row['Signal']}, {row['middle_band']}, {row['std_dev']}, 
                {row['upper_band']}, {row['lower_band']})
        """
        cur.execute(insert_query)

    cur.commit()


def create_sp500(cur, df):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sp500 (
        date DATE,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        dividends FLOAT,
        stock_splits FLOAT,
        ticker VARCHAR(10),
        SMA_20 FLOAT,
        EMA_20 FLOAT,
        RSI FLOAT,
        MACD FLOAT,
        Signal FLOAT,
        middle_band FLOAT,
        std_dev FLOAT,
        upper_band FLOAT,
        lower_band FLOAT
    )
    """
    cur.execute(create_table_query)
    
    # Insert data
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO stock_data (date, open, high, low, close, volume, dividends, stock_splits, ticker, 
                                SMA_20, EMA_20, RSI, MACD, Signal, middle_band, std_dev, upper_band, lower_band)
        VALUES ('{row['date']}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {row['volume']}, 
                {row['dividends']}, {row['stock_splits']}, '{row['ticker']}', {row['SMA_20']}, {row['EMA_20']}, 
                {row['RSI']}, {row['MACD']}, {row['Signal']}, {row['middle_band']}, {row['std_dev']}, 
                {row['upper_band']}, {row['lower_band']})
        """
        cur.execute(insert_query)

    cur.commit()

    def create_finance(cur, df):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS finance (
            date DATE,
        )
        """
        cur.execute(create_table_query)
        
        # Insert data
        for _, row in df.iterrows():
            insert_query = f"""
            INSERT INTO finance  ()
            VALUES ('{df['']})
            """
            cur.execute(insert_query)

        cur.commit()