# InsightForge 🔬

> AI-powered research digest and comparison engine built with LangChain, Groq, and Streamlit.

## 🚀 Live Demo
👉 [Try InsightForge](https://insightforge-099.streamlit.app/)

InsightForge takes any topic and runs it through a 4-step AI pipeline — Researcher, Summarizer, Critic, and Report Writer — producing a polished research digest in seconds. It also features a unique Comparison Mode that researches two topics in parallel and generates a structured side-by-side analysis.

---

## Features

- **Single Topic Research** - generates a structured digest with overview, key findings, open questions, and conclusion
- **Comparison Mode** - researches two topics independently then produces a head-to-head comparison report
- **Conversation Memory** - ask follow-up questions about any generated report via a memory-aware chat interface
- **Download Reports** - every report is downloadable as a .txt file instantly
- **Streamlit UI** - clean, interactive web interface with sidebar navigation

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Framework | LangChain (LCEL) |
| Model | Groq - openai/gpt-oss-120b |
| UI | Streamlit |
| Memory | LangChain ChatPromptTemplate with history |
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
├── ui.py               # Streamlit interface (standalone, no FastAPI needed)
├── client.py           # Terminal-based interactive client
├── .env
└── requirements.txt
```

---

## Pipeline Architecture

### Single Topic Mode
```
User Input (topic)
      |
  Researcher     -> 5 key developments (bullet points)
      |
  Summarizer     -> 3-paragraph summary
      |
  Critic         -> 3 gaps and open questions
      |
  Report Writer  -> structured digest (Overview, Key Findings, Open Questions, Conclusion)
```

### Comparison Mode
```
Topic A -> Researcher -> Summarizer --|
                                      |--> Comparator -> Report Writer -> side-by-side digest
Topic B -> Researcher -> Summarizer --|
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/kajal-bajpayi/InsightForge.git
cd InsightForge
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

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

### 5. Run the Streamlit UI

```bash
streamlit run ui.py
```

Visit `http://localhost:8501` in your browser.

### 6. Run the Terminal Client (optional)

Make sure the FastAPI server is running first:

```bash
uvicorn app.main:app --reload
```

Then in a second terminal:

```bash
python client.py
```



## Requirements

```txt
streamlit
langchain
langchain-groq
langchain-core
python-dotenv
```

---

## Author

**Kajal Bajpayi** — GenAI Developer, LLM Applications and Agents

[![GitHub](https://img.shields.io/badge/GitHub-kajal--bajpayi-black?logo=github)](https://github.com/kajal-bajpayi)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-InsightForge-brightgreen)](https://insightforge-099.streamlit.app/)

---



