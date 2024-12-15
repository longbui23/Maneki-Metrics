import plugins.financial_functions as fs_main
import plugins.functions as fs

import streamlit as st

st.set_page_config(page_title="Makeni.net", layout="wide", page_icon="🐱")
st.title("Company Info")

#styling
with open("styling/sidebar.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Data-loader
df_sp500 = fs.fetch_sp500()

# Sidebar for settings
st.sidebar.header("Dashboard Settings")
selected_stock = st.sidebar.selectbox("Select Stock", df_sp500['Symbol'])
timeframe = st.sidebar.radio("Select Timeframe", ['1D', '1W', '1M'])

#filter stock
df_filtered = fs_main.fetch_balance_sheet_data(selected_stock)

#3 radio to choose 3 types of dashboard
option = st.radio("Select Dashboard", ["Balance Sheet", "Income-Statement", "Cash-Flow"], horizontal=True)

# Show the selected chart based on the option
## Balance Sheet
if option == "Balance Sheet":
    st.subheader("Balance Sheet")
    st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)

## Income-Statement
elif option == "Income-Statement":
    st.subheader("Income-Statement")
    st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)

## Cash-Flow
elif option == "Cash-Flow":
    st.subheader("Cash-Flow")
    st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)