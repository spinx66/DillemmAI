# core/state.py
import streamlit as st

def init_session_state():
    """Initialize all required keys in session_state."""
    # UI stage: input -> questions -> final
    st.session_state.setdefault("stage", "input")
    # Dilemma inputs
    st.session_state.setdefault("main_purpose", "")
    st.session_state.setdefault("options", [])
    # Input field buffer for new option
    st.session_state.setdefault("new_opt", "")
    # Clarification questions and answers
    st.session_state.setdefault("questions", [])
    st.session_state.setdefault("answers", {})
    # Final decision storage
    st.session_state.setdefault("final_decision", {})
    # Removal dropdown buffer
    st.session_state.setdefault("remove_opt", "None")
