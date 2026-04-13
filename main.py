from pdf_reader import extract_pdf_content
from chunking import chunk_text
from embedding import get_embedding
from vector_store import VectorStore
from query import ask_llm

data = extract_pdf_content("data/book.pdf")

texts = []

for item in data:
    if item["type"] in ["text","image"]:
        chunks = chunk_text(item["content"])
        texts.extend(chunks)
    else:
        texts.append(item["content"])


embeddings = [get_embedding(text) for text in texts]

store = VectorStore(len(embeddings[0]))
store.add(embeddings, texts)

while True:
    question = input("\nASK: ")
    query_embedding = get_embedding(question)
    results = store.search(query_embedding)
    context = "\n".join(results)
    answer = ask_llm(context, question)
    print("\nAnswer:\n", answer)
