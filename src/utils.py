from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(text: str) -> list[float]:
    return embedding_model.encode(text).tolist()