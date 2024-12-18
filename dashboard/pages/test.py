import streamlit as st

# Inject custom CSS for switch styling
st.markdown(
    """
    <style>
    .stCheckbox > div {
        display: flex;
        align-items: center;
    }
    .stCheckbox div[role='checkbox'] {
        width: 50px;
        height: 25px;
        background-color: grey;
        border-radius: 15px;
        position: relative;
        transition: background-color 0.3s ease;
    }
    .stCheckbox div[role='checkbox'][aria-checked='true'] {
        background-color: #4caf50;
    }
    .stCheckbox div[role='checkbox']::after {
        content: '';
        width: 21px;
        height: 21px;
        background-color: white;
        border-radius: 50%;
        position: absolute;
        top: 2px;
        left: 2px;
        transition: left 0.3s ease;
    }
    .stCheckbox div[role='checkbox'][aria-checked='true']::after {
        left: 27px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout with text and toggle
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.write("Companies")

with col2:
    switch_state = st.checkbox("", key="companies_volume_toggle")

with col3:
    st.write("Volume")

# Display the toggle state
if switch_state:
    st.success("Switched to Volume")
else:
    st.info("Switched to Companies")
