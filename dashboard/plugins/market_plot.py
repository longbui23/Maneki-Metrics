import pandas as pd
import yfinance as yf

import matplotlib.pyplot as plt
import plotly.graph_objects as go


#fetch data
# Function to load data sp500
def load_sp500(client):
    qury = '''
        SELECT * FROM  axial-sight-443417-a6.sp500.sp500_market_history
    '''

    query_job = client.query(qury)
    rows_raw = query_job.result()
    df = pd.DataFrame.from_records([dict(row) for row in rows_raw]).sort_values(by='Date')

    return df

def load_today_data(client):
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

#load companies
def load_companies_data(client):
    qury = f'''
        SELECT * FROM  axial-sight-443417-a6.sp500.companies
    '''

    query_job = client.query(qury)
    rows_raw = query_job.result()

    df = pd.DataFrame.from_records([dict(row) for row in rows_raw])

    return df

#plot market trend
def investment_trend(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Close'], name='Close Price',
                    line=dict(color='blue', width=2), yaxis='y1'))
    fig.add_trace(
        go.Bar(x=df['Date'], y=df['Volume'], name='Volume', 
                   marker=dict(color='rgba(128,128,128,0.4)'), yaxis='y2')
    )
    fig.update_layout(
        title="S&P 500 Intraday Chart",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.5)"),
        yaxis=dict(title="Close Price", showgrid=True, gridcolor="rgba(200, 200, 200, 0.5)"),
        yaxis2=dict(title="Volume", overlaying="y", side="right",showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height = 300,
    )
    
    return fig

#plot candlestick chart for entire market
def candlestick_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['Date'],  
        open=df['Open'],  
        high=df['High'],  
        low=df['Low'],  
        close=df['Close'],  
        increasing_line_color='green',  
        decreasing_line_color='red',
    ))

    fig.update_layout(
        title='Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        plot_bgcolor='rgba(240, 240, 240, 1)', 
        paper_bgcolor='rgba(255, 255, 255, 1)',
        height = 300,
    )

    return fig


#companies by sector
def sector_trend(df):
    sector_df = df.groupby(by='GICS Sector').agg({'Symbol':'count'})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sector_df.index,y=sector_df['Symbol'], marker=dict(color=sector_df['Symbol'], colorscale='Viridis')
    ))

    fig.update_layout(
        title='Number of Companies by Sector',
        xaxis_title='Sector',
        yaxis_title='Number of Companies',
        plot_bgcolor='rgba(240, 240, 240, 1)',  
        paper_bgcolor='rgba(255, 255, 255, 1)',  
        showlegend=False,  
        xaxis=dict(showgrid=True, gridcolor='lightgray'),  
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        height = 600,
    )

    return fig

#volume by sector
def sector_volume(df):
    sector_df = df.groupby(by='GICS Sector').agg({'Volume':'sum'})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sector_df.index,y=sector_df['Volume'], marker=dict(color=sector_df['Volume'], colorscale='Viridis')
    ))

    fig.update_layout(
        title='Volume of Stock by Sector',
        xaxis_title='Sector',
        yaxis_title='Number of Stock',
        plot_bgcolor='rgba(240, 240, 240, 1)',  
        paper_bgcolor='rgba(255, 255, 255, 1)', 
        showlegend=False,  
        xaxis=dict(showgrid=True, gridcolor='lightgray'), 
        yaxis=dict(showgrid=True, gridcolor='lightgray'),  
    )

    return fig

#gauge chart for sectore performance
def gauge_sector(ticker):
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period='1d')
    close_price = hist['Close'].iloc[-1]
    min_value = 0
    max_value = 1000
    sector_average = (min_value + max_value)/2
    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode='gauge+number+delta',
        value=close_price,
        delta={'reference':sector_average},
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_value, sector_average], 'color': "lightblue"}, 
                {'range': [sector_average, max_value], 'color': "lightgreen"} 
                ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': sector_average 
                },
            },  title={'text': f"Sector's Closed Price Performance"},
    ))

    fig.update_layout(
        height=100,
        margin=dict(l=0, r=0, t=0.1, b=0.1),
    )

    return fig


#plot by sub-indsutry
def subindustry_trend(df):
    sector_df = df.groupby(by='GICS Sub-Industry').agg({'Symbol':'count'})

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=sector_df.index,values=sector_df['Symbol']
    ))

    fig.update_layout(
        title='Number of Companies by Sub Industry',
        plot_bgcolor='rgba(240, 240, 240, 1)',  
        paper_bgcolor='rgba(255, 255, 255, 1)',  
        showlegend = False,
        height = 500,
    )

    return fig

#subindustry volume
def subindustry_volume(df):
    sector_df = df.groupby(by='GICS Sub-Industry').agg({'Volume':'sum'})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sector_df.index, x=sector_df['Volume'], orientation='h'
    ))

    fig.update_layout(
        title='Stock Volumes by Sub Industry',
        plot_bgcolor='rgba(240, 240, 240, 1)', 
        paper_bgcolor='rgba(255, 255, 255, 1)',
        showlegend = False,
        height = 300,
    )

    return fig

#treemap for companies volumes
def companies_volumes(df):
    fig = go.Figure()

    fig.add_trace(go.Treemap(
        labels = df['Symbol'],
        values = df['Volume'],
        parents=[''] * len(df),
        textinfo= 'label',
    ))

    fig.update_layout(
        title="Company Volumes Treemap",
        margin=dict(t=50, l=25, r=25, b=25),
        height = 300,
    )

    return fig

#tables
def table_map(df):
    fig = go.Figure()

    fig.add_trace(go.Table(
            header=dict(
                values=list(df.columns),  
                fill_color='lavender',  
                align='left'             
            ),
            cells=dict(
                values=[df[col] for col in df.columns],  
                fill_color='white',      
                align='left'            
            )
        )
    )

    fig.update_layout(
        height = 300,
        margin=dict(l=0, r=0, t=0, b=0),
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