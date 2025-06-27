import os
import subprocess

folders = [
    "ai_bot/config",
    "ai_bot/watcher",
    "ai_bot/indexer",
    "ai_bot/retriever",
    "ai_bot/llm",
    "ai_bot/ui",
    "ai_bot/utils"
]

# Create folders and empty Python files
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "__init__.py"), "w"):
        pass

# Create main.py
with open("ai_bot/main.py", "w") as f:
    f.write("# Entry point for AI bot\n")

# Create requirements.txt
with open("requirements.txt", "w") as f:
    f.write("""watchdog
faiss-cpu
sentence-transformers
pytesseract
python-docx
PyMuPDF
opencv-python
gradio
""")

print("✅ Project structure created.")
