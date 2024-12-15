import pandas as pd
import json
import os
import boto3
import psycopg2


#connect with redshift
def conn_redshift():
    redshift_dw = boto3.resource(
        'redshift',
    
    )

    return redshift_dw

#connect to dynamoDB
def conn_dynamo():
    dynamodb = boto3.resource(
        'dynamodb',
    )

    return dynamodb

#connect with s3
def conn_s3():
    s3 = boto3.resource(
        's3',
    
    )
    return s3

#sp500
#insert sp500
def update_sp500(cur, df):
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO sp500 (symbol, Security, GICS_Sector, GICS_Sub_Industry, Location, CIK, Founded)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['Symbol'],
            row['Security'],
            row['GICS Sector'],
            row['GICS Sub-Industry'],
            row['Headquarters Location'],
            row['CIK'],
            row['Founded']
        )
        cur.execute(insert_query, values)

        delete_query = """
        DELETE FROM sp500 WHERE
        Symbol = %s
        """
        values =  (row['Symbol'])

        cur.execute(delete_query, values)
    
    cur.commit()


#insert stock table
def insert_stock_data(cur, df):
    
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

def insert_financial_data(cur, df):
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO finance  ()
        VALUES ('{df['']})
        """

        cur.execute(insert_query)

    cur.commit()