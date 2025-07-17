# components/ui.py
import streamlit as st
from core.state import init_session_state
from core.logic import generate_questions, get_final_decision

def render_ui():
    if st.session_state.stage == "input":
        render_input_stage()
    elif st.session_state.stage == "questions":
        render_questions_stage()
    elif st.session_state.stage == "final_decision":
        render_final_decision_stage()

def render_input_stage():
    st.title("🤔 DillemmAI")
    st.subheader("What's your dilemma?")
    
    st.session_state.main_purpose = st.text_input("Describe your main goal:", st.session_state.main_purpose)
    
    options_input = st.text_input("Enter your options (comma separated):", placeholder="e.g. Option A, Option B, Option C")
    
    if st.button("Next"):
        st.session_state.main_purpose = purpose
        st.session_state.options = [opt.strip() for opt in options_input.split(",") if opt.strip()]
        
        # Add safety check
        if not st.session_state.options or len(st.session_state.options) < 2:
            st.warning("Please enter at least 2 valid options.")
            return
    
        st.session_state.stage = "questions"

def render_questions_stage():
    st.title("🧠 Help me understand better")
    with st.form("questions_form"):
        for q in st.session_state.questions:
            if q not in st.session_state.answers:
                st.session_state.answers[q] = ""
            st.session_state.answers[q] = st.radio(q, ["More", "Less", "Depends"], index=2, key=q)
        if st.form_submit_button("Get Final Decision"):
            st.session_state.final_decision = get_final_decision(
                st.session_state.main_purpose,
                st.session_state.options,
                st.session_state.questions,
                st.session_state.answers
            )
            st.session_state.stage = "final_decision"
            st.rerun()

def render_final_decision_stage():
    st.title("✅ Here's your best choice")
    st.markdown(f"### {st.session_state.final_decision}")

    if st.button("Start Over"):
        for key in ["stage", "main_purpose", "options", "questions", "answers", "final_decision"]:
            del st.session_state[key]
        init_session_state()
        st.rerun()
