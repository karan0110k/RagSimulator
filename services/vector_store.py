import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# GLOBAL STORES
# ==============================

text_index = None
image_index = None

text_chunks = []
image_chunks = []

parent_docs = []
child_to_parent = {}

tfidf_vectorizer = None
tfidf_matrix = None


# ==============================
# CREATE TEXT INDEX (Parent-Child)
# ==============================

def create_text_index(embeddings, child_chunks, parents, mapping):
    global text_index, text_chunks, parent_docs, child_to_parent
    global tfidf_vectorizer, tfidf_matrix

    dim = embeddings.shape[1]

    text_index = faiss.IndexFlatL2(dim)
    text_index.add(np.array(embeddings))

    text_chunks = child_chunks
    parent_docs = parents
    child_to_parent = mapping

    # TF-IDF for hybrid retrieval
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(child_chunks)


# ==============================
# CREATE IMAGE INDEX
# ==============================

def create_image_index(embeddings, chunks):
    global image_index, image_chunks

    dim = embeddings.shape[1]

    image_index = faiss.IndexFlatL2(dim)
    image_index.add(np.array(embeddings))

    image_chunks = chunks


# ==============================
# HYBRID TEXT SEARCH
# ==============================

def hybrid_text_search(query_embedding, query_text, k=5):
    global text_index, text_chunks, tfidf_vectorizer, tfidf_matrix

    if text_index is None:
        return [], 0.0

    # Vector Search
    D, I = text_index.search(query_embedding, k)
    vector_scores = 1 / (1 + D[0])  # Convert distance → similarity

    # TF-IDF Search
    query_tfidf = tfidf_vectorizer.transform([query_text])
    keyword_scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    combined_scores = {}

    for i, idx in enumerate(I[0]):
        combined_scores[idx] = 0.7 * vector_scores[i] + 0.3 * keyword_scores[idx]

    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    child_ids = [item[0] for item in sorted_results[:k]]
    confidence = sorted_results[0][1] if sorted_results else 0.0

    return child_ids, round(float(confidence), 4)


# ==============================
# IMAGE SEARCH
# ==============================

def image_search(query_embedding, k=3):
    global image_index

    if image_index is None:
        return []

    D, I = image_index.search(query_embedding, k)

    return list(I[0])


# ==============================
# MAP CHILD → PARENT
# ==============================

def get_parent_documents(child_ids):
    global parent_docs, child_to_parent

    parent_ids = set()

    for cid in child_ids:
        if cid in child_to_parent:
            parent_ids.add(child_to_parent[cid])

    return [parent_docs[i] for i in parent_ids]