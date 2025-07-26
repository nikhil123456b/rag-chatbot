# utils/generate_embeddings.py

import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Paths
DATA_PATH = "data/cleaned/cleaned_data_with_text.json"
OUTPUT_DIR = "embeddings/vector_index/changi_langchain"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load cleaned records
with open(DATA_PATH, "r", encoding="utf-8") as f:
    records = json.load(f)

# Convert records to LangChain Documents
documents = []
for entry in records:
    metadata = entry.copy()
    text = metadata.pop("text", "")
    documents.append(Document(page_content=text, metadata=metadata))

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Build vector store
print("🔍 Generating embeddings...")
vector_store = FAISS.from_documents(documents, embedding_model)

# Save vector index
vector_store.save_local(OUTPUT_DIR)

print(f"✅ Stored {len(documents)} entries in FAISS index.")
