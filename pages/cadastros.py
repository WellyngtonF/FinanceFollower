import streamlit as st

from components.sidebar import render_sidebar
from pages.category.table_category import render_category_page
from pages.sector.table_sector import render_sector_page
from pages.asset.table_asset import render_asset_page

with open('./styles/cadastros.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def render_page():
    categ_tab, sec_tab, asset_tab = st.tabs(["Categorias", "Setores", "Ativos"])
    
    with categ_tab:
        render_category_page()
        
    with sec_tab:
        render_sector_page()

    with asset_tab:
        render_asset_page()
        
# Run the app
if __name__ == '__main__':
    render_sidebar()
    render_page()