# AI Agent Projects — Neha Kanwadiya

Building production-grade agentic AI systems from scratch using free APIs.
No paid subscriptions — everything runs on Groq (free) + local embeddings.

---

## Progress
- [x] Day 1 — Groq API + LLM basics
- [x] Day 2 — Tool Use + RAG from scratch
- [x] Day 3 — LangChain Agent + Memory + RAG combined
- [ ] Day 4 — CrewAI Multi-Agent Job Analyser
- [ ] Day 5 — Streamlit UI deployment

---

## Projects Built

### 1. LLM Basics + Tool Use Agent
**File:** `day1_groq.ipynb`

First agent that calls Python functions autonomously — LLM decides which tool to use and when, without being explicitly told.

**What it does:**
- Answers questions using real-time tool calls
- Calls date, calculator, and weather functions by itself
- Demonstrates function calling / tool use from scratch

**Stack:** Groq API · LLaMA 3.3 70B · Python  
**Concepts:** Tool Use · Function Calling · Prompt Engineering

---

### 2. Resume RAG Chatbot
**File:** `day2_rag.ipynb`

Ask any question about a resume PDF — the agent retrieves relevant sections and answers using only the document. No hallucination.

**What it does:**
- Loads and chunks a PDF resume
- Converts chunks to vector embeddings (locally, no API needed)
- Stores in ChromaDB vector database
- Retrieves top-3 relevant chunks per question
- LLM answers strictly from retrieved context

**Stack:** Groq API · LLaMA 3.3 70B · ChromaDB · Sentence Transformers · PyPDF  
**Concepts:** RAG · Embeddings · Vector Database · Semantic Search

---

### 3. LangChain Conversational Agent (RAG + Memory + Tools)
**File:** `day3_langchain_agent.ipynb`

Full conversational AI assistant that remembers context across turns, searches a resume PDF, and uses tools — all in one pipeline.

**What it does:**
- Maintains conversation memory across multiple turns
- Retrieves resume context and injects into prompt dynamically
- Uses tools for date and math queries
- Answers follow-up questions without losing context

**Stack:** LangChain · LangGraph · Groq API · ChromaDB · Sentence Transformers  
**Concepts:** Conversational Memory · RAG · Context Injection · LangGraph Agents

---

### 4. CrewAI Multi-Agent Job Analyser *(Coming)*
Two AI agents collaborating — one researches a job description, one writes a personalised cover letter.

---

### 5. Streamlit Deployed UI *(Coming)*
Full web interface for the Job Analyser — deployed and publicly accessible.

---

## Architecture Overview