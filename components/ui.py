# components/ui.py
import streamlit as st
from core.logic import generate_questions, get_final_decision
from core.state import init_session_state


def render_ui():
    """Main UI dispatcher based on the current stage."""
    if st.session_state.stage == "input":
        render_input_stage()
    elif st.session_state.stage == "questions":
        render_questions_stage()
    elif st.session_state.stage == "final_decision":
        render_final_decision_stage()


def render_input_stage():
    """Render the initial input stage with main question and tag-based options."""
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ What's your dilemma?")
    # Main purpose input
    st.session_state.main_purpose = st.text_input(
        "Describe your main goal:",
        st.session_state.main_purpose,
        key="main_purpose_input"
    )

    st.subheader("2️⃣ Enter your options")
    # Tag input style: text input + Add button
    cols = st.columns([3,1])
    new_opt = cols[0].text_input("Option", key="new_option")
    if cols[1].button("Add") and new_opt:
        if new_opt not in st.session_state.options:
            st.session_state.options.append(new_opt)
        st.session_state.new_option = ""
        st.experimental_rerun()

    # Display existing options as tags with remove buttons
    if st.session_state.options:
        tag_cols = st.columns(len(st.session_state.options))
        for i, opt in enumerate(st.session_state.options):
            with tag_cols[i]:
                st.markdown(f"<div style='display:inline-block;padding:4px 8px;border-radius:12px;background:#007bff;color:#fff;'>`{opt}` <a href='javascript:void(0)' style='color:#fff;text-decoration:none;' onclick='delete_option({i})'>×</a></div>", unsafe_allow_html=True)
        # Note: removal via callbacks isn't native; fallback to remove in next cycle
        # Use a selectbox to remove for simplicity
        remove_idx = st.selectbox("Remove option?", ["None"] + st.session_state.options, key="remove_select")
        if remove_idx != "None":
            st.session_state.options.remove(remove_idx)
            st.experimental_rerun()

    # Proceed button
    if st.button("🚀 Generate Follow-up Questions"):
        if not st.session_state.main_purpose:
            st.error("Please enter a main question.")
        elif len(st.session_state.options) < 2:
            st.error("Please add at least two options.")
        else:
            st.session_state.questions = generate_questions(
                st.session_state.main_purpose,
                st.session_state.options
            )
            st.session_state.stage = "questions"
            st.experimental_rerun()


def render_questions_stage():
    """Render the clarification questions stage."""
    st.title("🧠 Help me understand better")
    with st.form("questions_form"):
        answers = {}
        for idx, q in enumerate(st.session_state.questions):
            text = q.get("text", "Question")
            opts = q.get("options", [])
            answers[text] = st.radio(text, opts, key=f"q_{idx}")
        submitted = st.form_submit_button("🔍 Get Smart Decision")
        if submitted:
            st.session_state.answers = answers
            st.session_state.final_decision = get_final_decision(
                st.session_state.main_purpose,
                st.session_state.options,
                st.session_state.answers
            )
            st.session_state.stage = "final_decision"
            st.experimental_rerun()


def render_final_decision_stage():
    """Render the final decision stage with result and restart option."""
    st.title("✅ Here's your best choice")
    dec = st.session_state.final_decision
    # dec is expected as dict with keys decision and reason
    if isinstance(dec, dict):
        st.markdown(f"### 🎯 {dec.get('decision', 'Unknown')} ")
        st.write(dec.get('reason', 'No explanation.'))
    else:
        # fallback if dec is string
        st.write(dec)

    if st.button("🔄 Start Over"):
        for key in ["stage", "main_purpose", "options", "questions", "answers", "final_decision"]:
            st.session_state.pop(key, None)
        init_session_state()
        st.experimental_rerun()
