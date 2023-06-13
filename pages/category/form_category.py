import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

from dal.rn_category import RNCategory
from components.sidebar import render_sidebar

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

category = RNCategory()

def load_form(edit_form: bool = False, data: pd.DataFrame = None) -> None:
    category_id = data['idcategory'][0] if edit_form else ""
    category_name = data['description'][0] if edit_form else ""
    cash_brl = data['cash_brl'][0] if edit_form else 0.0
    cash_usd = data['cash_usd'][0] if edit_form else 0.0
    benchmark = data['benchmark'][0] if edit_form else ''

    with st.form("category_form"):
        category_name_input = st.text_input('**Categoria**', category_name)
        cash_brl_input = st.number_input('**Caixa R$**', value=cash_brl, min_value=0.0, format='%f', step=0.01)
        cash_usd_input = st.number_input('**Caixa $**', value=cash_usd, min_value=0.0, format='%f', step=0.01)

        benchmark_input = st.text_input('**Simbolo do benchmark**', value=benchmark, key='bench_input')

        submit_button = st.form_submit_button("Atualizar" if edit_form else "Salvar")
        if submit_button:
            if edit_form:
                category.edit_category(category_name_input, cash_brl_input, cash_usd_input, benchmark_input, category_id)
            else:
                category.insert_category(category_name_input, cash_brl_input, cash_usd_input, benchmark_input)
            switch_page('cadastros')

def create_category():
    st.markdown('#### **Adicionar nova categoria**')

    load_form()

def edit_category(category_id):
    st.markdown('#### **Editar categoria**')
   
    df = category.get_category_by_id(category_id)
    load_form(edit_form=True, data=df)

def render_form():
    if st.button('⬅️ Voltar'):
        switch_page('cadastros')
    if 'category_id' in st.session_state:
        edit_category(st.session_state['category_id'])
    else:
        create_category()

if __name__ == "__main__":
    render_sidebar()
    render_form()