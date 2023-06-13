import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox

from components.sidebar import render_sidebar
from dal.rn_category import RNCategory
from dal.rn_sector import RNSector
from dal.rn_asset import RNAsset

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

category, sector, asset = [RNCategory(), RNSector(), RNAsset()]
sector_descriptions = []

def load_form(edit_form: bool = False, data: pd.DataFrame = None) -> None:

    category_df = category.get_categorys()
    category_mapping = {row['Categoria']: row['id'] for _, row in category_df.iterrows()}
    category_id = data['idcategory'][0] if edit_form else 0
    category_description = category_df.loc[category_df['id'] == category_id, 'Categoria'].iloc[0] if edit_form else category_df['Categoria'][0]
    descriptions = list(category_mapping.keys())
    default_index = descriptions.index(category_description)

    asset_id = data['idasset'][0] if edit_form else ""
    asset_name = data['description'][0] if edit_form else ""
    ticker_name = data['ticker'][0] if edit_form else ""
    is_usd_input = data['is_usd'][0] if edit_form else 0

    with st.container():
        asset_name_input = st.text_input('**Ativo**', asset_name)

        cols = st.columns(3)
        with cols[0]:
            ticker_input = st.text_input('**Simbolo**', ticker_name)

            is_usd_input = st.checkbox('Cotação em dólar ?', value=is_usd_input)

        with cols[1]:
            category_description = st.selectbox('**Categoria**', options=descriptions, index=default_index, key='category_asset_form')        
            category_id_input = category_mapping[category_description] if category_description else None

        with cols[2]:
            sector_df = sector.get_sector_by_idcategory(category_id_input)
            sector_mapping = {row['description']: row['idsector'] for _, row in sector_df.iterrows()}
            sector_id = data['idsector'][0] if edit_form and data['idsector'][0] else 0
            sector_description = sector_df.loc[sector_df['idsector'] == sector_id, 'description'].iloc[0] if edit_form and sector_id > 0 else None

            sector_descriptions = list(sector_mapping.keys())
            default_index_sector = sector_descriptions.index(sector_description) if sector_description else 0

            sector_description = selectbox('**Setor**', sector_descriptions, no_selection_label='Nenhum', index=default_index_sector)
            sector_id_input = sector_mapping[sector_description] if sector_description else None

        submit_button = st.button("Atualizar" if edit_form else "Salvar")
        if submit_button:
            if edit_form:
                asset.edit_asset(category_id_input, sector_id_input, asset_name_input, ticker_input, is_usd_input, asset_id)
            else:
                asset.insert_asset(category_id_input, sector_id_input, asset_name_input, ticker_input, is_usd_input)
            switch_page('cadastros')

def create_asset():
    st.markdown('#### **Adicionar novo ativo**')

    load_form()

def edit_asset(asset_id):
    st.markdown('#### **Editar ativo**')
   
    df = asset.get_asset_by_id(asset_id)
    load_form(edit_form=True, data=df)


def render_form():
    if st.button('⬅️ Voltar'):
        switch_page('cadastros')

    if 'asset_id' in st.session_state:
        edit_asset(st.session_state['asset_id'])
    else:
        create_asset()

if __name__ == "__main__":
    render_sidebar()
    render_form()