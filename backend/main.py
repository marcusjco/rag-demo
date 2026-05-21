from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag import load_knowledge_base, list_documents
from agent import run_rag


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_knowledge_base()
    yield


app = FastAPI(title="Meridian RAG Demo", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/documents")
def documents():
    return list_documents()


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(
        run_rag(req.message, req.history),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
