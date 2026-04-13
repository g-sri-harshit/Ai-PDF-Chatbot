import streamlit as st
import tempfile

from pdf_reader import extract_pdf_content
from chunking import chunk_text
from embedding import get_embedding
from vector_store import VectorStore
from query import ask_llm

st.set_page_config(page_title = "PDF Chatbot", layout = "wide")

st.title("📄 AI PDF Chatbot")
st.write("Upload a PDF document and ask questions about its content!")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf "])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    st.success("✅ PDF uploaded successfully!")

    with st.spinner("Processing PDF..."):

        data = extract_pdf_content(pdf_path)

        texts = []

        for item in data:
            if item["type"] in ["text", "image"]:
                chunks = chunk_text(item["content"])
                texts.extend(chunks)
            else:
                texts.append(item["content"])  # tables not chunked

        # Embeddings
        embeddings = [get_embedding(text) for text in texts]

        # Store
        store = VectorStore(len(embeddings[0]))
        store.add(embeddings, texts)

        # Save store in session (VERY IMPORTANT)
        st.session_state.store = store

    st.success("✅ PDF processed! You can now ask questions.")
    
if "store" in st.session_state:

    question = st.text_input("Ask a question:")

    if question:

        with st.spinner("Thinking..."):

            query_embedding = get_embedding(question)

            results = st.session_state.store.search(query_embedding)

            context = "\n".join(results)

            answer = ask_llm(context, question)

        st.subheader("📌 Answer:")
        st.write(answer)

        # Optional: Show context (debug)
        with st.expander("🔍 Retrieved Context"):
            st.write(context)
