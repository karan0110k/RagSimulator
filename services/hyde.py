from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def generate_hypothetical_answer(query):

    prompt = f"""
Generate a detailed hypothetical answer to the following question.
This is only for retrieval purposes.

Question:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content