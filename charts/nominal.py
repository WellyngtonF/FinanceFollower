import altair as alt
import streamlit as st

from dal.rn_rentability import RNRentability


def render_nominal_chart(category_id: str = None):
    rentability = RNRentability()
    nominal_evolution = rentability.get_wallet_total(category_id)

    line = alt.Chart(nominal_evolution).mark_line(interpolate='basis').encode(
        x=alt.X('date', title='Data'),
        y=alt.Y('total', type='quantitative', title='Valor nominal (R$)'),
    )

    nearest = alt.selection_point(nearest=True, on='mouseover', fields=['date'], empty=False)

    selectors = alt.Chart(nominal_evolution).mark_point().encode(
        x='date',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(nominal_evolution).mark_rule(color='gray').encode(
        x='date',
    ).transform_filter(
        nearest
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='right', dx=-5, dy=-10, color='white').encode(
        text=alt.condition(nearest, 'total:Q', alt.value(' '), format='r'),
    )

    title = 'Evolução nominal da categoria' if category_id else 'Evolução nominal da carteira'

    nominal_chart = alt.layer(
        line,
        selectors,
        rules,
        text,
        points
    ).properties(
        title=title
    )

    st.altair_chart(nominal_chart, theme=None, use_container_width=True)