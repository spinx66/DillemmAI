# components/ui.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state

# Initialize session state keys
init_session_state()


def render_ui():
    """Dispatch to the appropriate UI stage based on session_state.stage."""
    stage = st.session_state.stage
    if stage == "input":
        render_input()
    elif stage == "questions":
        render_questions()
    else:
        render_final()


def render_input():
    """Render the input form to collect main question and options."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ Describe your dilemma & options")

    with st.form(key="input_form"):
        # Main question text input
        main_q = st.text_input(
            label="What do you want to decide?",
            value=st.session_state.main_purpose,
            key="main_input"
        )
        # Options textarea: one per line
        opts_text = st.text_area(
            label="Enter options (one per line):",
            value="\n".join(st.session_state.options),
            key="options_input",
            height=100
        )
        # Submit button for the form
        submitted = st.form_submit_button(label="🚀 Generate Questions")

    if submitted:
        # Update state
        st.session_state.main_purpose = main_q
        st.session_state.options = [o.strip() for o in opts_text.splitlines() if o.strip()]

        # Validation
        if not st.session_state.main_purpose:
            st.error("⚠️ Please enter your main question.")
            return
        if len(st.session_state.options) < 2:
            st.error("⚠️ Please enter at least two options.")
            return

        # Generate questions and update stage
        st.session_state.questions = generate_questions(
            st.session_state.main_purpose,
            st.session_state.options
        )
        st.session_state.stage = "questions"


def render_questions():
    """Render generated follow-up questions and collect user answers."""
    st.title("🧠 Clarification Questions")
    with st.form(key="questions_form"):
        # Loop through each question
        for idx, q in enumerate(st.session_state.questions):
            # Show styled question card
            st.markdown(
                f"<div class='question-block'>{q['text']}</div>",
                unsafe_allow_html=True
            )
            # Display radio options
            choice = st.radio(
                label="",
                options=q.get("options", []),
                key=f"answer_{idx}"
            )
            st.session_state.answers[q['text']] = choice
        # Submit answers
        answered = st.form_submit_button(label="🔍 Get Final Decision")

    if answered:
        # Compute final decision
        st.session_state.final_decision = get_final_decision(
            st.session_state.main_purpose,
            st.session_state.options,
            st.session_state.answers
        )
        st.session_state.stage = "final"


def render_final():
    """Display the final decision and allow restart."""
    st.title("✅ Smart Decision")
    result = st.session_state.final_decision
    if isinstance(result, dict):
        st.markdown(f"### 🎯 {result.get('decision', 'Unknown')}")
        st.write(result.get('reason', 'No explanation provided.'))
    else:
        st.write(result)

    if st.button("🔄 Start Over"):
        # Clear relevant session state keys
        for key in ["stage", "main_purpose", "options", "questions", "answers", "final_decision"]:
            st.session_state.pop(key, None)
        init_session_state()
