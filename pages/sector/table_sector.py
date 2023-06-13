import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from components.table import table
from dal.rn_sector import RNSector

sector = RNSector()

def handle_edit(row):
    st.session_state['sector_id'] = row['id']
    switch_page('setores')

def handle_delete(row):
    sector.delete_sector(row['id'])
    st.experimental_rerun()

def render_sector_page():
    df = sector.get_sectors()

    col = st.columns(2)

    with col[0]:
        st.button("Exportar dados", key='sector_export_button')
    with col[1]:
        if st.button("Adicionar", key='sector_add_button'):
            if 'sector_id' in st.session_state:
                del st.session_state['sector_id']
            switch_page('setores')
            
    table(df, handle_edit, handle_delete, 1)