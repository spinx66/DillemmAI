# components/ui.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state

# Ensure session state is initialized
init_session_state()


def render_ui():
    """Dispatch to the appropriate UI stage based on session_state.phase."""
    phase = st.session_state.phase
    if phase == "input":
        render_input()
    elif phase == "questions":
        render_questions()
    else:
        render_final()


def render_input():
    """Input stage: collect main question and options in a single form."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ Describe your dilemma & options")

    # Use a form to capture inputs and handle one-click submit
    with st.form(key="input_form"):
        # Main question field
        main_q = st.text_input(
            label="What do you want to decide?",
            value=st.session_state.main_purpose,
            key="main_input"
        )
        # Options field: one per line
        opts_text = st.text_area(
            label="Enter options (one per line):",
            value="\n".join(st.session_state.options),
            key="options_input",
            height=100
        )
        # Submit button for form
        submitted = st.form_submit_button(label="🚀 Generate Questions")

    if submitted:
        # Update session state
        st.session_state.main_purpose = main_q
        st.session_state.options = [o.strip() for o in opts_text.splitlines() if o.strip()]

        # Validate inputs
        if not st.session_state.main_purpose:
            st.error("⚠️ Please enter your main question.")
            return
        if len(st.session_state.options) < 2:
            st.error("⚠️ Please enter at least two options.")
            return

        # Generate questions and move phase
        st.session_state.questions = generate_questions(
            st.session_state.main_purpose,
            st.session_state.options
        )
        st.session_state.phase = "questions"


def render_questions():
    """Render generated follow-up questions and collect answers in a form."""
    st.title("🧠 Clarification Questions")
    with st.form(key="questions_form"):
        for idx, q in enumerate(st.session_state.questions):
            # Styled question card (CSS class 'question-block')
            st.markdown(
                f"<div class='question-block'>{q['text']}</div>",
                unsafe_allow_html=True
            )
            # Radio options for each question
            choice = st.radio(
                label="",
                options=q.get("options", []),
                key=f"answer_{idx}"
            )
            st.session_state.answers[q['text']] = choice
        # Submit button for answers
        answered = st.form_submit_button(label="🔍 Get Final Decision")

    if answered:
        # Compute final decision and switch phase
        st.session_state.final_decision = get_final_decision(
            st.session_state.main_purpose,
            st.session_state.options,
            st.session_state.answers
        )
        st.session_state.phase = "final"


def render_final():
    """Display the final decision and offer a restart button."""
    st.title("✅ Smart Decision")
    result = st.session_state.final_decision
    if isinstance(result, dict):
        st.markdown(f"### 🎯 {result.get('decision', 'Unknown')}")
        st.write(result.get('reason', 'No explanation provided.'))
    else:
        st.write(result)

    # Restart clears all relevant state and returns to input
    if st.button("🔄 Start Over"):
        for key in ["phase", "main_purpose", "options", "questions", "answers", "final_decision"]:
            st.session_state.pop(key, None)
        init_session_state()
