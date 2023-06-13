import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from components.table import table
from dal.rn_category import RNCategory

category = RNCategory()

def handle_edit(row):
    st.session_state['category_id'] = row['id']
    switch_page('categorias')

def handle_delete(row):
    category.delete_category(row['id'])
    st.experimental_rerun()

def render_category_page():
    df = category.get_categorys()

    col = st.columns(2)

    with col[0]:
        st.button("Exportar dados")
    with col[1]:
        if st.button("Adicionar"):
            if 'category_id' in st.session_state:
                del st.session_state['category_id']
            switch_page('categorias')

    table(df, handle_edit, handle_delete)