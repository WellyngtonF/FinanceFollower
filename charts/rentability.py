import altair as alt
import streamlit as st
import pandas as pd

from dal.rn_rentability import RNRentability

def render_rentability_chart(id_category: str = None, benchmark:str = '^BVSP'):
    rentability = RNRentability()
    
    benchmark_rentability, bench_name = rentability.get_benchmark_rentability(benchmark)
    wallet_rentability = rentability.get_rentability(id_category)

    benchmark_df = pd.merge(wallet_rentability, benchmark_rentability, how='left', left_on='date', right_on='Date')
    benchmark_df = benchmark_df.reset_index().melt('date', var_name='Benchmark', value_vars=['Carteira', bench_name], value_name='y')
    
    nearest = alt.selection_point(nearest=True, on='mouseover', fields=['date'], empty=False)

    
    line = alt.Chart(benchmark_df).mark_line(interpolate='basis').encode(
        x=alt.X('date', title='Data'),
        y=alt.Y('y', type='quantitative', axis=alt.Axis(format='%'), title='Rentabilidade'),
        color=alt.Color('Benchmark:N', sort=None)
    )


    selectors = alt.Chart(benchmark_df).mark_point().encode(
        x='date',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'y:Q', alt.value(' '), format='.2%')
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(benchmark_df).mark_rule(color='gray').encode(
        x='date',
    ).transform_filter(
        nearest
    )

    title = 'Rentabilidade da categoria vs benchmark' if id_category else 'Rentabilidade da carteira vs benchmark'
    # Put the five layers into a chart and bind the data
    rentability_chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        title=title
    )

    st.altair_chart(rentability_chart, theme=None, use_container_width=True)