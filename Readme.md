# InsightForge 🔬

> AI-powered research digest and comparison engine built with LangChain, Groq, and FastAPI.

InsightForge takes any topic and runs it through a 4-step AI pipeline — Researcher → Summarizer → Critic → Report Writer — producing a polished research digest in seconds. It also features a unique **Comparison Mode** that researches two topics in parallel and generates a structured side-by-side analysis.

---

## Features

- **Single Topic Research** - generates a structured digest with overview, key findings, open questions, and conclusion
- **Comparison Mode** - researches two topics independently then produces a head-to-head comparison report
- **Conversation Memory** - ask follow-up questions about any generated report via a memory-aware chat endpoint
- **Auto File Save** - every report is saved as a `.txt` file and downloadable via API
- **Streaming Ready** - built on FastAPI with `StreamingResponse` support
- **Interactive Docs** - full Swagger UI at `/docs` out of the box

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Framework | LangChain (LCEL) |
| Model | Groq - `openai/gpt-oss-120b` (Llama-based) |
| API | FastAPI + Uvicorn |
| Memory | LangChain `MessagesPlaceholder` |
| Environment | python-dotenv |

---

## Project Structure

```
insightforge/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app and all endpoints
│   ├── pipeline.py     # 4-step single topic research pipeline
│   ├── compare.py      # Comparison mode pipeline
│   └── memory.py       # Conversation memory and chat
├── reports/            # Auto-saved .txt report files
├── .env
└── requirements.txt
```

---

## Pipeline Architecture

### Single Topic Mode
```
User Input (topic)
      ↓
  Researcher     → 5 key developments (bullet points)
      ↓
  Summarizer     → 3-paragraph summary
      ↓
  Critic         → 3 gaps / open questions
      ↓
  Report Writer  → structured digest (Overview, Key Findings, Open Questions, Conclusion)
```

### Comparison Mode
```
Topic A → Researcher → Summarizer ─┐
                                    ├→ Comparator → Report Writer → side-by-side digest
Topic B → Researcher → Summarizer ─┘
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/insightforge.git
cd insightforge
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) - no credit card required.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## API Endpoints

### `GET /`
Health check.

**Response:**
```json
{ "status": "InsightForge is running" }
```

---

### `POST /research`
Runs the 4-step pipeline on a single topic.

**Request:**
```json
{ "topic": "artificial intelligence in healthcare" }
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "topic": "artificial intelligence in healthcare",
  "report": "## Overview\n..."
}
```

> The report is auto-saved to `reports/` and a memory session is started automatically.

---

### `POST /compare`
Researches two topics in parallel and generates a comparison digest.

**Request:**
```json
{
  "topic_a": "React",
  "topic_b": "Vue"
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "topic_a": "React",
  "topic_b": "Vue",
  "report": "## Overview\n..."
}
```

---

### `POST /chat`
Ask follow-up questions about a previously generated report.

**Request:**
```json
{
  "session_id": "uuid-from-research-or-compare",
  "question": "What are the biggest risks mentioned?"
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "answer": "Based on the report..."
}
```

---

### `GET /report/download/{filename}`
Download a saved report as a `.txt` file.

**Example:**
```
GET /report/download/artificial_intelligence_in_healthcare
```

---

## Example Usage

```bash
# Research a topic
curl -X POST http://127.0.0.1:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing"}'

# Compare two topics
curl -X POST http://127.0.0.1:8000/compare \
  -H "Content-Type: application/json" \
  -d '{"topic_a": "Python", "topic_b": "JavaScript"}'

# Chat about the report
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "question": "Summarize the key risks"}'
```



## Requirements

```txt
fastapi
uvicorn
langchain==0.3.14
langchain-groq==0.2.4
langchain-community==0.3.14
python-dotenv
```

---

## Author

**Kajal Bajpayi** — GenAI Developer · LLM Applications & Agents

[![GitHub](https://img.shields.io/badge/GitHub-kajal--bajpayi-black?logo=github)](https://github.com/kajal-bajpayi)

---

