import requests
import json
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    res = requests.post(GROQ_API_URL, headers=headers, json=payload)
    res.raise_for_status()
    data = res.json()
    return data["choices"][0]["message"]["content"]

def safe_json_array(text):
    try:
        start = text.index('[')
        end = text.rindex(']') + 1
        return json.loads(text[start:end])
    except Exception as e:
        st.error(f"Array parse error: {e}")
        return []

def safe_json_object(text):
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return json.loads(text[start:end])
    except Exception as e:
        st.error(f"Object parse error: {e}")
        return {"decision": "Unknown", "reason": "Parsing failed."}

def generate_questions(purpose, options):
    prompt = f"""
You are a helpful AI in a smart decision-making app.
User wants to decide: "{purpose}"
Their options: {", ".join(options)}
Generate 2–3 short questions with 2–4 multiple-choice options each.
Return only this JSON format:
[
  {{
    "text": "Question?",
    "options": ["Option A", "Option B"]
  }}
]
"""
    response = call_groq(prompt)
    return safe_json_array(response)

def get_final_decision(purpose, options, answers):
    answer_lines = "\n\n".join([f"Q{i+1}: {q}\nA: {a}" for i, (q, a) in enumerate(answers.items())])
    prompt = f"""
You are a smart assistant that helps users make decisions.
Main question: "{purpose}"
Options: {", ".join(options)}
Answers:
{answer_lines}
Now choose the best option and explain why.
Return in JSON:
{{
  "decision": "Best option",
  "reason": "Explanation"
}}
"""
    response = call_groq(prompt)
    return safe_json_object(response)
