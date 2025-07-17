# streamlit_app.py

import streamlit as st
from core.logic import generate_questions, get_final_decision

st.set_page_config(page_title="DillemAI 🎲", page_icon="🎲", layout="centered")

st.title("🎲 DillemAI")
st.caption("Let AI make your choices smarter, not random.")

# --- Input: Main Question & Options ---
st.subheader("1. What's the dilemma?")
main_question = st.text_input("Main question", placeholder="e.g., What should I eat today?")

st.subheader("2. Enter your options")
if "options" not in st.session_state:
    st.session_state.options = []

new_option = st.text_input("Type an option and press Enter", key="option_input")
if new_option:
    if new_option not in st.session_state.options:
        st.session_state.options.append(new_option)
    st.session_state.option_input = ""

if st.session_state.options:
    st.write("Your options:")
    st.markdown(" ".join([f"✅ `{opt}`" for opt in st.session_state.options]))

# --- Generate Questions ---
if st.button("🚀 Generate Follow-up Questions"):
    if not main_question:
        st.error("Please enter a main question.")
    elif len(st.session_state.options) < 2:
        st.error("Please add at least two options.")
    else:
        st.session_state.questions = generate_questions(main_question, st.session_state.options)
        st.session_state.answers = {}

# --- Show Follow-up Questions ---
if "questions" in st.session_state and st.session_state.questions:
    st.subheader("3. Answer the follow-up questions")

    for idx, q in enumerate(st.session_state.questions):
        selected = st.radio(q["text"], q["options"], key=f"q_{idx}")
        st.session_state.answers[q["text"]] = selected

    if st.button("🔍 Get Smart Decision"):
        result = get_final_decision(
            main_question,
            st.session_state.options,
            st.session_state.answers
        )
        st.session_state.final_decision = result

# --- Result ---
if "final_decision" in st.session_state:
    st.subheader("🎯 Final Decision")
    st.success(f"**{st.session_state.final_decision['decision']}**")
    st.caption(st.session_state.final_decision["reason"])
