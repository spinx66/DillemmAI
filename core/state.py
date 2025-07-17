# core/state.py
import streamlit as st

def init_session_state():
    if "stage" not in st.session_state:
        st.session_state.stage = "input"  # stages: input → questions → final_decision

    if "main_purpose" not in st.session_state:
        st.session_state.main_purpose = ""

    if "options" not in st.session_state:
        st.session_state.options = []

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "final_decision" not in st.session_state:
        st.session_state.final_decision = ""
