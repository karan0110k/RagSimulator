from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def select_model(query):
    query = query.lower()

    if "summarize" in query:
        return "llama-3.1-8b-instant"

    if len(query) > 100 or "analyze" in query or "compare" in query:
        return "llama-3.3-70b-versatile"

    return "llama-3.1-8b-instant"

def generate_response(query, context):

    model_name = select_model(query)

    prompt = f"""
You are an enterprise AI assistant.
Answer strictly from the provided context.
If answer is not found, say:
"Information not found in provided documents."

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content, model_name