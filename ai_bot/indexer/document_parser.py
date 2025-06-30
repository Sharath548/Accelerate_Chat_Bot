import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import docx
from ai_bot.indexer.flow_parser import detect_shapes_and_arrows

def parse_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return parse_image(file_path)
    elif ext in [".txt", ".py", ".md", ".json"]:
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return split_chunks(text)

def parse_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return split_chunks(text)

def parse_image(file_path):
    shapes = detect_shapes_and_arrows(file_path)
    if not shapes:
        return ["No flow detected."]
    
    steps = []
    for shape in shapes:
        steps.append(f"{shape['type'].capitalize()}: {shape['text']}")

    return split_chunks("\n".join(steps))

def parse_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return split_chunks(text)

def split_chunks(text, max_tokens=500):
    # Naive split by paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    chunk = ""

    for para in paragraphs:
        if len(chunk) + len(para) < max_tokens:
            chunk += para + "\n\n"
        else:
            chunks.append(chunk.strip())
            chunk = para + "\n\n"

    if chunk:
        chunks.append(chunk.strip())

    return chunks
