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
for key in ["questions", "answers", "options"]:
    if key not in st.session_state:
        st.session_state[key] = []

# --- UI Layout ---
st.set_page_config(page_title="🎲 DillemAI", layout="centered")
st.title("🎲 DillemAI")
st.write("Let AI help you make smarter choices, not random ones.")

purpose = st.text_input("💭 What do you want to decide?", placeholder="e.g. What should I eat tonight?")

# --- Tag Input Style Option Input ---
st.subheader("🔘 Enter your options (press 'Add Option' or Enter)")

with st.form("add_option_form", clear_on_submit=True):
    new_option = st.text_input("Type an option", placeholder="e.g. Burger", key="new_option_input")
    submitted = st.form_submit_button("➕ Add Option")
    if submitted and new_option:
        cleaned = new_option.strip().strip(",")
        if cleaned and cleaned not in st.session_state.options:
            st.session_state.options.append(cleaned)

# Display options as removable tags
if st.session_state.options:
    st.write("### Options:")
    cols = st.columns(min(len(st.session_state.options), 4))
    for i, opt in enumerate(st.session_state.options):
        with cols[i % len(cols)]:
            if st.button(f"❌ {opt}", key=f"remove_{opt}"):
                st.session_state.options.remove(opt)

else:
    st.info("Add at least 2 options to continue.")

# --- Generate Questions ---
def fetch_questions():
    options = st.session_state.options
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

# --- Show Questions and Collect Answers ---
if st.session_state.questions:
    st.subheader("🧠 Answer a few smart questions:")
    for q in st.session_state.questions:
        current_val = st.session_state.answers.get(q["text"], q["options"][0])
        answer = st.radio(q["text"], q["options"], key=q["text"], index=q["options"].index(current_val) if current_val in q["options"] else 0)
        st.session_state.answers[q["text"]] = answer

    if st.button("🎯 Get Smart Decision"):
        result = get_final_decision(purpose, st.session_state.options, st.session_state.answers)
        st.success(f"**Decision:** {result['decision']}")
        st.info(f"💡 _{result['reason']}_")
