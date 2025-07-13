# 🎲 DilemmAI

**Let AI make your choices smarter, not random.**

DilemmAI is an interactive Streamlit app powered by Groq's LLaMA 3 model. It helps you make thoughtful decisions by:

1. Asking clarifying questions based on your goal
2. Understanding your preferences
3. Suggesting the most suitable option

---

## 🚀 Features

- 🎯 Input any dilemma or choice
- 🏷️ Add custom options using smart tags
- 🧠 Automatically generates 2–3 intelligent follow-up questions
- 🤖 Final decision with reasoning using LLaMA 3
- 🌗 Responsive design with light/dark theme support

---

## 🛠️ Project Structure

```
📁 dillemmai
├── streamlit_app.py         # Main Streamlit entry point
├── core
│   ├── logic.py             # Handles Groq prompt generation and response parsing
│   └── state.py             # Manages session state and tag removal
├── components
│   └── ui.py                # Handles UI rendering for header, form, tags, etc.
├── assets
│   └── style.css            # Custom styles (dark/light mode supported)
└── README.md
```

---

## 🔐 Setup & Deployment

1. **Clone the repo**
```bash
git clone https://github.com/your-username/dillemmai.git
cd dillemmai
```

2. **Install dependencies**
```bash
pip install streamlit requests
```

3. **Add secrets**
Create `.streamlit/secrets.toml` and paste:
```toml
GROQ_API_KEY = "your_groq_api_key"
```

4. **Run the app**
```bash
streamlit run streamlit_app.py
```

---

## 🌐 Hosted On
[Streamlit Cloud](https://streamlit.io/cloud) — Free, fast, and perfect for hosting AI demos.

---

## 📌 Todo

- [x] Modularize codebase
- [x] Add dark/light mode support
- [ ] Unit tests
- [ ] Better error handling
- [ ] SarcasticBot as next project 🔥

---

## 👨‍💻 Built with
- [Streamlit](https://streamlit.io/)
- [Groq API](https://console.groq.com)
- [LLaMA 3](https://groq.com/models)

---

## ⚡ Author
Made with love and chaos by **Spinx** 💥
