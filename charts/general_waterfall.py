import altair as alt
import streamlit as st

from dal.rn_rentability import RNRentability


def render_general_watterfall_chart():
    rentability = RNRentability()
    df = rentability.get_general_waterfall_data()

    # The "base_chart" defines the transform_window, transform_calculate, and X axis
    base_chart = alt.Chart(df).transform_window(
        window_sum_amount="sum(wf_data)",
        window_lead_label="lead(description)",
    ).transform_calculate(
        calc_lead="datum.window_lead_label === null ? datum.description : datum.window_lead_label",
        calc_prev_sum="datum.description === 'End' ? 0 : datum.window_sum_amount - datum.wf_data",
        calc_amount="datum.description === 'End' ? datum.window_sum_amount : datum.wf_data",
        calc_sum_dec_value="datum.window_sum_amount < datum.calc_prev_sum ? round(datum.wf_data * 10000) / 100 : ''",
        calc_sum_dec_coord="datum.window_sum_amount < datum.calc_prev_sum ? datum.window_sum_amount : ''",
        calc_sum_inc_value="datum.window_sum_amount > datum.calc_prev_sum ? round(datum.wf_data * 10000) / 100: ''",
        calc_sum_inc_coord="datum.window_sum_amount > datum.calc_prev_sum ? datum.window_sum_amount : ''",
    ).encode(
        x=alt.X(
            "description:O",
            axis=alt.Axis(title="Ativos", labelAngle=-45, labelPadding=10),
            sort=None,
        )
    )

    color_coding = {
        "condition": [
            {"test": "datum.calc_amount < 0", "value": "#fa4d56"},
        ],
        "value": "#24a148",
    }

    bar = base_chart.mark_bar().encode(
        y=alt.Y("calc_prev_sum:Q", title="Retorno (%)", axis=alt.Axis(format='.1%')),
        y2=alt.Y2("window_sum_amount:Q", title='' ),
        color=color_coding,
    )

    # The "rule" chart is for the horizontal lines that connect the bars
    rule = base_chart.mark_rule(
        xOffset=-18,
        x2Offset=18,
        color='white'
    ).encode(
        y="window_sum_amount:Q",
        x2="calc_lead",
    )

    # Add values as text
    text_pos_values_top_of_bar = base_chart.mark_text(
        baseline="bottom",
        dy=-4,
        color='white'
    ).encode(
        text=alt.Text("calc_sum_inc_value:N"),
        y=alt.Y("calc_sum_inc_coord:Q", axis=alt.Axis(format='.1%'))
    )

    text_neg_values_bot_of_bar = base_chart.mark_text(
        baseline="top",
        dy=4,
        color='white'
    ).encode(
        text=alt.Text("calc_sum_dec_value:N"),
        y=alt.Y("calc_sum_dec_coord:Q", axis=alt.Axis(format='.1%'))
    )

    chart = alt.layer(
        bar,
        rule,
        text_pos_values_top_of_bar,
        text_neg_values_bot_of_bar,
    ).configure_view(
        stroke='transparent'
    ).properties(
        height=450
    )

    st.altair_chart(chart, theme=None, use_container_width=True)