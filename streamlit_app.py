import streamlit as st
import requests
import json

# --- Setup ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

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

# --- UI ---
st.set_page_config(page_title="🎲 DillemAI", layout="centered")
st.title("🎲 DillemAI")
st.write("Let AI help you make smarter choices, not random ones.")

purpose = st.text_input("💭 What do you want to decide?", placeholder="e.g. What should I eat tonight?")
options_input = st.text_input("🔘 Enter options (comma-separated)", placeholder="Pizza, Burger, Salad")

if st.button("🚀 Generate Questions"):
    if not purpose or not options_input:
        st.warning("Please enter both a main question and at least 2 options.")
    else:
        options = [o.strip() for o in options_input.split(",") if o.strip()]
        if len(options) < 2:
            st.warning("You need at least 2 options.")
        else:
            questions = generate_questions(purpose, options)
            if not questions:
                st.error("Groq didn't return any questions.")
            else:
                answers = {}
                st.subheader("🧠 Answer a few smart questions:")
                for q in questions:
                    answers[q["text"]] = st.radio(q["text"], q["options"], key=q["text"])
                
                if st.button("🎯 Get Smart Decision"):
                    result = get_final_decision(purpose, options, answers)
                    st.success(f"**Decision:** {result['decision']}")
                    st.info(f"💡 _{result['reason']}_")
