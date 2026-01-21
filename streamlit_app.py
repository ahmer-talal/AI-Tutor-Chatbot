import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Tutor Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Tutor Chatbot")
st.caption("Ask questions related to AI, ML, DL, CNNs, LLMs")

# ---------- GROQ CLIENT ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Session Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "greeted" not in st.session_state:
    st.session_state.greeted = False

# Initial Greeting  
if not st.session_state.greeted:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "👋 Hi! I’m your AI Tutor designed by **Ahmer Talal**. Ask me anything related to AI, ML, DL, Autoencoders, or LLMs."
    })
    st.session_state.greeted = True

# Constraints for AI-related questions  
AI_TOPICS = [
    "ai", "machine learning", "deep learning",
    "cnn", "rnn","ann", "transformer", "llm",
    "neural network", "autoencoder",
    "computer vision", "nlp"
]

def is_ai_related(text):
    return any(topic in text.lower() for topic in AI_TOPICS)


# User Input/Difficulty Level Selection
st.sidebar.title("⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Choose difficulty level",
    ["Beginner", "Intermediate", "Advanced"]
)

# Topic Suggestion Buttons
st.sidebar.markdown("### 💡 Suggested Topics")

suggested = [
    "What is CNN?",
    "Autoencoder vs CNN",
    "What are LLMs?",
    "How transformers work?"
]

for topic in suggested:
    if st.sidebar.button(topic):
        st.session_state.chat_history.append(
            {"role": "user", "content": topic}
        )

# Chat Input + Display History
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask an AI question...")


# API Call
def get_ai_response(user_input, difficulty):
    if not is_ai_related(user_input):
        return "Sorry! I am designed to only answer AI-related questions."

    system_prompt = f"""
You are an AI tutor.
Explain concepts at {difficulty.lower()} level.
Stay within AI/ML topics only.
"""

    with st.spinner("🤖 Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

    return response.choices[0].message.content


# Append Messages to Memory
if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    reply = get_ai_response(user_input, difficulty)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

# Clear Chat Button 
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.greeted = False
    st.rerun()
