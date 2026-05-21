"""
RAG synthesis — retrieve relevant chunks then stream Claude's answer.
Claude is grounded entirely in the retrieved context; it does not use prior knowledge.
"""
import json
import os
from typing import Generator

import anthropic
from dotenv import load_dotenv

from rag import retrieve

load_dotenv()

_client = None

SYSTEM_PROMPT = """You are a technical support assistant for Meridian Supply Co., a B2B industrial equipment distributor.

Answer the user's question using ONLY the provided source documents below. Do not use outside knowledge.
If the documents don't contain enough information to fully answer, say so clearly and suggest contacting support.

Format your answers with markdown — use headers, bullets, and bold for key values where it helps readability.
When you reference specific information, note which document it came from in parentheses.
Be direct and specific — give actual values, steps, and part numbers from the docs."""

SYSTEM = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def run_rag(question: str, history: list[dict]) -> Generator[str, None, None]:
    # 1. Retrieve relevant chunks
    chunks = retrieve(question, n_results=4)

    # 2. Emit sources so the frontend can show them before the answer arrives
    yield f"data: {json.dumps({'type': 'sources', 'chunks': chunks})}\n\n"

    # 3. Build context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['doc']} — {chunk['section']}]\n{chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    # 4. Build messages
    messages = history[-8:] + [{
        "role": "user",
        "content": f"SOURCE DOCUMENTS:\n\n{context}\n\n---\n\nQUESTION: {question}",
    }]

    # 5. Stream Claude's synthesis
    with get_client().messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield f"data: {json.dumps({'type': 'text', 'content': text})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
