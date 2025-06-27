import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ai_bot.retriever.query_engine import get_context_for_query
from ai_bot.llm.ollama_interface import ask_ollama

st.set_page_config(page_title="AI Knowledge Bot", page_icon="🤖")
st.title("🤖 AI Knowledge Assistant")
st.markdown("Ask anything based on the files you dropped into `input_files/`.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("📝 Your question:")

if st.button("💬 Ask") and question.strip():
    with st.spinner("Thinking..."):
        # 1. Search vector DB
        context = get_context_for_query(question)

        # 2. Send to local LLM via Ollama
        answer = ask_ollama(question, context)

        # 3. Store chat
        st.session_state.chat_history.append(("You", question))
        st.session_state.chat_history.append(("Bot", answer))

# Show chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑‍💻 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
