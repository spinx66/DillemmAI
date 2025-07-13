# streamlit_app.py

import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state, handle_tag_removal
from components.ui import (
    render_header,
    render_input_section,
    render_tags,
    render_question_section,
    render_result_box
)

st.set_page_config(page_title="🎲 DilemmAI", layout="centered")

st.markdown("""
<script>
const observer = new MutationObserver(() => {
  const theme = window.getComputedStyle(document.documentElement).getPropertyValue('--background-color');
  const isDark = getComputedStyle(document.body).backgroundColor === 'rgb(14, 17, 23)';
  document.body.classList.remove('dark-mode', 'light-mode');
  document.body.classList.add(isDark ? 'dark-mode' : 'light-mode');
});
observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
</script>
""", unsafe_allow_html=True)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize state
init_session_state()
handle_tag_removal()

render_header()
purpose = render_input_section()
render_tags()

if st.button("🚀 Decide My Fate", key="decide_button"):
    if not purpose or len(st.session_state.options) < 2:
        st.warning("Enter a valid question and at least two options.")
    else:
        st.session_state.questions = generate_questions(purpose, st.session_state.options)
        st.session_state.answers = {}

render_question_section(purpose)
render_result_box(purpose)
