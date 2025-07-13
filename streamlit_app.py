import streamlit as st
import requests
import json

# --- Setup ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- Helper Functions ---
def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    res = requests.post(GROQ_API_URL, headers=headers, json=body)
    return res.json()["choices"][0]["message"]["content"]

def safe_json_array(text):
    try:
        start = text.index('[')
        end = text.rindex(']') + 1
        return json.loads(text[start:end])
    except:
        return []

def safe_json_object(text):
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return json.loads(text[start:end])
    except:
        return {"decision": "Unknown", "reason": "Could not parse the response."}

def generate_questions(purpose, options):
    prompt = f"""
You are a helpful AI in a smart decision-making app.
User asked: "{purpose}"
Options: {', '.join(options)}

Generate 2–3 short clarification questions with 2–4 answer options each.
Format:
[
  {{
    "text": "Your question?",
    "options": ["Option A", "Option B"]
  }}
]
"""
    return safe_json_array(call_groq(prompt))

def get_final_decision(purpose, options, answers):
    formatted = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])
    prompt = f"""
Main question: "{purpose}"
Options: {', '.join(options)}
User's answers:
{formatted}

Choose the best option and explain why.
Respond in:
{{
  "decision": "Best option",
  "reason": "Why"
}}
"""
    return safe_json_object(call_groq(prompt))

# --- Session State ---
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- UI Layout ---
st.set_page_config(page_title="🎲 DillemAI", layout="centered")
st.title("🎲 DillemAI")
st.write("Let AI help you make smarter choices, not random ones.")

purpose = st.text_input("💭 What do you want to decide?", placeholder="e.g. What should I eat tonight?")

# --- Option tag input system ---
st.subheader("🔘 Add decision options")
if "options" not in st.session_state:
    st.session_state.options = []

# Input box to enter one option at a time
new_option = st.text_input("Type option and press Enter", key="new_option_input")

# Add on Enter or comma
if new_option and (st.session_state.get("last_option") != new_option):
    cleaned = new_option.strip().strip(",")
    if cleaned and cleaned not in st.session_state.options:
        st.session_state.options.append(cleaned)
    st.session_state.last_option = new_option
    st.experimental_rerun()  # Instant refresh

# Show all current tags
if st.session_state.options:
    st.write("### Options:")
    cols = st.columns(len(st.session_state.options))
    for i, opt in enumerate(st.session_state.options):
        with cols[i]:
            remove = st.button(f"❌ {opt}", key=f"remove_{opt}")
            if remove:
                st.session_state.options.remove(opt)
                st.experimental_rerun()
else:
    st.info("Enter at least 2 options.")

def fetch_questions():
    options = [o.strip() for o in options_input.split(",") if o.strip()]
    if not purpose or len(options) < 2:
        st.warning("Please enter a valid question and at least 2 options.")
        return
    questions = generate_questions(purpose, options)
    if not questions:
        st.error("Groq didn't return any questions.")
    else:
        st.session_state.questions = questions
        st.session_state.answers = {}

st.button("🚀 Generate Questions", on_click=fetch_questions)

if st.session_state.questions:
    st.subheader("🧠 Answer a few smart questions:")
    for q in st.session_state.questions:
        current_val = st.session_state.answers.get(q["text"], q["options"][0])
        answer = st.radio(q["text"], q["options"], key=q["text"], index=q["options"].index(current_val) if current_val in q["options"] else 0)
        st.session_state.answers[q["text"]] = answer

    if st.button("🎯 Get Smart Decision"):
        options = [o.strip() for o in options_input.split(",") if o.strip()]
        result = get_final_decision(purpose, options, st.session_state.answers)
        st.success(f"**Decision:** {result['decision']}")
        st.info(f"💡 _{result['reason']}_")
