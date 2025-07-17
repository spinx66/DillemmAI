import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state

# Initialize state to ensure keys exist before rendering
init_session_state()

def render_ui():
    """Dispatch UI based on the current phase."""
    phase = st.session_state.phase
    if phase == "input":
        render_input()
    elif phase == "questions":
        render_questions()
    else:
        render_final()


def render_input():
    """Input stage: enter main purpose and options."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ What's your dilemma?")

    # Main question input
    st.session_state.main_purpose = st.text_input(
        label="Your question:",
        value=st.session_state.main_purpose,
        key="main_input"
    )

    # Option tags input
    st.subheader("2️⃣ Add options as tags")
    new_opt = st.text_input(
        label="Add an option and press Enter:",
        key="new_opt_input"
    )
    # Add to options list on Enter
    if new_opt:
        if new_opt not in st.session_state.options:
            st.session_state.options.append(new_opt)
        # Reset the input widget by clearing its value
        st.session_state.new_opt_input = ""

    # Display tags with remove buttons
    if st.session_state.options:
        cols = st.columns(len(st.session_state.options))
        for i, opt in enumerate(st.session_state.options):
            with cols[i]:
                st.markdown(
                    f"<div class='tag'>{opt} <span class='remove' onclick='removeOption({i})'>×</span></div>",
                    unsafe_allow_html=True
                )
        # Removal via selectbox as fallback
        to_remove = st.selectbox(
            "Remove an option:",
            options=["None"] + st.session_state.options,
            key="remove_select"
        )
        if to_remove != "None":
            st.session_state.options.remove(to_remove)
            st.session_state.remove_select = "None"

    # Proceed to generate questions
    if st.button("🚀 Generate Questions"):
        if not st.session_state.main_purpose:
            st.error("Enter your main question!")
            return
        if len(st.session_state.options) < 2:
            st.error("Add at least 2 options!")
            return
        # Generate and switch phase
        st.session_state.questions = generate_questions(
            st.session_state.main_purpose,
            st.session_state.options
        )
        st.session_state.phase = "questions"


def render_questions():
    """Questions stage: show follow-ups and record answers."""
    st.title("🧠 Clarification Questions")
    for idx, q in enumerate(st.session_state.questions):
        # Styled question block
        st.markdown(
            f"<div class='question-block'>{q['text']}</div>",
            unsafe_allow_html=True
        )
        choice = st.radio(
            label="Your choice:",
            options=q.get("options", []),
            key=f"answer_{idx}"
        )
        st.session_state.answers[q['text']] = choice

    # Compute final decision
    if st.button("🔍 Get Final Decision"):
        st.session_state.final_decision = get_final_decision(
            st.session_state.main_purpose,
            st.session_state.options,
            st.session_state.answers
        )
        st.session_state.phase = "final"


def render_final():
    """Final stage: display AI's decision and restart option."""
    st.title("✅ Smart Decision")
    result = st.session_state.final_decision
    if isinstance(result, dict):
        st.markdown(f"### 🎯 {result.get('decision', 'N/A')}")
        st.write(result.get('reason', 'No explanation.'))
    else:
        st.write(result)

    if st.button("🔄 Start Over"):
        # Clear only relevant keys
        for key in ["phase", "main_purpose", "options", "questions", "answers", "final_decision"]:
            if key in st.session_state:
                del st.session_state[key]
        init_session_state()
