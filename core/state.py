# core/state.py

import streamlit as st

def init_session_state():
    for key in ["questions", "answers", "options"]:
        if key not in st.session_state:
            st.session_state[key] = []

def reset_all():
    st.session_state.questions = []
    st.session_state.answers = {}
    st.session_state.options = []
