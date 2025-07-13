import streamlit as st
import groq_api
import json

st.set_page_config(page_title="DillemAI Backend API", layout="centered")
st.title("🧠 DillemAI Backend")

st.markdown("This backend provides two API endpoints using Groq:")

# Endpoint 1: Generate Questions
if st.button("Test Generate Questions"):
    example_purpose = "Where should I go this weekend?"
    example_options = ["Beach", "Mountains", "City"]
    questions = groq_api.generate_questions(example_purpose, example_options)
    st.json(questions)

# Endpoint 2: Get Final Decision
if st.button("Test Final Decision"):
    purpose = "Where should I go this weekend?"
    options = ["Beach", "Mountains", "City"]
    sample_answers = {
        "Do you prefer calm or adventure?": "Adventure",
        "Budget high or low?": "Low"
    }
    result = groq_api.get_final_decision(purpose, options, sample_answers)
    st.json(result)
