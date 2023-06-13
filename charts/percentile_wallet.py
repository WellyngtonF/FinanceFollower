import altair as alt
import streamlit as st
from pandas import DataFrame

from dal.rn_rentability import RNRentability


def render_percentile_wallet(percentile_wallet: DataFrame):
    max_domain = round(percentile_wallet['amount'].max() / percentile_wallet['amount'].sum(),1)
    max_domain = max_domain + 0.1 if max_domain < 1 else max_domain
    base_chart = alt.Chart(percentile_wallet).transform_joinaggregate(
        totalAmount = 'sum(amount)'
    ).transform_calculate(
        Percentual = 'datum.amount / datum.totalAmount'
    ).mark_bar(
        
    ).encode(
        x=alt.X('Percentual:Q', axis=alt.Axis(format='%', orient='top'), scale=alt.Scale(domain=[0, max_domain]), title=None),
        y=alt.Y('description:N', sort='-x', title='Ativo')
    ).properties(
        title='Alocação da carteira por ativo'
    )

    label = base_chart.mark_text(
        baseline='middle',
        align='left',
        color='white',
        dx=5
    ).encode(
        text=alt.Text('Percentual:Q', format='.1%'),
        x= alt.X('Percentual:Q', axis=alt.Axis(format='.1%'))
    )

    chart = alt.layer(
        base_chart,
        label
    )

    st.altair_chart(chart, theme=None, use_container_width=True)