import streamlit as st

def card(data, title, icon):
    st.markdown(
        f"""
        <style>
            .card-container {{
                display: flex;
                align-items: center;
                border: 1px solid black;
                border-radius: 5px;
                background-color: #282930;
                margin-top: -20px !important;
                padding-top: 0px !important;
                # width: fit-content;
                max-width: 100%;
                cursor: pointer;
            }}
            .card-icon {{
                margin-left: 5px;
                font-size: 48px;
                margin-right: 15px;
            }}
            .card-content {{
                font-size: 40px;
                font-weight: bold;
                
            }}
            .card-text {{
                flex-grow: 1;
                margin-top: 2px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}
            # .card-title {{
            #     white-space: nowrap;
            #     overflow: hidden;
            #     text-overflow: ellipsis;
            # }}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container() as _:
        st.markdown(
            f"""
            <div class="card-container">
                <div class="card-icon">{icon}</div>
                <div class="card-text">
                    <div class="card-content">{data}</div>
                    <div class="card-title">{title}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )