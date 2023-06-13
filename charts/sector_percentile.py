import altair as alt
import pandas as pd
import streamlit as st
from pandas import DataFrame

from dal.rn_rentability import RNRentability

# Waffle chart
def render_sector_percentile_chart(percentile_wallet: DataFrame, id_category:str):
    rentability = RNRentability()
    df = rentability.get_sector_percentile(percentile_wallet, id_category)
    df['proportion'] = df['amount'] / df['amount'].sum()
    df = df.sort_values('proportion')

    # Calculate the number of squares for each category based on the proportion
    df['count'] = (df['proportion'] * 100).round().astype(int)

    # Calculate the adjustment needed to ensure a total count of 100
    total_count = df['count'].sum()
    count_adjustment = 100 - total_count

    # Apply the adjustment to the category with the largest rounding error
    if count_adjustment < 0:
        # If the total count is less than 100, reduce the count of the category with the largest rounding error
        df.loc[df['count'].idxmax(), 'count'] += count_adjustment
    elif count_adjustment > 0:
        # If the total count is greater than 100, increase the count of the category with the largest rounding error
        df.loc[df['count'].idxmin(), 'count'] += count_adjustment

    # Generate a sequence of values for each category based on the count
    values = []
    for _, row in df.iterrows():
        count = row['count']
        values.extend([row['description']] * count)

    # Create a new DataFrame with the values
    df_values = pd.DataFrame({'value': values})
    df_values['index'] = df_values.index.values

    # Create the waffle chart using Altair
    chart = alt.Chart(df_values).mark_square(size=240).transform_calculate(
        row='floor(datum.index / 10)',
        column='datum.index % 10'
    ).encode(
        x=alt.X('column:O', title=None, axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('row:O', title=None, axis=alt.Axis(labels=False, ticks=False)),
        color=alt.Color("value:N", sort=None, legend=alt.Legend(title='Setores')),
        tooltip=[alt.Tooltip('value:N', title='Setor')],
    ).properties(
        title='Alocação da carteira por setor'
    )
    # Display the waffle chart in Streamlit
    st.altair_chart(chart, use_container_width=True)