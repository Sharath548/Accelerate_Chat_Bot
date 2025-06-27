import os
import faiss
import pickle
import numpy as np

# Path to store vector DB and metadata
INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_meta.pkl"

dimension = 384  # for MiniLM model

# Load or create FAISS index
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else:
    index = faiss.IndexFlatL2(dimension)

# Metadata to track file and chunk text
if os.path.exists(META_FILE):
    with open(META_FILE, "rb") as f:
        metadata = pickle.load(f)
else:
    metadata = []

def save_vectors(file_path, chunks, embeddings):
    global metadata

    # Convert to float32 numpy array
    embeddings = np.array(embeddings).astype("float32")

    # Add to FAISS index
    index.add(embeddings)

    # Save metadata
    for chunk in chunks:
        metadata.append({
            "file": file_path,
            "text": chunk
        })

    # Persist to disk
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)

def search(query_vector, top_k=5):
    D, I = index.search(np.array([query_vector]).astype("float32"), top_k)
    return [metadata[i] for i in I[0] if i < len(metadata)]
