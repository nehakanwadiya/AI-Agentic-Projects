import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from pypdf import PdfReader
from groq import Groq

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎯",
    layout="wide"
)

st.title("AI Career Assistant")
st.markdown("**Powered by LLaMA 3.3 · Built by Neha Kanwadiya, IIT Bombay**")
st.divider()

# ── SIDEBAR INPUTS ──
with st.sidebar:
    st.header("Your Details")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    
    if uploaded_file:
        st.success("Resume uploaded")
    
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. Enter Groq API key")
    st.markdown("2. Upload resume PDF")
    st.markdown("3. Paste job description")
    st.markdown("4. Pick a feature tab")
    st.markdown("5. Click analyse")

job_description = st.text_area(
    "Paste Job Description",
    height=150,
    placeholder="Paste any job description here..."
)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Fit Analysis",
    "ATS Scanner", 
    "Interview Prep",
    "Cover Letter",
    "LinkedIn Message"
])

def extract_resume(pdf_file):
    reader = PdfReader(pdf_file)
    return "".join(page.extract_text() for page in reader.pages)

def validate():
    if not api_key:
        st.error("Enter your Groq API key in the sidebar")
        return False
    if not uploaded_file:
        st.error("Upload your resume PDF in the sidebar")
        return False
    if not job_description:
        st.error("Paste a job description above")
        return False
    return True

# ── TAB 1: FIT ANALYSIS + COVER LETTER ──
with tab1:
    st.subheader("Job Fit Analysis")
    if st.button("Analyse Fit", type="primary", key="fit"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Analysing fit..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""You are an expert recruiter.

JOB DESCRIPTION: {job_description}
RESUME: {resume_text}

Provide:
1. Top 5 required skills from JD
2. Match score out of 10 (number only, e.g. 7.5)
3. Candidate's 3 strongest matching points
4. 2 skill gaps
5. 3 keywords to add to resume"""}]
                )
                result = response.choices[0].message.content

                # Extract score for visual meter
                score_resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", 
                               "content": f"Extract only the numeric score out of 10 from this text. Return only the number, nothing else: {result}"}]
                )
                try:
                    score = float(score_resp.choices[0].message.content.strip())
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("Fit Score", f"{score}/10")
                    with col2:
                        st.progress(score/10)
                except:
                    pass

                st.divider()
                st.markdown(result)

# ── TAB 2: ATS SCANNER ──
with tab2:
    st.subheader("ATS Keyword Scanner")
    st.caption("Check if your resume will pass automated screening filters")
    if st.button("Scan ATS Compatibility", type="primary", key="ats"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Scanning ATS compatibility..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""You are an ATS system.

JOB DESCRIPTION: {job_description}
RESUME: {resume_text}

Analyse ATS compatibility:
1. Keywords PRESENT in resume (list all matches)
2. Keywords MISSING from resume (list all gaps)
3. ATS pass probability: High / Medium / Low
4. Top 5 specific suggestions to improve ATS score
5. Exact phrases to add to resume for this role"""}]
                )
                st.markdown(response.choices[0].message.content)

# ── TAB 3: INTERVIEW PREP ──
with tab3:
    st.subheader("Interview Preparation")
    st.caption("AI-generated questions based on YOUR resume and this specific JD")
    if st.button("Generate Interview Questions", type="primary", key="interview"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Generating personalised interview questions..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""You are a senior interviewer at a top tech company.

JOB DESCRIPTION: {job_description}
CANDIDATE RESUME: {resume_text}

Generate:
1. 3 DSA/Technical questions likely for this role
2. 3 questions about their specific projects (be specific to their actual projects)
3. 3 behavioral STAR questions for this role
4. 2 system design questions at intern level
5. Brief suggested answer approach for each (2-3 lines)

Be very specific to their actual experience and projects."""}]
                )
                st.markdown(response.choices[0].message.content)

# ── TAB 4: COVER LETTER ──
with tab4:
    st.subheader("Cover Letter Generator")
    if st.button("Generate Cover Letter", type="primary", key="cover"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Writing cover letter..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""Write a professional cover letter.

RESUME: {resume_text}
JOB: {job_description}

Rules:
- Exactly 3 short paragraphs
- Paragraph 1: Who they are + college + role (2 sentences)
- Paragraph 2: Most relevant internship + project (3 sentences)
- Paragraph 3: Why this company + call to action (2 sentences)
- No Dear Hiring Manager
- No filler phrases
- 120-150 words total
- Confident, direct, human tone"""}]
                )
                cover = response.choices[0].message.content
                st.markdown(cover)
                st.divider()
                st.text_area("Copy:", value=cover, height=200)

# ── TAB 5: LINKEDIN MESSAGE ──
with tab5:
    st.subheader("LinkedIn Cold Message")
    st.caption("Message to send to the hiring manager directly")
    if st.button("Generate LinkedIn Message", type="primary", key="linkedin"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Writing LinkedIn message..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""Write a LinkedIn connection request message.

JOB: {job_description}
CANDIDATE RESUME: {resume_text}

Rules:
- Maximum 5 sentences
- Start with Hi [Name],
- Mention college and one specific achievement
- Reference something specific about the company or role
- End with clear ask
- Under 100 words
- Natural, not salesy"""}]
                )
                msg = response.choices[0].message.content
                st.markdown(msg)
                st.divider()
                st.text_area("Copy:", value=msg, height=150)

# ── FOOTER ──
st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: 12px;'>
Built by Neha Kanwadiya · IIT Bombay · 
<a href='https://github.com/nehakanwadiya'>GitHub</a> · 
<a href='https://www.linkedin.com/in/neha-kanwadiya-076063290/'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
