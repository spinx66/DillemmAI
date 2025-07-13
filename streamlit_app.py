import streamlit as st
import requests
import json

# --- Setup ---
st.set_page_config(page_title="🎲 DillemAI", layout="centered")
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

# --- State ---
for key in ["questions", "answers", "options"]:
    if key not in st.session_state:
        st.session_state[key] = []

# --- CSS Injection ---
st.markdown("""
<style>
    .app-title {
        text-align: center;
        font-size: 2.5em;
        font-weight: 600;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: #777;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .tag-button {
        background-color: #eee;
        border: none;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 4px;
        cursor: pointer;
        font-size: 0.9em;
    }
    .tag-button:hover {
        background-color: #ccc;
    }
</style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown("<h1 class='app-title'>🎲 DillemAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Let AI make your choices smarter, not random.</p>", unsafe_allow_html=True)

st.subheader("💭 What do you want to decide?")
purpose = st.text_input("", placeholder="e.g. Should I launch this feature?")

st.subheader("🏷️ Your Options")

# Add option input
with st.form("option_form", clear_on_submit=True):
    new_opt = st.text_input("Type and press Add", placeholder="e.g. Build new feature")
    add_btn = st.form_submit_button("➕ Add Option")
    if add_btn and new_opt:
        val = new_opt.strip().strip(",")
        if val and val not in st.session_state.options:
            st.session_state.options.append(val)

# Style tags using HTML
st.markdown("""
<style>
.tag-pill {
    display: inline-block;
    background-color: #f1f1f1;
    color: #333;
    border-radius: 20px;
    padding: 6px 12px;
    margin: 5px 6px 5px 0;
    font-size: 0.9em;
    position: relative;
}
.tag-pill:hover {
    background-color: #e0e0e0;
}
.tag-pill button {
    border: none;
    background: none;
    color: #999;
    margin-left: 8px;
    font-size: 1em;
    cursor: pointer;
    position: absolute;
    top: 2px;
    right: 6px;
}
.tag-pill button:hover {
    color: red;
}
</style>
""", unsafe_allow_html=True)

# Render each tag with a working remove button
for i, tag in enumerate(st.session_state.options):
    col = st.columns([1, 5, 1])[1]  # center column
    with col:
        tag_html = f"""
        <div class="tag-pill">
            {tag}
            <form action="" method="post">
                <button name="remove_tag" value="{i}">&times;</button>
            </form>
        </div>
        """
        st.markdown(tag_html, unsafe_allow_html=True)

# Process tag remove if triggered
remove_index = st.experimental_get_query_params().get("remove_tag")
if st.session_state.get("remove_tag"):
    index = int(st.session_state.remove_tag)
    if 0 <= index < len(st.session_state.options):
        del st.session_state.options[index]
        st.session_state.remove_tag = None
elif "remove_tag" in st.query_params:
    del_index = int(st.query_params["remove_tag"][0])
    if 0 <= del_index < len(st.session_state.options):
        st.session_state.options.pop(del_index)
        st.experimental_rerun()

if st.session_state.options:
    cols = st.columns(min(4, len(st.session_state.options)))
    for i, opt in enumerate(st.session_state.options):
        with cols[i % 4]:
            if st.button(f"❌ {opt}", key=f"rm_{opt}"):
                st.session_state.options.remove(opt)

# --- Generate Questions ---
if st.button("🚀 Generate Smart Questions"):
    if not purpose or len(st.session_state.options) < 2:
        st.warning("Please enter a purpose and at least 2 options.")
    else:
        st.session_state.questions = generate_questions(purpose, st.session_state.options)
        st.session_state.answers = {}

# --- Show Questions ---
if st.session_state.questions:
    st.subheader("🧠 Help me understand better:")
    for q in st.session_state.questions:
        answer = st.radio(q["text"], q["options"], key=q["text"])
        st.session_state.answers[q["text"]] = answer

    if st.button("🎯 Get Smart Decision"):
        result = get_final_decision(purpose, st.session_state.options, st.session_state.answers)
        st.success(f"**Decision:** {result['decision']}")
        st.info(f"💡 _{result['reason']}_")
