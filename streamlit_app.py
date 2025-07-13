import streamlit as st
import requests
import json

# --- Page Setup ---
st.set_page_config(page_title="🎲 DillemAI", layout="centered")

# --- Constants ---
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
User asked: \"{purpose}\"
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
Main question: \"{purpose}\"
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

# --- Style Injection ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- App Container ---
st.markdown("""
<div class="app-container">
  <header class="app-header">
    <h1>🎲 DilemmAI</h1>
    <p class="subtitle">Let AI make your choices smarter, not random.</p>
  </header>
""", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("<section class='input-section'>", unsafe_allow_html=True)

purpose = st.text_input("What do you want to decide?", key="main_purpose", placeholder="e.g., What should I eat today?", label_visibility="collapsed")

st.markdown("<label class='input-label'>Enter options (press Add or Enter):</label>", unsafe_allow_html=True)
with st.form("add_option_form", clear_on_submit=True):
    new_option = st.text_input("", placeholder="Type and press Enter...", key="option_input", label_visibility="collapsed")
    submitted = st.form_submit_button("Add Option")
    if submitted and new_option:
        val = new_option.strip().strip(",")
        if val and val not in st.session_state.options:
            st.session_state.options.append(val)

# --- Render Tags ---
if st.session_state.options:
    st.markdown("<div class='tag-container'>", unsafe_allow_html=True)
    for i, tag in enumerate(st.session_state.options):
        col = st.columns([0.05, 0.9, 0.05])[1]
        with col:
            st.markdown(f"""
            <div class='tag'>
              {tag} <span onclick="window.location.href='/?remove_tag={i}'">×</span>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Remove Tag via Query Param ---
query = st.experimental_get_query_params()
if "remove_tag" in query:
    try:
        index = int(query["remove_tag"][0])
        if 0 <= index < len(st.session_state.options):
            st.session_state.options.pop(index)
            st.experimental_set_query_params()
            st.experimental_rerun()
    except:
        pass

# --- Start Decision Button ---
if st.button("🚀 Decide My Fate", key="decide_button"):
    if not purpose or len(st.session_state.options) < 2:
        st.warning("Enter a valid question and at least two options.")
    else:
        st.session_state.questions = generate_questions(purpose, st.session_state.options)
        st.session_state.answers = {}

st.markdown("</section>", unsafe_allow_html=True)

# --- Question Section ---
if st.session_state.questions:
    st.markdown("<section class='question-section'>", unsafe_allow_html=True)
    for q in st.session_state.questions:
        st.markdown("<div class='question-block'>", unsafe_allow_html=True)
        answer = st.radio(q["text"], q["options"], key=q["text"])
        st.session_state.answers[q["text"]] = answer
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔍 Get Smart Result"):
        result = get_final_decision(purpose, st.session_state.options, st.session_state.answers)
        st.markdown(f"""
        <section class='result-box'>
        🎯 <strong>Decision:</strong> {result['decision']}<br>
        💡 <em>{result['reason']}</em>
        </section>
        """, unsafe_allow_html=True)

    st.markdown("</section>", unsafe_allow_html=True)

# --- End ---
st.markdown("</div>", unsafe_allow_html=True)
