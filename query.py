import requests

def ask_llm(context, question):
    prompt = f"""
    You are a helpful assistant.
    Answer ONLY from the given context.
    If the answer is not in context, say "I don't know".

    Context:
    {context}

    Question:
    {question}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]