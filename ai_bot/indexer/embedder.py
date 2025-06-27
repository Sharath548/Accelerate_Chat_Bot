import os
from sentence_transformers import SentenceTransformer
from ai_bot.indexer import vector_store

# Load transformer once (can choose other models later)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_and_store(file_path, chunks):
    if not chunks:
        print(f"⚠️ No content extracted from {file_path}")
        return

    embeddings = model.encode(chunks)

    # Store vectors with metadata
    vector_store.save_vectors(file_path, chunks, embeddings)

    print(f"✅ Embedded and stored: {file_path} ({len(chunks)} chunks)")
