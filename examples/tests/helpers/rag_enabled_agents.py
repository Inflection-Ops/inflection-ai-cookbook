import torch
import tiktoken
import numpy as np
from scipy.spatial.distance import cdist
from transformers import AutoTokenizer, AutoModel

model_name = "answerdotai/ModernBERT-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

texts = [
    "Electric vehicles (EVs) are becoming more popular due to their efficiency and environmental benefits. Charging infrastructure is expanding worldwide.",
    "Quantum computing uses principles of quantum mechanics to perform calculations at speeds unattainable by classical computers.",
    "Renewable energy sources like solar and wind power are key to reducing carbon emissions and combating climate change."
]


def get_chunks(texts: list, max_tokens: int = 10, encoding_name: str = "cl100k_base") -> list:
    enc = tiktoken.get_encoding(encoding_name)
    chunks = []
    for text in texts:
        tokens = enc.encode(text)
        for i in range(0, len(tokens), max_tokens):
            chunk = tokens[i:i + max_tokens]
            chunks.append(enc.decode(chunk))
    return chunks


processed_chunks = get_chunks(texts)


def encode_text(text: str) -> np.ndarray:
    """Encodes a piece of text using ModernBERT"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # Take [CLS] token representation


chunk_embeddings = np.array([encode_text(chunk) for chunk in processed_chunks])  # Store embeddings in memory

# Store chunks for lookup
chunk_dict = {i: processed_chunks[i] for i in range(len(processed_chunks))}


def retrieve_top_k(query: str, k: int = 4) -> list:
    """Encodes query, retrieves top k matching chunks using cosine similarity"""
    query_embedding = encode_text(query).reshape(1, -1)  # Encode query
    distances = cdist(query_embedding, chunk_embeddings, metric="cosine")  # Compute cosine similarity
    indices = np.argsort(distances)[0][:k]  # Get top-k the closest chunks

    retrieved_texts = [chunk_dict[idx] for idx in indices]
    return retrieved_texts


system_instruction_prompt = """
You are a helpful assistant. Your task is to answer the user's question strictly based on the provided context.

## Instructions:
- You will be given a question and a context.
- Your answer must be based only on the provided context. Do not include any external information or assumptions.
- If the answer is not in the context, state that explicitly. Do not attempt to infer or fabricate an answer.
"""
