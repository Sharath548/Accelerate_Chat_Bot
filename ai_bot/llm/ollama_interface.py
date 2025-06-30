from ollama import Client

OLLAMA_MODEL = "phi3"  # You can change this to 'llama3', 'mistral', etc.

client = Client(host='http://localhost:11434')  # Default Ollama server

def ask_ollama(question, context, chat_history=None):
    try:
        # System prompt for behavior
        system_msg = {
            "role": "system",
            "content": "You are a helpful AI assistant that answers user questions based on provided document context and prior conversation."
        }

        # Start building the message thread
        messages = [system_msg]

        # Include prior conversation history if available
        if chat_history:
            messages.extend(chat_history)

        # Add the current user question with context
        user_msg = {
            "role": "user",
            "content": f"""Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""
        }
        messages.append(user_msg)

        # Send to Ollama
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages
        )

        return response['message']['content'].strip()

    except Exception as e:
        return f"❌ Error talking to Ollama: {e}"
