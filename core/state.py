# core/state.py

import streamlit as st

def init_session_state():
    for key in ["questions", "answers", "options"]:
        if key not in st.session_state:
            st.session_state[key] = []
