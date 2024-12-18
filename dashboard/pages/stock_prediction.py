import streamlit as st
import plugins.model as md
import plugins.stock_functions as fs
from sklearn.preprocessing import MinMaxScaler

# Load the LSTM model
@st.cache(allow_output_mutation=True)  # Cache the model to avoid reloading on every interaction
model = md.load_model("something/something.pkl")

# load data

st.title("LSTM Model Prediction")

# Data-loader
df_sp500 = fs.fetch_sp500()

# Sidebar for settings
st.sidebar.header("Dashboard Settings")
selected_stock = st.sidebar.selectbox("Select Stock", df_sp500['Symbol'])
timeframe = st.sidebar.radio("Select Timeframe", ['1D', '1W', '1M'])

# data processing
df_filtered = fs.load_stock_data(selected_stock)
X, y = md.data_preprocessing(df_filtered)

#visualization