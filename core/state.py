# core/state.py

import streamlit as st

def init_session_state():
    defaults = {
        "questions": [],
        "answers": {},     # <-- should be a dict
        "options": [],
        "result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_all():
    st.session_state.questions = []
    st.session_state.answers = {}
    st.session_state.options = []
    st.session_state.result = None
    st.session_state.main_purpose = ""
    st.session_state.reset_flag = True
