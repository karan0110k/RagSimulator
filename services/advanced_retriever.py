from services.hyde import generate_hypothetical_answer
from services.embedding_service import generate_embeddings
import services.vector_store as vs
import numpy as np

def advanced_retrieve(query, k=5):

    # 🔹 Step 1: HYDE
    hypothetical = generate_hypothetical_answer(query)

    query_embedding = generate_embeddings([hypothetical])
    query_embedding = np.array(query_embedding)

    # 🔹 Step 2: Hybrid text search
    child_ids, confidence = vs.hybrid_text_search(
        query_embedding,
        query,
        k=k
    )

    # 🔹 Step 3: Map child → parent
    parent_context = vs.get_parent_documents(child_ids)

    return parent_context, confidence