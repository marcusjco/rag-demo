# RAG Knowledge Base Demo

![python](https://img.shields.io/badge/Python-3.11+-3b82f6) ![claude](https://img.shields.io/badge/Claude-Sonnet%204.6-818cf8) ![chromadb](https://img.shields.io/badge/ChromaDB-0.5+-22c55e)

Built this to show what a real RAG pipeline looks like end to end — not just the concept, but the actual retrieval step made visible. When you ask a question, you see which document sections got pulled before the answer even starts generating. That transparency is something I think most chatbot demos skip over, and it matters a lot for building trust in a production system.

The demo uses fictional Meridian Supply Co. product documentation — install guides, spec sheets, VLAN config, warranty policy. Ask it anything about those docs and it'll find the right sections and answer from them. If the docs don't cover it, it says so.

## What makes it RAG vs. a regular chat

A standard LLM response is the model working from its training data — you can't control what it knows or verify where an answer came from. RAG flips that. Before Claude says anything, the system:

1. Embeds your question into a vector
2. Searches the knowledge base for the closest matching chunks (cosine similarity)
3. Injects those chunks into the prompt as context
4. Tells Claude to answer *only* from those sources

The model becomes a synthesizer over documents you control, not a black box. You can update the knowledge base, audit what got retrieved, and catch it when it tries to go off-script.

## Architecture

```
User question
     │
     ▼
Sentence Transformer (all-MiniLM-L6-v2)
     │  embed query
     ▼
ChromaDB — cosine similarity search → top 4 chunks
     │
     ▼
Claude Sonnet 4.6 — synthesize answer from retrieved context
     │
     ▼
SSE stream → frontend (sources shown first, then answer)
```

## Tech Stack

| Layer | Tech |
|---|---|
| AI | Claude Sonnet 4.6 |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, runs locally) |
| Vector DB | ChromaDB (in-memory, no setup required) |
| Backend | Python, FastAPI, Uvicorn |
| Streaming | Server-Sent Events |
| Frontend | Vanilla JS — KB panel left, chat right |

No OpenAI or Cohere key needed. Embeddings run locally via sentence-transformers.

## Project layout

```
rag-demo/
├── backend/
│   ├── documents.py    # knowledge base content (19 chunks across 6 documents)
│   ├── rag.py          # embed on startup, retrieve on query
│   ├── agent.py        # Claude synthesis with SSE streaming
│   └── main.py         # FastAPI — /chat/stream + /api/documents
├── frontend/
│   └── index.html      # KB panel + chat UI, source cards, relevance scores
├── .env.example
├── requirements.txt
└── README.md
```

## Running it locally

```bash
git clone https://github.com/marcusjco/rag-demo.git
cd rag-demo
pip install -r requirements.txt

cp .env.example .env
# add your Anthropic API key

cd backend
uvicorn main:app --reload
```

Open `http://localhost:8000`.

**First run note:** sentence-transformers will download the `all-MiniLM-L6-v2` model (~90MB) on startup. After that it's cached locally and loads in seconds.

## The knowledge base

Six fictional Meridian Supply Co. documents split into 19 chunks:

| Document | Sections |
|---|---|
| ISA-2400 Industrial Sensor Array | Overview, Installation, Configuration, Troubleshooting |
| GCU-1800 Gateway Controller | Overview, REST API, Network Config |
| RP-3200 RFID Reader Pro | Overview, Antenna Setup, Integration Guide |
| NS-24 Network Switch | Overview, VLAN Config, QoS & PoE |
| 2026 Product Catalog | Sensors, Hardware, Networking, Software & Services |
| Support & Warranty Policy | Warranty Terms, RMA Process, SLA Tiers |

Things worth asking:
- How do I configure VLANs on the NS-24?
- What's the read range of the RP-3200?
- How do I reset the ISA-2400 to factory defaults?
- What does the warranty cover and what's the RMA process?
- How do I set up the GCU-1800 REST API?

## Things I was intentional about

**Source cards before the answer.** The frontend emits a `sources` SSE event the moment retrieval finishes — before Claude starts generating. You see exactly which sections were used while the answer streams in. Makes the system auditable, not just functional.

**Claude never uses outside knowledge.** The system prompt explicitly instructs it to answer only from the provided context and say so if the docs don't cover something. In a production deployment you'd want this for compliance and consistency.

**Chunking is at the section level.** Each doc section is its own chunk with metadata (doc name, section title, category). This makes retrieval precise and citations clean — you know exactly what got pulled, not just a blob of text.

**Swapping the knowledge base is one file.** Add or replace entries in `documents.py`, restart the server. ChromaDB re-embeds on startup if the collection is empty.

## Extending it

- **Connect real docs:** Replace the hardcoded `DOCUMENTS` list in `documents.py` with a PDF/DOCX loader (PyMuPDF, python-docx) that chunks on page or section boundaries.
- **Persist the vector store:** Pass `chromadb.PersistentClient(path="./chroma_data")` instead of `chromadb.Client()` — no re-embedding on restart.
- **Tune retrieval:** Adjust `n_results` in `rag.py` or swap `all-MiniLM-L6-v2` for a larger model if precision matters more than speed.
- **Add a reranker:** After the initial retrieval, run a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) to reorder chunks before passing to Claude.

## License

MIT
