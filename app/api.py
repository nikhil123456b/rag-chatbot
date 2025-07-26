from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Ensure we can import chatbot.py
sys.path.append(os.path.dirname(__file__))

from chatbot import create_chatbot  # ✅ Reuse the chatbot logic

# Initialize FastAPI app
app = FastAPI()

# Load chatbot once at startup
chatbot = create_chatbot()

# Define request and response schemas
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
def root():
    return {"message": "✅ RAG Chatbot API is running!"}

@app.post("/chat", response_model=QueryResponse)
def chat_endpoint(payload: QueryRequest):
    try:
        result = chatbot.invoke({"question": payload.query})  # 👈 matches updated prompt format
        return QueryResponse(answer=result["result"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
