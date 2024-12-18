import streamlit as st
import plugins.model as md
import plugins.stock_functions as fs
from sklearn.preprocessing import MinMaxScaler

# Load the LSTM model
model = md.load_model("something/something.pkl")

# Data-loader
df_sp500 = fs.fetch_sp500()

# load data
# Sidebar for settings
st.sidebar.header("Dashboard Settings")
selected_stock = st.sidebar.selectbox("Select Stock", df_sp500['Symbol'])
timeframe = st.sidebar.radio("Select Timeframe", ['1D', '1W', '1M'])

#build modeldata
model, predictions, y_actual  = md.train_lstm_model(selected_stock,  start_date='2010-01-01', end_date='2024-12-01')

#visualize prediction
fig = md.visualize_predictions(selected_stock, model, window_size=60, days_ahead=30)
st.plotly_chart(fig)