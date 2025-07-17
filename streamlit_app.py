# streamlit_app.py
import streamlit as st
from core.state import init_session_state
from components.ui import render_ui


def main():
    # Page config
    st.set_page_config(page_title="DillemmAI 🎲", layout="centered")
    # Apply custom CSS
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Initialize session state and render appropriate UI
    init_session_state()
    render_ui()


if __name__ == "__main__":
    main()
