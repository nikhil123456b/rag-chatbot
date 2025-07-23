import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_chunks(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def generate_embeddings(text_list, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(text_list, show_progress_bar=True)
    return embeddings

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_index(index, path="embeddings/vector_index/changi_faiss.index"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)
    print(f"✅ FAISS index saved to {path}")

def save_mapping(data, path="embeddings/vector_index/changi_mapping.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Metadata saved to {path}")

def run_embedding_pipeline():
    input_json = "data/cleaned/changi_chunks.json"
    data = load_chunks(input_json)
    texts = [item["content"] for item in data]

    print("🔄 Generating embeddings...")
    embeddings = generate_embeddings(texts)

    print("🔄 Building FAISS index...")
    index = build_faiss_index(np.array(embeddings))

    save_index(index)
    save_mapping(data)

if __name__ == "__main__":
    run_embedding_pipeline()
