import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppresses INFO and WARNING logs from TensorFlow

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='tensorflow')

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

load_dotenv()

# Set your paths
persist_path = "embeddings/vector_index/changi_langchain"

# Load embeddings
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vector store
def load_vectorstore():
    if os.path.exists(persist_path):
        print("✅ Loading prebuilt FAISS store...")
        return FAISS.load_local(persist_path, embeddings=get_embeddings(), allow_dangerous_deserialization=True)
    else:
        raise FileNotFoundError("Vector store not found. Please run preprocessing first.")

# Create chatbot chain
def create_chatbot():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()
    llm = OllamaLLM(model="phi3")
    chatbot = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        input_key="query"  # Explicitly declare expected input key
    )
    return chatbot

# Main interaction
if __name__ == "__main__":
    chatbot = create_chatbot()

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break
        result = chatbot.invoke({"query": query})
        print(f"\n🧠 Answer: {result['result']}\n")
        if result.get("source_documents"):
            print("📚 Sources:")
            for doc in result["source_documents"]:
                print(f"- {doc.metadata.get('source', 'Unknown')}")
