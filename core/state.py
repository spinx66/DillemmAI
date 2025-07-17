# core/state.py
import streamlit as st

def init_session_state():
    """Initialize all required keys in session_state."""
    if "stage" not in st.session_state:
        st.session_state.stage = "input"  # stages: input, questions, final
    st.session_state.setdefault("main_purpose", "")
    st.session_state.setdefault("options", [])
    st.session_state.setdefault("questions", [])
    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("final_decision", {})
