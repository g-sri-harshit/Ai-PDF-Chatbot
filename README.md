# 🤖 AI PDF Chatbot (RAG-based)

An intelligent chatbot that can read PDF documents and answer questions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📄 Upload any PDF
- 🔍 Semantic search using embeddings
- 🤖 Context-aware answers
- 🧠 Uses NLP & LLM concepts
- 🖼️ OCR support for images in PDFs

---

## 🛠️ Tech Stack

- Python
- Streamlit
- SentenceTransformers
- PyMuPDF (fitz)
- FAISS / Custom Vector Store
- Pytesseract (OCR)

---

## ⚙️ How it Works

1. Extract text, tables, and images from PDF
2. Clean and chunk the content
3. Convert text into embeddings
4. Store embeddings in vector database
5. Retrieve relevant chunks based on query
6. Generate answer using LLM

---

## ▶️ Run Locally

```bash
git clone https://github.com/your-username/AI-PDF-Chatbot.git
cd AI-PDF-Chatbot
pip install -r requirements.txt
streamlit run app.py
