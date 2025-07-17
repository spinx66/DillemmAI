# components/ui.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state

def render_ui():
    """Dispatch to the appropriate UI stage based on session_state.stage."""
    stage = st.session_state.stage
    if stage == "input":
        render_input()
    elif stage == "questions":
        render_questions()
    elif stage == "final":
        render_final()

def render_input():
    """Render the input stage: main question and tag-style option inputs."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ Describe your dilemma")

    # Main question input
    st.session_state.main_purpose = st.text_input(
        "What do you want to decide?",
        st.session_state.main_purpose,
        key="main_input"
    )

    # Options input
    st.subheader("2️⃣ Add your options")
    cols = st.columns([3, 1])
    new_opt = cols[0].text_input("Option")
    if cols[1].button("➕ Add") and new_opt:
        if new_opt not in st.session_state.options:
            st.session_state.options.append(new_opt)
        # No direct state modification of text_input after creation
        

    # Display current options as tags
    if st.session_state.options:
        st.markdown("**Options:**")
        tags_md = "  ".join(f"{o}" for o in st.session_state.options)
        st.markdown(tags_md, unsafe_allow_html=True)

        # Removal dropdown
        remove = st.selectbox(
            "Remove an option:",
            ["None"] + st.session_state.options,
            key="remove_select"
        )
        if remove != "None":
            st.session_state.options.remove(remove)
            

    # Generate questions button
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
            

def render_questions():
    """Render clarification questions and collect answers."""
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
        if st.form_submit_button("🔍 Get Final Decision"):
            st.session_state.answers = answers
            st.session_state.final_decision = get_final_decision(
                st.session_state.main_purpose,
                st.session_state.options,
                st.session_state.answers
            )
            st.session_state.stage = "final"
            

def render_final():
    """Render the final decision result and restart button."""
    st.title("✅ Here's Your Decision")
    d = st.session_state.final_decision
    if isinstance(d, dict):
        st.markdown(f"### 🎯 {d.get('decision', 'Unknown')}")
        st.write(d.get('reason', 'No explanation provided.'))
    else:
        st.write(d)

    if st.button("🔄 Start Over"):
        for key in ["stage", "main_purpose", "options", "questions", "answers", "final_decision"]:
            st.session_state.pop(key, None)
        init_session_state()
        
