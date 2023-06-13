import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from components.table import table
from dal.rn_asset import RNAsset

asset = RNAsset()

def handle_edit(row):
    st.session_state['asset_id'] = row['id']
    switch_page('ativos')

def handle_delete(row):
    asset.delete_asset(row['id'])
    st.experimental_rerun()

def render_asset_page():
    df = asset.get_assets()

    col = st.columns(2)

    with col[0]:
        st.button("Exportar dados", key='asset_export_button')
    with col[1]:
        if st.button("Adicionar", key='asset_add_button'):
            if 'asset_id' in st.session_state:
                del st.session_state['asset_id']
            switch_page('ativos')
            
    table(df, handle_edit, handle_delete, 2)