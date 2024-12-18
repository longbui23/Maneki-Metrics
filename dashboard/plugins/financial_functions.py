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

#credentials
credentials = service_account.Credentials.from_service_account_file('gcp_key.json')
client = bigquery.Client(credentials=credentials)

# Fetch data
##balance_sheet
def fetch_balance_sheet_data(ticker):
    qury = f'''SELECT * FROM  axial-sight-443417-a6.sp500.balance_sheet_2024 WHERE string_field_0 = '{ticker}';'''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])

    return df

##income-statement
def fetch_income_stmt_data(ticker):
    qury = f'''SELECT * FROM  axial-sight-443417-a6.sp500.income_stmt_2024 WHERE string_field_0 = '{ticker}';'''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])

    return df

##cashflow
def fetch_cash_flow_sheet_data(ticker):
    qury = f'''SELECT * FROM  axial-sight-443417-a6.sp500.cash_flow_2024 WHERE symbol = '{ticker}';'''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])

    return df



#Balance-Sheet plots
def plot_table(df, title):
    df_index = df.reset_index()
    df_index.columns = ['Metrics', f'{title}']
    headers = list(df_index.columns)
    rows = df_index.values.tolist()

    # Create the table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=headers,
                    fill_color='lightblue',
                    align='center',
                    font=dict(size=14, color='black'),
                ),
                cells=dict(
                    values=[df_index[col] for col in df_index.columns],
                    fill_color='white',
                    align='center',
                    font=dict(size=12),
                )
            )
        ]
    )

    # Update layout with title
    fig.update_layout(title_text=title, title_x=0.5)
    return fig

## basic val
def key_balance_sheet_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = ['Net Debt', 'Total Debt'],
        y = df[['Net Debt', 'Total Debt']],
        marker=dict(color='blue'),
        name = df.columns[0]
    )) 

    fig.update_layout(
        title= f'Balance Sheet Key Metrics',
        xaxis_title='Metrics',
        yaxis_title='Amount (in billions)',
        template='plotly_white',
        xaxis=dict(tickangle=45),
        bargap=0.4,
    )

    return fig

## current asset vs liabilites
def plot_balance_sheet_items(items, title, y_title):
    fig = go.Figure()
    for item in items:
        fig.add_trace(go.Scatter(x=item.index, 
                                 y=item[item],
                                 mode='lines+markers',
                                 name=item))
    fig.update_layout(title=title,
                      xaxis_title='Year',
                      yaxis_title=y_title,
                      template='plotly_white',
                      legend=dict(title='Items'))
    
    return fig

##financial ratios
def plot_financial_ratio(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, 
                            y=df['Current Ratio'], 
                            mode='lines+markers', 
                            name='Current Ratio'))
    fig.add_trace(go.Scatter(x=df.index, 
                            y=df['Debt to Equity Ratio'], 
                            mode='lines+markers', 
                            name='Debt to Equity Ratio'))
    fig.update_layout(title='Apple Inc. - Financial Ratios',
                    xaxis_title='Year',
                    yaxis_title='Ratio',
                    template='plotly_white',
                    legend=dict(title='Ratios'))
    
    return fig