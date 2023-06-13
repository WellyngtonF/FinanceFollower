import altair as alt
import pandas as pd
import streamlit as st
from pandas import DataFrame

from dal.rn_rentability import RNRentability

# Donut chart
# def render_category_percentile_chart(percentile_wallet: DataFrame):
#     rentability = RNRentability()
#     category_percentile = rentability.get_category_percentile(percentile_wallet)

#     base = alt.Chart(category_percentile).encode(
#         theta=alt.Theta(field='amount', type="quantitative", stack=True),
#         color=alt.Color(field='Categoria', legend=None, type='nominal')
#     )

#     donut = base.mark_arc(innerRadius=50, outerRadius=100)
#     text = base.mark_text(radius=120, size=10).encode(text='Categoria:N')

#     category_chart = donut + text

#     st.altair_chart(category_chart, use_container_width=True)


# # Mosaic chart
# def render_category_percentile_chart(percentile_wallet: DataFrame):
#     # rentability = RNRentability()
#     # category_percentile = rentability.get_category_percentile(percentile_wallet)
#     df = percentile_wallet

#     df['rank'] = df['amount'].rank(ascending=False, method='dense')
#     # Calculate the accumulated amount for each category

#     # Initialize the sub-rank as 1 for the first category
#     df['rx'] = 1

#     # Determine the sub-rank based on accumulated amounts
#     max_amount = df['amount'].max()
#     accumulated_amount = 0

#     for i in range(1, len(df)):
#         accumulated_amount += df.iloc[i]['amount'].sum()
#         print(accumulated_amount)
#         if accumulated_amount <= max_amount:
#             if df.at[i - 1, 'rx'] == 1:
#                 df.at[i, 'rx'] = 2
#             else:
#                 df.at[i, 'rx'] = df.at[i - 1, 'rx']
#         else:
#             df.at[i, 'rx'] = df.at[i - 1, 'rx'] + 1

#     df['ry'] = df.groupby('rx').cumcount() + 1
#     df['count_y'] = df.groupby('rx')['ry'].transform('nunique')

#     # Sort the dataframe back to its original order
#     df = df.sort_index()

#     df['x'] = (df['rx'] - 1) * 3
#     df['x2'] = df['rx'] * 3
#     df['y'] = 9 / df['count_y'] * (df['ry'] - 1)
#     df['y2'] = 9 / df['count_y'] * (df['ry'])

#     rect = alt.Chart(df).mark_rect().encode(
#         x=alt.X("x:Q", axis=None),
#         x2="x2",
#         y="y:Q",
#         y2="y2",
#         color=alt.Color("Categoria:N", legend=None),
#         tooltip=["Categoria:N"],
#     )


#     # category_chart = alt.layer(
#     #     rect
#     # )

#     st.altair_chart(rect, theme=None, use_container_width=True)

# Waffle chart
def render_category_percentile_chart(percentile_wallet: DataFrame):
    rentability = RNRentability()
    df = rentability.get_category_percentile(percentile_wallet)
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
        values.extend([row['Categoria']] * count)

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
        color=alt.Color("value:N", sort=None, legend=alt.Legend(title='Categorias')),
        tooltip=[alt.Tooltip('value:N', title='Categoria')],
    ).properties(
        title='Alocação da carteira por categoria'
    )
    # Display the waffle chart in Streamlit
    st.altair_chart(chart, use_container_width=True)