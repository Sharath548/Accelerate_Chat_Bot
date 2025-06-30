import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import os
import json
from datetime import datetime
from ai_bot.retriever.query_engine import get_context_for_query
from ai_bot.llm.ollama_interface import ask_ollama

st.set_page_config(page_title="SPOS Knowledge Assistant", layout="wide")

# 📁 Create chat_logs directory if not exists
os.makedirs("chat_logs", exist_ok=True)

# 📅 Generate unique session filename
if "session_file" not in st.session_state:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
    st.session_state.session_file = f"chat_logs/history_{timestamp}.json"

# 🔁 Load previous chat from file (if exists)
if os.path.exists(st.session_state.session_file) and "chat_history" not in st.session_state:
    with open(st.session_state.session_file, "r", encoding="utf-8") as f:
        st.session_state.chat_history = json.load(f)
else:
    st.session_state.chat_history = []

if "questions" not in st.session_state:
    st.session_state.questions = [q["content"] for q in st.session_state.chat_history if q["role"] == "user"]
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "last_context" not in st.session_state:
    st.session_state.last_context = None
if "use_memory" not in st.session_state:
    st.session_state.use_memory = True  # Default: ON

# Sidebar: history + controls
with st.sidebar:
    st.title("🗂️ Chat History")

    if st.session_state.questions:
        for i, q in enumerate(reversed(st.session_state.questions)):
            if st.button(q, key=f"load-{i}"):
                st.session_state.current_question = q
    else:
        st.info("No chats yet")

    st.markdown("---")
    st.checkbox("🧠 Enable memory (chat history)", key="use_memory")

    if st.button("🧠 Regenerate Last Response"):
        if st.session_state.last_question and st.session_state.last_context:
            with st.spinner("Regenerating..."):
                chat_thread = st.session_state.chat_history[:-1] if st.session_state.use_memory else []
                answer = ask_ollama(
                    st.session_state.last_question,
                    st.session_state.last_context,
                    chat_history=chat_thread
                )
                st.session_state.chat_history[-1] = {"role": "assistant", "content": answer}

    if st.button("🔁 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.questions = []
        st.session_state.last_question = None
        st.session_state.last_context = None
        with open(st.session_state.session_file, "w", encoding="utf-8") as f:
            f.write("")

# Main title
st.markdown("<h1 style='text-align: center;'>🤖 AI Knowledge Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything based on the files you dropped into <code>input_files/</code>.</p>", unsafe_allow_html=True)
st.markdown("---")

# Chat container
chat_container = st.container()

# Input box
with st.form(key="chat_form"):
    question = st.text_input("Your question:", key="user_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("💬 Ask")

# On Ask
if submit_button and question.strip():
    with st.spinner("Thinking..."):
        context = get_context_for_query(question)

        # Save last Q/context
        st.session_state.last_question = question
        st.session_state.last_context = context

        # Build chat memory if enabled
        chat_thread = st.session_state.chat_history if st.session_state.use_memory else []

        answer = ask_ollama(question, context, chat_history=chat_thread)

        # Store chat
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.session_state.questions.append(question)

        # Save to file
        with open(st.session_state.session_file, "w", encoding="utf-8") as f:
            json.dump(st.session_state.chat_history, f, indent=2)

        # Show context (optional debug)
        with st.expander("🔍 Show Context Used"):
            st.code(context)

# Render chat messages
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<p style='color: blue;'><strong>🧑‍💻 You:</strong> {msg['content']}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: green;'><strong>🤖 Bot:</strong> {msg['content']}</p>", unsafe_allow_html=True)
