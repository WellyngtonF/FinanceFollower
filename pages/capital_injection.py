import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from components.sidebar import render_sidebar
from dal.rn_capital import RNCapital

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

capital = RNCapital()

def render_capital_injection_page():
    with st.form("injection_form"):
        st.markdown('#### **Adicionar novo aporte**')

        capital_injection_input = st.number_input("**Valor do aporte**", min_value=0.0, format='%f', step=0.01)

        injection_date_input = st.date_input("**Data do aporte**")

        if st.form_submit_button('Salvar'):
            capital.insert_capital(capital_injection_input, injection_date_input)
            switch_page("Home")

if __name__ == "__main__":
    render_sidebar()
    render_capital_injection_page()