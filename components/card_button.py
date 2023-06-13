import streamlit as st
from streamlit.elements import button_proto

def card_button(data, title, icon, on_click):
    button_proto.button_proto.empty = button_proto.empty

    card_button = button_proto.button_proto.empty()

    def handle_card_click():
        on_click(title)

    card_button.label = f"""
        <div class="card-container">
            <div class="card-icon">{icon}</div>
            <div class="card-text">
                <div class="card-content">{data}</div>
                <div>{title}</div>
            </div>
        </div>
    """
    card_button.onclick = handle_card_click