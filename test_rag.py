import sys
from services.rag_pipeline import run_rag
from services.embedding_service import generate_embeddings
from services.vector_store import create_text_index, text_chunks, parent_docs, child_to_parent
import numpy as np

# Mocking data
test_text = "OmniRAG is a multi-model RAG system designed for enterprise use. It supports PDF and image parsing. The answer to life is 42."
chunks = ["OmniRAG is a multi-model RAG system designed for enterprise use.", "It supports PDF and image parsing.", "The answer to life is 42."]
parents = [test_text]
mapping = {0: 0, 1: 0, 2: 0}

embeddings = generate_embeddings(chunks)
create_text_index(np.array(embeddings), chunks, parents, mapping)

print("--- Testing regular retrieval ---")
from services.advanced_retriever import advanced_retrieve

query = "What is the answer to life?"
p, c = advanced_retrieve(query)
print("Parents:", p)
print("Confidence:", c)

print("\n--- Testing RAG ---")
ans, model, conf = run_rag(query)
print("Answer:", ans)
print("Model:", model)
print("Confidence:", conf)
