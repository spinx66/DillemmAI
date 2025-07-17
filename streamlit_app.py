# streamlit_app.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state
from components.ui import render_ui

st.set_page_config(page_title="DillemmAI", layout="centered")
st.markdown("<style>" + open("assets/style.css").read() + "</style>", unsafe_allow_html=True)

init_session_state()
render_ui()
