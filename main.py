import streamlit as st

from components.sidebar import render_sidebar

st.set_page_config('Home')

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Render the home page
def render_home_page():
    render_sidebar()

    st.markdown("""
    # Finance Follower

    Sua ferramenta diária para acompanhar seus investimentos, sejam eles em ações, FIIs, criptomoedas e etc

    ### Input de dados

    Para o cadastro de seus investimentos é necessário cadastrar algumas informações, como a categorização da sua carteira, setores, aportes,
    ativos investidos, compras e vendas.

    ### Dashboard

    No dashboard você poderá acompanhar a evolução de seu patrimônio, assim como ver as últimas movimentações feitas na sua carteira, rentabilidade e etc
    """)

# Run the app
if __name__ == '__main__':
    render_home_page()