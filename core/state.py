# core/state.py
import streamlit as st

def init_session_state():
    """Initialize all required keys in session_state before UI access."""
    # stage management
    st.session_state.setdefault("stage", "input")  # input -> questions -> final

    # main input
    st.session_state.setdefault("main_purpose", "")

    # options list and input buffer
    st.session_state.setdefault("options", [])
    st.session_state.setdefault("new_opt", "")

    # removal buffer
    st.session_state.setdefault("remove_opt", "None")

    # questions and answers
    st.session_state.setdefault("questions", [])
    st.session_state.setdefault("answers", {})

    # final decision storage
    st.session_state.setdefault("final_decision", {})
