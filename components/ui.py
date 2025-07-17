# components/ui.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state

def render_ui():
    """Dispatch to the appropriate UI stage."""
    stage = st.session_state.stage
    if stage == "input":
        render_input()
    elif stage == "questions":
        render_questions()
    elif stage == "final":
        render_final()

def render_input():
    """Input stage: get main question and options via tag-style inputs."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ Describe your dilemma")

    st.session_state.main_purpose = st.text_input(
        "What do you want to decide?",
        st.session_state.main_purpose,
        key="main_input"
    )

    st.subheader("2️⃣ Add your options")
    cols = st.columns([3, 1])
    new_opt = cols[0].text_input("Option", key="new_opt")
    if cols[1].button("➕ Add") and new_opt:
        if new_opt not in st.session_state.options:
            st.session_state.options.append(new_opt)
        st.session_state.new_opt = ""
        st.experimental_rerun()

    # Display tags
    if st.session_state.options:
        st.markdown("**Options:**")
        tags = "  ".join(f"`{o}`" for o in st.session_state.options)
        st.markdown(tags, unsafe_allow_html=True)
        # Removal dropdown
        remove = st.selectbox(
            "Remove an option:",
            ["None"] + st.session_state.options,
            key="remove_opt"
        )
        if remove != "None":
            st.session_state.options.remove(remove)
            st.experimental_rerun()

    # Proceed
    if st.button("🚀 Generate Follow‑up Questions"):
        if not st.session_state.main_purpose:
            st.error("⚠️ Please enter your main question.")
        elif len(st.session_state.options) < 2:
            st.error("⚠️ Add at least two options.")
        else:
            st.session_state.questions = generate_questions(
                st.session_state.main_purpose,
                st.session_state.options
            )
            st.session_state.stage = "questions"
            st.experimental_rerun()

def render_questions():
    """Questions stage: show follow-ups and collect answers."""
    st.title("🧠 Clarification Questions")
    with st.form("questions_form"):
        answers = {}
        for i, q in enumerate(st.session_state.questions):
            text = q.get("text", f"Question {i+1}")
            opts = q.get("options", [])
            answers[text] = st.radio(
                text,
                opts,
                key=f"radio_{i}"
            )
        submitted = st.form_submit_button("🔍 Get Final Decision")
        if submitted:
            st.session_state.answers = answers
            st.session_state.final_decision = get_final_decision(
                st.session_state.main_purpose,
                st.session_state.options,
                st.session_state.answers
            )
            st.session_state.stage = "final"
            st.experimental_rerun()

def render_final():
    """Final stage: display the decision and reason, with restart option."""
    st.title("✅ Here's Your Decision")
    d = st.session_state.final_decision
    # If dict
    if isinstance(d, dict):
        st.markdown(f"### 🎯 {d.get('decision', 'Unknown')}")
        st.write(d.get('reason', 'No explanation provided.'))
    else:
        st.write(d)

    if st.button("🔄 Start Over"):
        for key in ["stage", "main_purpose", "options", "questions", "answers", "final_decision"]:
            st.session_state.pop(key, None)
        init_session_state()
        st.experimental_rerun()
