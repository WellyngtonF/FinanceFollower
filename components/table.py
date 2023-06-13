import streamlit as st
import pandas as pd

def table(dataframe: pd.DataFrame, edit_func=None, delete_func=None, table_index=0) -> None:

    st.markdown(
        f"""
        <style>
            .element-container.divisao_table {{
                height: 20px;
                margin-top: -25px;
                padding-top: 0px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render the table headers
    columns = dataframe.columns.tolist()
    columns.append("Ações")
    header_elements = st.columns(len(columns))

    for i, column in enumerate(columns):
        header_elements[i].write(f"**{column}**")
    
    st.markdown("""
            <div width="704" class="element-container css-1hynsf2 divisao_table e1tzin5v2">
                <div style="width: 704px;">
                    <div class="css-nahz7x e16nr0p34">
                        <hr>
                    </div>
                </div>
            </div>""", 
            unsafe_allow_html=True)

    # Render the table rows
    for index, row in dataframe.iterrows():
        values = row.values.tolist()
        row_elements = st.columns(len(columns))  # Add 1 column for actions

        # Render the data columns
        for i, value in enumerate(values):
            row_elements[i].write(f"{value}")

        # Render the actions column
        if edit_func is not None and delete_func is not None:
            actions_column = row_elements[-1].columns(2)  # Create 2 sub-columns
            edit_button = actions_column[0].button('✏️', key=f'edit_{index}_{table_index}', type='primary')
            delete_button = actions_column[1].button('🗑️', key=f'delete_{index}_{table_index}', type='primary')
            if edit_button:
                edit_func(row)
            if delete_button:
                delete_func(row)

        # Add separator between rows
        st.markdown("""
            <div width="704" class="element-container css-1hynsf2 divisao_table e1tzin5v2">
                <div style="width: 704px;">
                    <div class="css-nahz7x e16nr0p34">
                        <hr>
                    </div>
                </div>
            </div>""", 
            unsafe_allow_html=True)