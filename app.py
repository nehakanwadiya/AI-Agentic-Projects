import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from pypdf import PdfReader
from groq import Groq

st.set_page_config(
    page_title="Job Fit Analyser",
    page_icon="🎯",
    layout="centered"
)

st.title("Job Fit Analyser")
st.markdown("**Powered by LLaMA 3.3 · Built by Neha Kanwadiya, IIT Bombay**")
st.divider()

col1, col2 = st.columns(2)
with col1:
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
with col2:
    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Paste any job description here..."
)

def extract_resume(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyse_fit(api_key, resume_text, job_desc):
    client = Groq(api_key=api_key)

    research = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"""You are an expert recruiter.

JOB DESCRIPTION:
{job_desc}

CANDIDATE RESUME:
{resume_text}

Provide:
1. Top 5 required skills from JD
2. Match score out of 10 with reasoning
3. Candidate's 3 strongest matching points
4. 2 gaps or missing skills
5. 3 keywords to use in cover letter"""}]
    )
    research_result = research.choices[0].message.content

    cover = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"""You are a professional cover letter writer.

Based on this analysis:
{research_result}

And this resume:
{resume_text}

Write a cover letter:
- Exactly 3 short paragraphs
- Paragraph 1: Who they are + college + role applying for (2 sentences)
- Paragraph 2: Most relevant internship + project (3 sentences)
- Paragraph 3: Why this company + call to action (2 sentences)
- No Dear Hiring Manager
- No filler like I am excited or I am passionate
- 120-150 words total
- Confident, direct, human tone"""}]
    )

    return research_result, cover.choices[0].message.content

if st.button("Analyse Fit + Generate Cover Letter", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API key")
    elif not uploaded_file:
        st.error("Please upload your resume PDF")
    elif not job_description:
        st.error("Please paste a job description")
    else:
        with st.spinner("Reading resume..."):
            resume_text = extract_resume(uploaded_file)

        with st.spinner("Agents analysing... please wait 30 seconds"):
            try:
                research_result, cover_letter = analyse_fit(
                    api_key, resume_text, job_description
                )

                st.success("Done!")
                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Fit Analysis")
                    st.markdown(research_result)
                with col2:
                    st.subheader("Cover Letter")
                    st.markdown(cover_letter)

                st.divider()
                st.text_area("Copy cover letter:", value=cover_letter, height=250)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: 12px;'>
Built by Neha Kanwadiya · IIT Bombay · 
<a href='https://github.com/nehakanwadiya'>GitHub</a> · 
<a href='https://www.linkedin.com/in/neha-kanwadiya-076063290/'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
