import streamlit as st
import pandas as pd
import numpy as np

st.markdown("""
Teste
""")

with open('./styles/main.css')as f:
 st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

resume_data = {
    'Amount Invested': "R$ 10000,00",
    'Current value': "R$ 12000,00",
    'Rentability': [np.random.uniform(low=0, high=10) for _ in range(6)]
}

# Render the home page
def render_home_page():
    st.title("Investment Dashboard")
    st.subheader("Summary of Investments")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.write(resume_data['Amount Invested'])
            st.info("Amount Invested")

    with col2:
        with st.container():
            st.write(resume_data['Current value'])
            st.info("Current Value")

    with col3:
        with st.container():
            st.info("Rentability")
            for i, rentability in enumerate(resume_data['Rentability']):
                st.write(f"Period {i+1}: {rentability}%")
# Run the app
if __name__ == '__main__':
    render_home_page()