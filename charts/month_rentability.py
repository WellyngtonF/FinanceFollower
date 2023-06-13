import altair as alt
import streamlit as st

from dal.rn_rentability import RNRentability


def render_month_rentability_chart():
    rentability = RNRentability()
    
    month_rentability = rentability.get_month_rentability()
    max_abs_value = month_rentability['rentability'].abs().max() + 0.01

    # Create the Altair chart
    month_chart = alt.Chart(month_rentability).mark_bar().encode(
        y=alt.Y('month:O', title='', sort=None, axis=alt.Axis(tickMinStep=1)),
        x=alt.X('rentability:Q', title='Rentabilidade', scale=alt.Scale(domain=[(max_abs_value * -1), max_abs_value]), axis=alt.Axis(format='.1%', domain=True, tickMinStep=0.1)),
        tooltip=[alt.Tooltip('rentability:Q', format='.3%', title='Rentabilidade')],
        color=alt.value('steelblue')
    )

    # Add percentile labels to the bars
    positive_text_layer = month_chart.mark_text(
        align='left',
        baseline='middle',
        dx=5,
    ).encode(
        text=alt.condition(
            alt.datum.rentability > 0,
            alt.Text('rentability:Q', format='.1%'),
            alt.value('')
        ),
        color=alt.value('white')
    )

    # Add percentile labels to the bars
    negative_text_layer = month_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-5
    ).encode(
        text=alt.condition(
            alt.datum.rentability < 0,
            alt.Text('rentability:Q', format='.1%'),
            alt.value('')
        ),
        color=alt.value('white')
    )

    # Configure the chart properties
    month_chart = (month_chart + positive_text_layer + negative_text_layer)
    month_chart = month_chart.configure_view(
        stroke='transparent'  # Hide chart border
    )
    
    # Render the chart using Streamlit
    st.altair_chart(month_chart, use_container_width=True, theme=None)