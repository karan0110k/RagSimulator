from services.embedding_service import generate_embeddings
from services.vector_store import hybrid_search
import numpy as np

def retrieve(query):
    query_emb = generate_embeddings([query])
    docs, confidence = hybrid_search(np.array(query_emb), query)
    return docs, confidence