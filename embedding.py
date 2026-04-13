from sentence_transformers import SentenceTransformer

model = SentenceTransformer("All-MiniLM-L6-v2")


def get_embedding(text: str):
    return model.encode(text).tolist()