# core/state.py

import streamlit as st

def init_session_state():
    for key in ["questions", "answers", "options"]:
        if key not in st.session_state:
            st.session_state[key] = []

def handle_tag_removal():
    query = st.query_params
    if "remove_tag" in query:
        try:
            index = int(query["remove_tag"])
            if 0 <= index < len(st.session_state.options):
                st.session_state.options.pop(index)
                st.query_params.clear()
                st.rerun()
        except:
            pass
