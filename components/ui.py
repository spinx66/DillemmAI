# components/ui.py

import streamlit as st

def render_header():
    st.markdown("""
    <div class="app-container">
      <header class="app-header">
        <h1>🎲 DilemmAI</h1>
        <p class="subtitle">Let AI make your choices smarter, not random.</p>
      </header>
    """, unsafe_allow_html=True)

def render_input_section():
    st.markdown("<section class='input-section'>", unsafe_allow_html=True)

    purpose = st.text_input(
        "What do you want to decide?",
        key="main_purpose",
        placeholder="e.g., What should I eat today?",
        label_visibility="collapsed"
    )

    st.markdown("<label class='input-label'>Enter options (press Add or Enter):</label>", unsafe_allow_html=True)

    with st.form("add_option_form", clear_on_submit=True):
        new_option = st.text_input("", placeholder="Type and press Enter...", key="option_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Add Option")
        if submitted and new_option:
            val = new_option.strip().strip(",")
            if val and val not in st.session_state.options:
                st.session_state.options.append(val)

    return purpose

def render_tags():
    if st.session_state.options:
        st.markdown("<div class='tag-container'>", unsafe_allow_html=True)
        for i, tag in enumerate(st.session_state.options):
            col = st.columns([0.05, 0.9, 0.05])[1]
            with col:
                st.markdown(f"""
                <div class='tag'>
                  {tag} <span onclick=\"window.location.href='/?remove_tag={i}'\">×</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_question_section(purpose):
    if st.session_state.questions:
        st.markdown("<section class='question-section'>", unsafe_allow_html=True)
        for q in st.session_state.questions:
            st.markdown("<div class='question-block'>", unsafe_allow_html=True)
            answer = st.radio(q["text"], q["options"], key=q["text"])
            st.session_state.answers[q["text"]] = answer
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</section>", unsafe_allow_html=True)

def render_result_box(purpose):
    from core.logic import get_final_decision

    if st.session_state.questions and st.button("🔍 Get Smart Result"):
        result = get_final_decision(purpose, st.session_state.options, st.session_state.answers)
        st.markdown(f"""
        <section class='result-box'>
        🎯 <strong>Decision:</strong> {result['decision']}<br>
        💡 <em>{result['reason']}</em>
        </section>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # Close .app-container
