import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

from components.sidebar import render_sidebar
from dal.rn_sector import RNSector
from dal.rn_category import RNCategory

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

sector = RNSector()
category = RNCategory()

def load_form(edit_form: bool = False, data: pd.DataFrame = None) -> None:
    category_df = category.get_categorys()
    category_mapping = {row['Categoria']: row['id'] for _, row in category_df.iterrows()}
    category_id = data['idcategory'][0] if edit_form else 0
    category_description = category_df.loc[category_df['id'] == category_id, 'Categoria'].iloc[0] if edit_form else category_df['Categoria'][0]
    descriptions = list(category_mapping.keys())
    default_index = descriptions.index(category_description)

    sector_id = data['idsector'][0] if edit_form else ""
    sector_name = data['description'][0] if edit_form else ""

    with st.form("sector_form"):
        sector_name_input = st.text_input('**Setor**', sector_name)

        category_description = st.selectbox('**Categoria**', options=descriptions, index=default_index)
        
        category_id_input = category_mapping[category_description] if category_description else None

        submit_button = st.form_submit_button("Atualizar" if edit_form else "Salvar")
        if submit_button:
            if edit_form:
                sector.edit_sector(category_id_input, sector_name_input, sector_id)
            else:
                sector.insert_sector(category_id_input, sector_name_input)
            switch_page('cadastros')

def create_sector():
    st.markdown('#### **Adicionar novo setor**')

    load_form()

def edit_sector(sector_id):
    st.markdown('#### **Editar setor**')
   
    df = sector.get_sector_by_id(sector_id)
    load_form(edit_form=True, data=df)

def render_form():
    if st.button('⬅️ Voltar'):
        switch_page('cadastros')

    if 'sector_id' in st.session_state:
        edit_sector(st.session_state['sector_id'])
    else:
        create_sector()

if __name__ == "__main__":
    render_sidebar()
    render_form()