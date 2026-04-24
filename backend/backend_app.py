from fastapi import FastAPI
from pydantic import BaseModel

from backend.intent_router import process_question

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Documind Financial Assistant",
    description="AI powered financial question answering system",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    result   = process_question(question)

    return {
        "question":         question,
        "intent":           result["intent"],
        "entities":         result["entities"],
        "sql_query":        result["query"],
        "data":             result["data"],
        "answer":           result["answer"],
        # NEW — intent debug fields
        "predicted_intent": result.get("predicted_intent", result["intent"]),
        "final_intent":     result.get("final_intent",     result["intent"]),
        "confidence":       result.get("confidence",       None),
        "override_fired":   result.get("override_fired",   False),
    }


