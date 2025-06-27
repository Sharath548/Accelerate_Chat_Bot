from sentence_transformers import SentenceTransformer
from ai_bot.indexer import vector_store

# Use the same embedding model as before
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_context_for_query(query, top_k=5):
    print(f"🔎 Searching vector DB for: {query}")
    
    query_embedding = model.encode([query])[0]  # Single query
    results = vector_store.search(query_embedding, top_k=top_k)
    
    context_texts = [item["text"] for item in results]
    combined_context = "\n\n".join(context_texts)
    
    return combined_context
