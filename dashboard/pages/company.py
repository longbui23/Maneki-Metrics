import plugins.financial_functions as fs_main
import plugins.stock_functions as fs
import plugins.cloud_connection as cc

import streamlit as st

st.set_page_config(page_title="Makeni.net", layout="wide", page_icon="🐱")
st.title("Company Info")

#styling
with open("dashboard/styling/sidebar.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Data-loader
client = cc.connect_bigquery()
df_sp500 = fs.fetch_company(client)

# Sidebar for settings
st.sidebar.header("Dashboard Settings")
selected_stock = st.sidebar.selectbox("Select Stock", df_sp500['Symbol'])
timeframe = st.sidebar.radio("Select Timeframe", ['1D', '1W', '1M'])

#3 radio to choose 3 types of dashboard
option = st.radio("Select Dashboard", ["Balance Sheet", "Income-Statement", "Cash-Flow"], horizontal=True)

# Show the selected chart based on the option
## Balance Sheet
if option == "Balance Sheet":
    #try:
    df_filtered = fs_main.fetch_balance_sheet_data(selected_stock)
    st.plotly_chart(fs_main.plot_table(df_filtered.transpose(), selected_stock))
    st.markdown( df_filtered[['Net Debt', 'Total Debt']])
    st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)
    #except:
    #    st.markdown(f"Company does not published {option}")

## Income-Statement
elif option == "Income-Statement":
    try:
        df_filtered = fs_main.fetch_income_stmt_data(selected_stock)
        st.plotly_chart(fs_main.plot_table(df_filtered.transpose(), selected_stock))
        st.subheader("Income-Statement")
        st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)
    except:
        st.markdown(f"Company does not published {option}")

## Cash-Flow
elif option == "Cash-Flow":
    try:
        df_filtered = fs_main.fetch_cash_flow_data(selected_stock)
        st.plotly_chart(fs_main.plot_table(df_filtered.transpose(), selected_stock))
        st.subheader("Cash-Flow")
        st.plotly_chart(fs_main.key_balance_sheet_chart(df_filtered), use_container_width=True)
    except:
        st.markdown(f"Company does not published {option}")