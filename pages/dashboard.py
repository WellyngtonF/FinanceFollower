import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.metric_cards import style_metric_cards

from components.sidebar import render_sidebar
from dal.rn_rentability import RNRentability
from dal.rn_operations import RNOperation
from dal.rn_category import RNCategory
from dal.rn_sector import RNSector
from data_treatment.routine import verify_inserted_rentability

from charts.nominal import render_nominal_chart
from charts.percentile_wallet import render_percentile_wallet
from charts.category_percentile import render_category_percentile_chart
from charts.sector_percentile import render_sector_percentile_chart
from charts.rentability import render_rentability_chart
from charts.month_rentability import render_month_rentability_chart
from charts.general_waterfall import render_general_watterfall_chart

with open('./styles/main.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

rentability = RNRentability()
operation = RNOperation()
category = RNCategory()
sector = RNSector()
category_df = category.get_categorys()

def render_general_tab(percentile_wallet: pd.DataFrame):
    card_cols = st.columns(3)

    df = rentability.get_categorys_rentability(percentile_wallet)

    invested_value = round(df['Investido (R$)'].sum(),2)
    actual_value = round(df['Atual (R$)'].sum(),2)
    rentability_value = str(round(((actual_value/invested_value) - 1) * 100,2)) + '%'

    card_cols[0].metric(label='Valor investido (R$)', value=invested_value, delta='')
    card_cols[1].metric(label='Valor atual (R$)', value=actual_value)
    card_cols[2].metric(label='Rentabilidade', value=rentability_value)
    style_metric_cards(background_color='#080808', border_left_color='#ff4b4b')

    render_nominal_chart()

    cols = st.columns(2)

    with cols[0]:
        render_percentile_wallet(percentile_wallet)

    with cols[1]:
        render_category_percentile_chart(percentile_wallet)

    st.dataframe(df, hide_index=True, use_container_width=True, column_config={
        'Rentabilidade': st.column_config.NumberColumn(
            format="%.2f%%"
        )
    })

def render_rentability_tab():
    render_rentability_chart()

    render_month_rentability_chart()

    render_general_watterfall_chart()

def render_operations_tab():
    minimal_date = operation.get_minimal_operational_date()

    cols = st.columns(4)
    with cols[0]:
        selected_min_date = st.date_input('Data Inicial', value=minimal_date, min_value=minimal_date)
    with cols[1]:
        selected_max_date = st.date_input('Data Final', min_value=minimal_date)
    with cols[2]:
        category_mapping = {row['Categoria']: row['id'] for _, row in category_df.iterrows()}

        category_descriptions = list(category_mapping.keys())
            
        category_selected = selectbox('**Categoria**', category_descriptions, no_selection_label='Nenhum', )
        category_id_input = category_mapping[category_selected] if category_selected else None

    with cols[3]:
        asset_filter = st.text_input('**Ativo**')

    operation_df = operation.get_operations(selected_min_date, selected_max_date, category_id_input, asset_filter)

    st.dataframe(operation_df, hide_index=True, use_container_width=True)

def render_categorys_tab(category_id: str, benchmark:str, percentile_wallet: pd.DataFrame):
    df = percentile_wallet[percentile_wallet['idcategory'] == category_id]
    assets_df = rentability.get_assets_rentability(df)

    invested_value = round(assets_df['Investido (R$)'].sum(),2)
    actual_value = round(assets_df['Atual (R$)'].sum(),2)
    rentability_value = str(round(((actual_value/invested_value) - 1) * 100,2)) + '%'

    card_cols = st.columns(3)
    card_cols[0].metric(label='Valor investido (R$)', value=invested_value, delta='')
    card_cols[1].metric(label='Valor atual (R$)', value=actual_value)
    card_cols[2].metric(label='Rentabilidade', value=rentability_value)
    style_metric_cards(background_color='#080808', border_left_color='#ff4b4b')

    render_nominal_chart(category_id)

    render_rentability_chart(category_id, benchmark)

    if sector.have_sector(category_id):

        cols = st.columns(2)

        with cols[0]:
            render_percentile_wallet(df)

        with cols[1]:
            render_sector_percentile_chart(df, category_id)

    else:
        render_percentile_wallet(df)

    st.dataframe(assets_df, hide_index=True, use_container_width=True, column_config={
        'Rentabilidade': st.column_config.NumberColumn(
            format="%.2f%%"
        )
    })

def render_dash_page():
    default_tabs = np.array(["Geral", "Rentabilidade", "Operações"])    
    category_tabs = np.array(category_df['Categoria'])
    tabs_name = np.concatenate([default_tabs, category_tabs])

    tabs = st.tabs(tabs_name.tolist())

    percentile_wallet = rentability.get_percentile_wallet()
    verify_inserted_rentability()
    with tabs[0]:
        render_general_tab(percentile_wallet)
        
    with tabs[1]:
        render_rentability_tab()

    with tabs[2]:
        render_operations_tab()

    for i, row in category_df.iterrows():
        index_tab = i +3
        with tabs[index_tab]:
            render_categorys_tab(row['id'], row['Benchmark'], percentile_wallet)


# Run the app
if __name__ == '__main__':
    render_sidebar()
    render_dash_page()