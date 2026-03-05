from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, docs):

    if not docs:
        return []

    pairs = [(query, doc) for doc in docs]

    scores = reranker_model.predict(pairs)

    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, score in scored_docs[:3]]