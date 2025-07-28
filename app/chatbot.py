import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.embeddings import FakeEmbeddings  #  use dummy embeddings for loading

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === Initialize Groq LLM ===
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-8b-8192"
)

# === Load FAISS Vector Store with FakeEmbeddings (no SBERT model in memory) ===
print("Loading FAISS vector store...")
vector_store = FAISS.load_local(
    "embeddings/vector_index/changi_langchain",
    FakeEmbeddings(size=384),  #  lighter for memory-constrained deploys
    allow_dangerous_deserialization=True
)
print(f"Total entries in index: {vector_store.index.ntotal}")

# === Set Retriever ===
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# === Prompt Template ===
template = """
You are an expert travel assistant helping users with accurate and friendly information about Changi Airport and Jewel Changi.

Use ONLY the context provided to answer the question.
Be helpful and slightly conversational, but avoid generic phrases like "I'm happy to help" or "Let me know if you have more questions".
If the answer is not found in the context, reply with:
"Sorry, I couldn't find that in the available info."

Context:
{context}

Question: {question}

Answer (be concise yet informative):
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# === Retrieval Q&A Chain ===
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False,
    input_key="question"
)

# === Exportable chatbot for FastAPI ===
def create_chatbot():
    return chain

# === Optional CLI Testing ===
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ").strip()
        if user_query.lower() in ["exit", "quit"]:
            break

        # Terminal filtering
        terminal_match = re.search(r"terminal\s?(\d+)", user_query, re.IGNORECASE)
        if terminal_match:
            terminal_number = f"T{terminal_match.group(1)}"
            print(f"Filtering chunks for: Terminal {terminal_match.group(1)}")
            retriever.search_kwargs["filter"] = {"terminal": terminal_number}
        else:
            retriever.search_kwargs.pop("filter", None)

        # Get answer
        response = chain.invoke({"question": user_query})
        print(f"\n Answer: {response['result']}")
