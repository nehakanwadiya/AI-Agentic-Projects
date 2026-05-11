import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import os
from crewai import Agent, Task, Crew
from pypdf import PdfReader

# ─────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────
st.set_page_config(
    page_title="Job Fit Analyser",
    page_icon="🎯",
    layout="centered"
)

# ─────────────────────────────────────
# HEADER
# ─────────────────────────────────────
st.title("Job Fit Analyser")
st.markdown("**Powered by CrewAI + LLaMA 3.3 · Built by Neha Kanwadiya, IIT Bombay**")
st.divider()

# ─────────────────────────────────────
# INPUTS
# ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_..."
    )

with col2:
    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="""Software Engineering Intern — Full Stack + AI
Requirements:
- Python, React, REST APIs
- ML/AI exposure preferred
- IIT graduates preferred..."""
)

# ─────────────────────────────────────
# EXTRACT RESUME TEXT
# ─────────────────────────────────────
def extract_resume(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ─────────────────────────────────────
# RUN CREW
# ─────────────────────────────────────
def run_crew(api_key, resume_text, job_desc):
    os.environ["GROQ_API_KEY"] = api_key

    researcher = Agent(
        role="Job Description Analyst",
        goal="Analyse job descriptions and evaluate candidate fit",
        backstory="""You are an expert recruiter with 10 years experience.
        You identify top skills required and evaluate candidate fit precisely.""",
        llm="groq/llama-3.3-70b-versatile",
        verbose=False
    )

    writer = Agent(
        role="Cover Letter Specialist",
        goal="Write compelling personalised cover letters",
        backstory="""You are a professional career coach who has helped 
        500+ candidates land jobs at top tech companies.""",
        llm="groq/llama-3.3-70b-versatile",
        verbose=False
    )

    research_task = Task(
        description=f"""Analyse this job description:
{job_desc}

Evaluate fit for this candidate based on their resume:
{resume_text}

Provide:
1. Top 5 required skills
2. Match score out of 10 with reasoning
3. Candidate's strongest matching points
4. Gaps or missing skills
5. Keywords to use in cover letter""",
        expected_output="""Structured analysis with match score, 
        strengths, gaps, and keywords""",
        agent=researcher
    )

    write_task = Task(
    description=f"""Write a professional cover letter for this candidate.

Resume: {resume_text}
Job: {job_desc}

STRICT RULES:
- Exactly 3 short paragraphs
- Paragraph 1: Who you are + college + role applying for (2 sentences max)
- Paragraph 2: Most relevant internship + most relevant project (3 sentences max)  
- Paragraph 3: Why this company specifically + call to action (2 sentences max)
- No "Dear Hiring Manager" or greetings
- No filler phrases like "I am excited" or "I am passionate"
- No bullet points
- Total length: 120-150 words maximum
- Tone: Confident, direct, human — not robotic""",
    expected_output="""A 3 paragraph cover letter, 120-150 words, 
    confident tone, no greetings, no filler language""",
    agent=writer
)

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=False
    )

    return crew.kickoff()

# ─────────────────────────────────────
# ANALYSE BUTTON
# ─────────────────────────────────────
if st.button("Analyse Fit + Generate Cover Letter", type="primary"):
    
    # Validate inputs
    if not api_key:
        st.error("Please enter your Groq API key")
    elif not uploaded_file:
        st.error("Please upload your resume PDF")
    elif not job_description:
        st.error("Please paste a job description")
    else:
        # Extract resume
        with st.spinner("Reading resume..."):
            resume_text = extract_resume(uploaded_file)

        # Run crew
        with st.spinner("Agents working... Researcher analysing JD, Writer drafting cover letter..."):
            try:
                result = run_crew(api_key, resume_text, job_description)
                
                # Show result
                st.success("Done!")
                st.divider()
                
                st.subheader("Analysis + Cover Letter")
                st.markdown(str(result))
                
                # Copy button
                st.divider()
                st.text_area(
                    "Copy cover letter:",
                    value=str(result),
                    height=300
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try rephrasing the job description or check your API key")

# ─────────────────────────────────────
# FOOTER
# ─────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: 12px;'>
Built by Neha Kanwadiya · IIT Bombay · 
<a href='https://github.com/nehakanwadiya'>GitHub</a> · 
<a href='https://www.linkedin.com/in/neha-kanwadiya-076063290/'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)