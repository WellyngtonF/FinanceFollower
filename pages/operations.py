import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from components.sidebar import render_sidebar
from dal.rn_operations import RNOperation
from dal.rn_asset import RNAsset

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

operations, asset = [RNOperation(), RNAsset()]

def render_operations_page():
    asset_df = asset.get_assets()
    asset_mapping = {row['Ativo']: row['id'] for _, row in asset_df.iterrows()}
    descriptions = list(asset_mapping.keys())
    with st.form("injection_form"):
        st.markdown('#### **Adicionar nova operação**')

        asset_description = st.selectbox('**Ativo**', options=descriptions)
        asset_id_input = asset_mapping[asset_description] if asset_description else None

        cols = st.columns(2)
        with cols[0]:
            quantity_input = st.number_input("**Quantidade**", min_value=0.0, format='%f', step=0.01)
            date_input = st.date_input("**Data da operação**")
        with cols[1]:
            price_input = st.number_input("**Preço de negociação**", min_value=0.0, format='%f', step=0.01)
            direction_radio = st.radio(
                "A operação foi de compra ou venda ?",
                ('Compra', 'Venda',)
            )

        if st.form_submit_button('Salvar'):
            direction_input = 1 if direction_radio == 'Compra' else 0
            operations.insert_operation(asset_id_input, date_input, quantity_input, price_input, direction_input)
            switch_page("Home")


if __name__ == "__main__":
    render_sidebar()
    render_operations_page()