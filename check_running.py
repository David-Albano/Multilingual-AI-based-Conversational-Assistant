import streamlit as st

class StopConversation(Exception):
    pass


def check_running():
    if not st.session_state.running:
        raise StopConversation()