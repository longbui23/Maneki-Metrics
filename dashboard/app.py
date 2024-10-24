import streamlit as st
import plotly.express as px
import pandas as pd

# Load sample data
@st.cache_data
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

df = load_data()

# Set page title
st.set_page_config(page_title="Interactive Country Data Visualization")

# App title
st.title('Interactive Country Data Visualization')

# Country selection dropdown
selected_country = st.selectbox(
    'Choose a country:',
    options=df['country'].unique(),
    index=df['country'].unique().tolist().index('Canada')
)

# Filter data based on selected country
filtered_df = df[df['country'] == selected_country]

# Create and display the graph
fig = px.line(filtered_df, x='year', y='lifeExp', title=f'Life Expectancy in {selected_country}')
st.plotly_chart(fig)

# Optional: Display the data
if st.checkbox('Show raw data'):
    st.write(filtered_df)