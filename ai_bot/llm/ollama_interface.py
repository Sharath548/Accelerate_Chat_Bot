import subprocess
import json

OLLAMA_MODEL = "mistral"  # You can change to llama3, gemma, etc.

def ask_ollama(question, context):
    # Build the full prompt
    full_prompt = f"""You are an AI assistant.
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

    try:
        # Use subprocess to call ollama
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=full_prompt.encode("utf-8"),
            capture_output=True,
            timeout=200
        )
        output = result.stdout.decode("utf-8").strip()
        return output

    except subprocess.TimeoutExpired:
        return "⚠️ Ollama timed out."
    except Exception as e:
        return f"❌ Error talking to Ollama: {e}"
