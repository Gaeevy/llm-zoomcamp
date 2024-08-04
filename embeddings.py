from sentence_transformers import SentenceTransformer

model = SentenceTransformer("multi-qa-distilbert-cos-v1")
vector_size = model.encode("").shape[0]


def encode(text: str) -> list[float]:
    return model.encode(text).tolist()
