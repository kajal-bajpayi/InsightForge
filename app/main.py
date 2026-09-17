from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.pipeline import run_pipeline
from app.compare import run_comparison
from app.memory import start_session, chat
import uuid
import os

app = FastAPI(
    title="InsightForge",
    description="AI-powered research digest and comparison engine",
    version="1.0.0"
)

# request models 
class ResearchRequest(BaseModel):
    topic: str

class CompareRequest(BaseModel):
    topic_a: str
    topic_b: str

class ChatRequest(BaseModel):
    session_id: str
    question: str


# health checks
@app.get("/")
def root():
    return {"status": " App is running"}

@app.post("/research")
def research(request: ResearchRequest):
    result = run_pipeline(request.topic)

    session_id = str(uuid.uuid4)
    start_session(session_id, result["report"])

    save_report(request.topic, result["report"])

    return {
        "session_id": session_id,
        "topic": result["topic"],
        "report": result["report"]
    }


@app.post("/compare")
def compare(request: CompareRequest):
    result = run_comparison(request.topic_a, request.topic_b)

    session_id = str(uuid.uuid4)
    start_session(session_id, result["report"])

    topic_label = f"{request.topic_a} vs {request.topic_b}"
    save_report(topic_label, result["report"])

    return {
        "session_id": session_id,
        "topic_a": result["topic_a"],
        "topic_b": result["topic_b"],
        "report": result["report"]
    }


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = chat(request.session_id, request.question)
    return {
        "session_id": request.session_id,
        "answer": response 
    }

@app.get("/report/download/{filename}")
def download_report(fname: str):
    filepath = f"reports/{fname}.txt"
    if not os.path.exists(filepath):
        return {"error": "Report not found"}
    return StreamingResponse(
        open(filepath, "rb"),
        media_type = "text/plain",
        headers= {"Content-Disposition":f"attachment; filename={filename}.txt" }

    )

def save_report(topic: str, report: str):
    filename = topic.lower().replace(" ", "_")[:50]
    filepath = f"reports/{filename}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)