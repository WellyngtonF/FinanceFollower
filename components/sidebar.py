import streamlit as st
from st_pages import show_pages_from_config, hide_pages
from streamlit_extras.switch_page_button import switch_page

def render_sidebar():
    show_pages_from_config()
    hide_pages(['Categorias', 'Setores', 'Ativos', 'Aportes', 'Operações'])

    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"]{
            min-height: 70%;
        }
        .css-1oe5cao {
            min-height: 100%;
            max-height: 100%
        }
        """,
            unsafe_allow_html=True,
        )   

    cols = st.sidebar.columns([1,10,1])
    
    with cols[1]:
    # Add a button at the bottom of the sidebar
        if st.button("Adicionar aporte", use_container_width=True):
            switch_page("aportes")

        if st.button("Adicionar operação", use_container_width=True):
            switch_page("operações")