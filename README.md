# 🤖 AI Agentic Projects — Neha Kanwadiya

Building production-grade agentic AI systems from scratch using **free APIs only**.
---

##  Projects Built

### 1. LLM Basics + Tool Use Agent
**File:** `day1_groq.ipynb`

First agent that calls Python functions autonomously — LLM decides which tool to use and when, without being explicitly told.

**What it does:**
- Answers questions using real-time tool calls
- Calls date, calculator, and weather functions by itself
- Demonstrates function calling and tool use from scratch

**Stack:** Groq API · LLaMA 3.3 70B · Python  
**Concepts:** Tool Use · Function Calling · Prompt Engineering

---

### 2. Resume RAG Chatbot
**File:** `day2_RAG.ipynb`

Ask any question about a resume PDF — the agent retrieves relevant sections and answers using only the document. Zero hallucination.

**What it does:**
- Loads and chunks a PDF resume
- Converts chunks to vector embeddings locally (no API needed)
- Stores in ChromaDB vector database
- Retrieves top-3 relevant chunks per question
- LLM answers strictly from retrieved context

**Stack:** Groq API · LLaMA 3.3 70B · ChromaDB · Sentence Transformers · PyPDF  
**Concepts:** RAG · Embeddings · Vector Database · Semantic Search

---

### 3. LangChain Conversational Agent
**File:** `day3_LangChain.ipynb`

Full conversational AI assistant that remembers context across turns, searches a resume PDF, and uses tools — all in one pipeline.

**What it does:**
- Maintains conversation memory across multiple turns
- Retrieves resume context and injects into prompt dynamically
- Uses tools for date and math queries
- Answers follow-up questions without losing context

**Stack:** LangChain · LangGraph · Groq API · ChromaDB · Sentence Transformers  
**Concepts:** Conversational Memory · RAG · Context Injection · LangGraph Agents

---

### 4. CrewAI Multi-Agent Job Analyser
**File:** `day4_AI_multiagent.ipynb`

Two AI agents collaborating — Researcher analyses the job description, Writer drafts a personalised cover letter. Inspired by real production agentic systems.

**What it does:**
- Researcher Agent reads JD, extracts top skills, scores candidate fit out of 10
- Writer Agent uses researcher output to write a tailored cover letter
- Agents communicate and pass context automatically
- Dynamic function accepts any job description

**Stack:** CrewAI · Groq API · LLaMA 3.3 70B · LiteLLM  
**Concepts:** Multi-Agent Systems · Agent Orchestration · Task Chaining

---

### 5. Streamlit Web App — Job Fit Analyser
Full web interface wrapping the CrewAI multi-agent system. Upload any resume, paste any job description, get fit analysis and cover letter in 60 seconds.

**What it does:**
- Upload resume PDF → extracted automatically
- Paste any job description
- Two agents analyse fit and write cover letter
- Results displayed instantly in browser
- Publicly deployed and shareable

**Stack:** Streamlit · CrewAI · Groq API · PyPDF · Python  
**Concepts:** Full Stack AI App · Deployment · Multi-Agent · RAG
---

## Key Concepts Learned

| Concept | What it means |
|---|---|
| **Tool Use** | LLM autonomously decides when and which Python function to call |
| **RAG** | Agent reads documents before answering — no hallucination |
| **Embeddings** | Text converted to vectors — similar meaning = close in space |
| **Vector DB** | Database optimised for similarity search on embeddings |
| **Memory** | Conversation history passed to agent so it remembers context |
| **Multi-Agent** | Multiple LLMs with different roles collaborating on one task |
| **Context Injection** | Relevant docs injected into prompt directly — more reliable than tool calling |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API — LLaMA 3.3 70B (free) |
| Agent Framework | LangChain + LangGraph |
| Multi-Agent | CrewAI |
| Vector DB | ChromaDB (local) |
| Embeddings | Sentence Transformers — all-MiniLM-L6-v2 (local, free) |
| PDF Reading | PyPDF |
| UI | Streamlit |
| Language | Python 3.x |

---

##  How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/nehakanwadiya/AI-Agentic-Projects.git

# 2. Install dependencies
pip install streamlit crewai langchain-groq langgraph chromadb sentence-transformers pypdf litellm

# 3. Run the app
streamlit run app.py

# 4. Get free Groq API key at console.groq.com
# Enter it in the app when prompted
```

---

##  Build Timeline
Built in 5 days 
---

##  About
Built as part of a structured placement preparation plan targeting  
high-paying product companies at IIT Bombay.

**Contact:**  
📧 23b1852@iitb.ac.in  
🔗 [LinkedIn](https://www.linkedin.com/in/neha-kanwadiya-076063290/)  
💻 [GitHub](https://github.com/nehakanwadiya)