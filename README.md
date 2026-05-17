# 🤖 AI Career Assistant — Neha Kanwadiya
> B.Tech. Engineering Physics · IIT Bombay · 2027

An AI-powered web app that analyses your resume against any job description and instantly generates everything you need to apply — fit score, ATS report, interview questions, cover letter, and LinkedIn message.

🔗 **Live Demo:** [Try it here](https://ai-agentic-projects.streamlit.app)  
> No sign up. No API key. Just upload your resume and paste a job description.

---

## What Does This Do?

Most job applications fail before a human even reads them.
Your resume gets rejected by ATS filters. Your cover letter is generic.
You walk into interviews unprepared.

**This app fixes all of that in 60 seconds.**

Upload your resume PDF → paste any job description → get:

---

## 5 Features

###  Fit Analysis
See exactly how well your resume matches the job — before you apply.
- Match score out of 10 with a visual progress bar
- Your 3 strongest matching points
- Skill gaps you need to address
- Keywords missing from your resume

###  ATS Scanner
Most companies filter resumes automatically before humans see them.
- Checks which JD keywords are present or missing in your resume
- Gives ATS pass probability: High / Medium / Low
- Rewrites your resume bullet points to match this specific JD
- Tells you exactly what to add, remove, or reframe

###  Interview Prep
10 personalised interview questions based on YOUR resume and this specific JD.
- 3 DSA / Technical questions
- 3 questions about your actual projects
- 3 behavioral STAR questions
- 1 system design question
- Answers hidden — attempt first, then reveal with one click

###  Cover Letter
A ready-to-send cover letter in 3 short paragraphs.
- Tailored to the specific job and company
- References your most relevant internship and project
- 120-150 words — short enough to actually get read
- No filler phrases, no Dear Hiring Manager

###  LinkedIn Cold Message
A humble, formal message to send directly to the hiring manager.
- Under 80 words
- Introduces you naturally without bragging
- Mentions your college and relevant experience
- Ends with a genuine ask to connect

---

## How to Use

```
1. Open the app → link above
2. Upload your resume PDF (sidebar)
3. Paste any job description in the text box
4. Click any tab → click the button
5. Get results in 30 seconds
```

That's it. No account. No API key. Completely free.

---

## Who Is This For?

- **Students** applying for internships and placements
- **Fresh graduates** entering the job market
- **Anyone** who wants to stop applying blindly and start applying smart

---

## Example Output

**Input:** Neha's resume + Razorpay SWE Intern JD

**Fit Score:** 8.5/10

**ATS:** High pass probability — 12/15 keywords matched

**Cover Letter:**
> I am Neha Kanwadiya, a third-year Engineering Physics student at IIT Bombay, applying for the Software Engineering Intern role at Razorpay. At GradPipe, I built backend pipelines for an AI-driven developer marketplace, and my multi-agent Job Analyser directly applies LLMs and RAG to real product problems. Razorpay's scale and product complexity is exactly the environment I want to grow in — I have attached my resume and would love to connect over a quick call.

**LinkedIn Message:**
> Hi [Name], I'm a third-year student at IIT Bombay with experience in backend development, REST APIs, and AI/ML projects. I'm currently exploring SWE internship opportunities at Razorpay and would love to connect!

---

## Built With

| | |
|---|---|
| **AI Model** | LLaMA 3.3 70B via Groq API (free) |
| **UI** | Streamlit |
| **PDF Reading** | PyPDF |
| **Deployment** | Streamlit Cloud |
| **Language** | Python |

---

##  Project Journey

### Day 1 - LLM Basics
**File:** `day1_groq.ipynb`

First contact with LLMs via Groq API. Learned how to make raw API calls, structure prompts, and get responses from LLaMA 3.3 70B.

**Concepts:** LLM API · Prompt Engineering · Response Parsing  
**Stack:** Groq API · LLaMA 3.3 70B · Python

---

### Day 2 — Tool Use + RAG From Scratch
**File:** `day2_RAG.ipynb`

Built two foundational agentic AI concepts from scratch — no frameworks, pure Python.

**Tool Use:** LLM autonomously decides which Python function to call and when — demonstrated with date, calculator, and weather tools.

**RAG Pipeline:**
- Loaded and chunked resume PDF into 350-character segments
- Converted chunks to vector embeddings using Sentence Transformers (local, free)
- Stored in ChromaDB vector database
- Retrieved top-3 relevant chunks per question via semantic similarity
- LLM answers strictly from retrieved context — zero hallucination

**Concepts:** Tool Use · Function Calling · RAG · Embeddings · Vector Database · Semantic Search  
**Stack:** Groq API · ChromaDB · Sentence Transformers · PyPDF

---

### Day 3 — LangChain Conversational Agent
**File:** `day3_LangChain.ipynb`

Full conversational AI assistant combining tools, RAG, and persistent memory in one pipeline.

**What was built:**
- LangGraph-based agent with tool calling
- Conversation memory via MemorySaver — agent remembers context across turns
- Dynamic RAG — resume context injected into prompt based on question type
- Interactive chatbot loop with follow-up question handling

**Key insight:** Context injection (fetching chunks in Python, injecting into prompt) is more reliable than tool-based RAG for free-tier LLMs.

**Concepts:** Conversational Memory · LangGraph Agents · Context Injection · RAG  
**Stack:** LangChain · LangGraph · Groq API · ChromaDB · Sentence Transformers

---

### Day 4 — CrewAI Multi-Agent System
**File:** `day4_AI_multiagent.ipynb`

Two specialised AI agents collaborating on a shared task — directly inspired by production agentic systems like Microsoft's Shiproom Agent.

**Agents:**
- **Researcher Agent** — reads JD, extracts top skills, scores candidate fit, identifies keywords
- **Writer Agent** — receives researcher's analysis, writes a tailored cover letter

**Task chaining:** Writer automatically receives Researcher's output — no manual passing needed. CrewAI orchestrates the full pipeline.

**Concepts:** Multi-Agent Systems · Agent Orchestration · Task Chaining · Role-Based Agents  
**Stack:** CrewAI · Groq API · LiteLLM · Python

---

### Day 5 — Streamlit Web App (Deployed)
**File:** `app.py` · **[Live Demo](https://ai-agentic-projects.streamlit.app)**

Production-grade web application wrapping everything into a clean, tabbed interface. Publicly deployed — no installation needed.

**5 features across 5 tabs:**
- Fit Analysis with visual score meter
- ATS keyword scanner with resume rewrite suggestions
- Interview prep with 10 personalised Q&A (answers hidden behind expanders)
- Cover letter generator (120-150 words, 3 paragraphs)
- LinkedIn cold message generator (humble, formal, under 80 words)

**Architecture decision:** Removed CrewAI from deployment — used direct Groq API calls for stability on Streamlit Cloud's Python 3.14 environment.

**Stack:** Streamlit · Groq API · PyPDF · Python

---

##  System Architecture

```
User (Resume PDF + Job Description)
              ↓
       Streamlit UI (app.py)
              ↓
    ┌─────────────────────────┐
    │      Groq API           │
    │   LLaMA 3.3 70B         │
    │                         │
    │  Call 1 → Fit Analysis  │
    │  Call 2 → Score Extract │
    │  Call 3 → ATS Scan      │
    │  Call 4 → Resume Rewrite│
    │  Call 5 → Questions     │
    │  Call 6 → Answers       │
    │  Call 7 → Cover Letter  │
    │  Call 8 → LinkedIn Msg  │
    └─────────────────────────┘
              ↓
    Results displayed in tabs
```

---

##  Key Concepts Learned

| Concept | Explanation |
|---|---|
| **Tool Use** | LLM decides autonomously which Python function to call and when |
| **RAG** | Retrieve relevant document chunks → inject into prompt → answer from context |
| **Embeddings** | Text converted to vectors where similar meaning = close distance in space |
| **Vector DB** | Database optimised for similarity search on embedding vectors |
| **Memory** | Full conversation history passed to agent each turn — simulates memory |
| **Multi-Agent** | Specialised agents with different roles collaborate via task chaining |
| **Context Injection** | More reliable than tool-based RAG for free-tier LLMs |
| **Streamlit Secrets** | Secure API key management — never hardcode keys in public repos |

---

##  Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Groq API — LLaMA 3.3 70B (free) |
| **Agent Framework** | LangChain + LangGraph |
| **Multi-Agent** | CrewAI |
| **Vector DB** | ChromaDB (local) |
| **Embeddings** | Sentence Transformers — all-MiniLM-L6-v2 (local, free) |
| **PDF Reading** | PyPDF |
| **UI + Deployment** | Streamlit Cloud |
| **Language** | Python 3.x |

---

##  Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/nehakanwadiya/AI-Agentic-Projects.git
cd AI-Agentic-Projects

# 2. Install dependencies
pip install streamlit groq pypdf

# 3. Add your Groq API key (free at console.groq.com)
mkdir .streamlit
echo 'GROQ_API_KEY = "your_key_here"' > .streamlit/secrets.toml

# 4. Run
streamlit run app.py
```


##  About the builder

Built during placement preparation at IIT Bombay targeting high-paying  
product companies.

**Contact:**   
 [LinkedIn](https://www.linkedin.com/in/neha-kanwadiya-076063290/)  
 [GitHub](https://github.com/nehakanwadiya)