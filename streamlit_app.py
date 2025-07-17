# streamlit_app.py

import streamlit as st
import requests
import json

# ─── CONFIG & LOGIC ─────────────────────────────────────────────────────────

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"
TEMPERATURE = 0.7

def call_groq(prompt: str) -> str:
    """Call the Groq API with a single-user message prompt."""
    headers = {
        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE
    }
    res = requests.post(GROQ_API_URL, json=body, headers=headers)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

def safe_json_array(text: str) -> list:
    """Extract and parse the first JSON array from a text blob."""
    try:
        start = text.index('[')
        end = text.rindex(']') + 1
        return json.loads(text[start:end])
    except Exception:
        return []

def safe_json_object(text: str) -> dict:
    """Extract and parse the first JSON object from a text blob."""
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return json.loads(text[start:end])
    except Exception:
        return {"decision": "Unknown", "reason": "Could not parse response."}

def generate_questions(purpose: str, options: list[str]) -> list[dict]:
    prompt = f"""
You are a helpful AI in a smart decision-making app.
User asked: "{purpose}"
Options: {', '.join(options)}

Generate 2–3 short clarification questions with 2–4 answer options each.
Return only a JSON array like:
[
  {{
    "text": "Your question?",
    "options": ["Opt A", "Opt B"]
  }},
  ...
]
"""
    return safe_json_array(call_groq(prompt))

def get_final_decision(purpose: str, options: list[str], answers: dict[str,str]) -> dict:
    formatted = "\n\n".join([f"Q: {q}\nA: {a}" for q,a in answers.items()])
    prompt = f"""
Main question: "{purpose}"
Options: {', '.join(options)}
User's answers:
{formatted}

Choose the best option and explain why.
Respond in a JSON object:
{{
  "decision": "Best option",
  "reason": "Why it fits best"
}}
"""
    return safe_json_object(call_groq(prompt))


# ─── SESSION STATE SETUP ────────────────────────────────────────────────────

def init_session():
    if "stage" not in st.session_state:
        st.session_state.stage = "input"          # input → questions → final
    st.session_state.setdefault("main_purpose", "")
    st.session_state.setdefault("options", [])
    st.session_state.setdefault("questions", [])
    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("final_decision", {})


# ─── UI RENDERING ────────────────────────────────────────────────────────────

def render_input():
    st.title("🤔 DillemmAI")
    st.subheader("1️⃣ Describe your dilemma")

    st.session_state.main_purpose = st.text_input(
        "What do you want to decide?", 
        st.session_state.main_purpose
    )

    st.subheader("2️⃣ Add your options")
    cols = st.columns([3,1])
    new_opt = cols[0].text_input("Option", key="new_opt_input")
    if cols[1].button("➕ Add") and new_opt:
        if new_opt not in st.session_state.options:
            st.session_state.options.append(new_opt)
        st.session_state.new_opt_input = ""
        st.experimental_rerun()

    # Display tags
    if st.session_state.options:
        st.markdown("**Options:**")
        tags = "  ".join(f"`{o}`" for o in st.session_state.options)
        st.markdown(tags, unsafe_allow_html=True)

        # Removal dropdown
        remove = st.selectbox("Remove an option:", ["None"] + st.session_state.options)
        if remove != "None":
            st.session_state.options.remove(remove)
            st.experimental_rerun()

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
    st.title("🧠 Clarification Questions")
    with st.form("q_form"):
        answers = {}
        for i, q in enumerate(st.session_state.questions):
            text = q.get("text", f"Question {i+1}")
            opts = q.get("options", [])
            answers[text] = st.radio(text, opts, key=f"radio_{i}")
        if st.form_submit_button("🔍 Get Final Decision"):
            st.session_state.answers = answers
            st.session_state.final_decision = get_final_decision(
                st.session_state.main_purpose,
                st.session_state.options,
                st.session_state.answers
            )
            st.session_state.stage = "final"
            st.experimental_rerun()

def render_final():
    st.title("✅ Here's Your Decision")
    d = st.session_state.final_decision
    st.markdown(f"### 🎯 {d.get('decision','Unknown')}")
    st.write(d.get("reason","No explanation provided."))

    if st.button("🔄 Start Over"):
        for k in ["stage","main_purpose","options","questions","answers","final_decision"]:
            st.session_state.pop(k, None)
        init_session()
        st.experimental_rerun()


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="DillemmAI 🎲", layout="centered")
    # optional: load custom CSS
    try:
        css = open("assets/style.css").read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    init_session()

    if st.session_state.stage == "input":
        render_input()
    elif st.session_state.stage == "questions":
        render_questions()
    else:
        render_final()

if __name__ == "__main__":
    main()
