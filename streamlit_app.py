# streamlit_app.py

import streamlit as st
from core.logic import generate_questions, get_final_decision
from components.ui import (
    render_header,
    render_input_section,
    render_tags,
    render_question_section,
    render_result_box,
    render_reset_button
)

st.set_page_config(page_title="🎲 DilemmAI", layout="centered")

st.markdown("""
<script>
function detectDarkMode() {
  const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  document.body.classList.remove('dark-mode', 'light-mode');
  document.body.classList.add(dark ? 'dark-mode' : 'light-mode');
}
detectDarkMode();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', detectDarkMode);
</script>
""", unsafe_allow_html=True)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize state
init_session_state()

render_header()
purpose = render_input_section()
render_tags()

print("🔧 Reset button rendered!")
render_reset_button()

# 🚀 Main Action Button
if st.button("🚀 Decide My Fate", key="decide_button"):
    if not purpose or len(st.session_state.options) < 2:
        st.warning("Enter a valid question and at least two options.")
    else:
        st.session_state.questions = generate_questions(purpose, st.session_state.options)
        st.session_state.answers = {}

render_question_section(purpose)
render_result_box(purpose)
