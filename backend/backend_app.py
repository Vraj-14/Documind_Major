from fastapi import FastAPI
from pydantic import BaseModel

from backend.intent_router import process_question

app = FastAPI(
    title="Documind Financial Assistant",
    description="AI powered financial question answering system",
    version="1.0"
)


# -----------------------------
# Request Schema
# -----------------------------

class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def home():
    return {"message": "Documind API is running"}


# -----------------------------
# Ask Question Endpoint
# -----------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question

    result = process_question(question)

    return {
        "question": question,
        "intent": result["intent"],
        "entities": result["entities"],
        "sql_query": result["query"],
        "data": result["data"],
        "answer": result["answer"]
    }