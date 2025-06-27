# 🤖 Accelerate Chat Bot

A fully local, open-source AI assistant that can:
- 📂 Watch a folder and index any uploaded documents
- 🧠 Build a semantic knowledge base using embeddings + FAISS
- 💬 Let you ask natural language questions via a clean Streamlit UI
- 🧪 Generate test cases or summaries using a local LLM (like Mistral via Ollama)
- 🧩 Understand PDFs, Word docs, images (OCR), plain text, and code

---

## 🚀 Features

- ✅ Local only — no internet or API needed
- 📁 File types: `.pdf`, `.docx`, `.txt`, `.jpg`, `.png`, `.py`, `.json`
- 🤖 Works with Ollama + open LLMs (Mistral, LLaMA3, Gemma)
- 🧠 Uses FAISS for fast vector-based search
- 💬 Built-in Streamlit chat UI

---

## 🧰 Tech Stack

| Component        | Tool                      |
|------------------|---------------------------|
| File Watcher     | `watchdog`                |
| Text Extraction  | `PyMuPDF`, `python-docx`, `pytesseract` |
| Embeddings       | `sentence-transformers` (MiniLM) |
| Vector DB        | `FAISS`                   |
| LLM Runtime      | `Ollama` + `mistral`      |
| UI               | `Streamlit`               |

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/Sharath548/Accelerate_Chat_Bot.git
cd Accelerate_Chat_Bot
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
Activate it:

On Windows:

bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🧠 Ollama Setup (Local LLM)
1. Install Ollama
Download and install from https://ollama.com/download

2. Pull a model
For example:

bash
Copy
Edit
ollama pull mistral
📂 How to Use
1. Start File Watcher (Indexing)
bash
Copy
Edit
python ai_bot/main.py
Drop files into the input_files/ folder — they'll be automatically parsed, embedded, and saved.

2. Start the Chatbot UI
bash
Copy
Edit
streamlit run ai_bot/ui/chat_ui.py
Go to http://localhost:8501, and start chatting with your bot!

Example questions:

"Generate test cases for bronze enrollment"

"What is this diagram about?"

"List all steps in the refund flow"

🗃 Project Structure
bash
Copy
Edit
Accelerate_Chat_Bot/
├── ai_bot/
│   ├── watcher/         # File watcher for new documents
│   ├── indexer/         # Parser, embedder, vector store
│   ├── retriever/       # Query engine for semantic search
│   ├── llm/             # Ollama interface
│   └── ui/              # Streamlit UI
├── input_files/         # Folder to drop files into
├── requirements.txt
├── main.py
└── README.md
⚠️ Troubleshooting
"Ollama timed out"
→ Increase timeout in ollama_interface.py and check if Ollama is running

"No documents found"
→ Make sure files are placed in input_files/ before asking questions

OCR issues?
→ Install Tesseract OCR and add it to your PATH

🙌 Credits
Developed by Sharath Chandra Reddy
Powered by Ollama + open-source LLMs + Python

🔐 Privacy & Security
100% offline

No data leaves your system

Ideal for enterprise environments with sensitive data

🏁 Future Plans
Flowchart → logic parser

Export test cases to .feature files

Advanced RAG tuning and multi-file relationships

Live context preview in UI