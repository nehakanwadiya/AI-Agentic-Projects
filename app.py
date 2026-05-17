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
    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    if uploaded_file:
        st.success("Resume uploaded")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. Upload resume PDF")
    st.markdown("2. Paste job description")
    st.markdown("3. Pick a feature tab")
    st.markdown("4. Click analyse")

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
                
                # ATS Analysis
                ats_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""You are an ATS system.

JOB DESCRIPTION: {job_description}
RESUME: {resume_text}

Analyse ATS compatibility:
1. Keywords PRESENT in resume (list all matches)
2. Keywords MISSING from resume (list all gaps)
3. ATS pass probability: High / Medium / Low with reason
4. Top 5 specific suggestions to improve ATS score
5. Exact phrases to add to resume for this role"""}]
                )
                st.markdown(ats_response.choices[0].message.content)
                
                st.divider()
                
                # Resume rewrite suggestion
                st.subheader("How Your Resume Should Look for This Role")
                st.caption("AI-suggested resume bullet points tailored to this specific JD")
                
                with st.spinner("Generating tailored resume suggestions..."):
                    resume_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"""You are an expert resume coach.

CANDIDATE RESUME: {resume_text}
TARGET JOB: {job_description}

Rewrite and suggest improvements for this candidate's resume to match this job:

1. Suggested Professional Summary (2-3 lines tailored to this JD)
2. Rewritten bullet points for their most relevant internship 
   (make it match JD keywords, add metrics where possible)
3. Rewritten bullet points for their most relevant project
   (highlight skills the JD is asking for)
4. Skills section — exactly what to list for this role
5. What to remove or de-emphasise for this specific role

Be very specific — use their actual experience, just reframe it for this JD."""}]
                    )
                    
                    st.markdown(resume_response.choices[0].message.content)

# ── TAB 3: INTERVIEW PREP ──
with tab3:
    st.subheader("Interview Preparation")
    st.caption("Personalised questions based on YOUR resume and this JD — solve first, then reveal answers")
    if st.button("Generate Interview Questions", type="primary", key="interview"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Generating personalised interview questions..."):
                client = Groq(api_key=api_key)
                
                # Generate questions only first
                q_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""You are a senior interviewer at a top tech company.

JOB DESCRIPTION: {job_description}
CANDIDATE RESUME: {resume_text}

Generate exactly 10 interview questions only. No answers yet.

Format exactly like this:
DSA/Technical:
Q1. [question]
Q2. [question]
Q3. [question]

Project-Specific:
Q4. [question based on their actual projects]
Q5. [question based on their actual projects]
Q6. [question based on their actual projects]

Behavioral:
Q7. [STAR format question]
Q8. [STAR format question]
Q9. [STAR format question]

System Design:
Q10. [intern level system design question]

Be specific to their actual resume projects and experience."""}]
                )
                questions = q_response.choices[0].message.content
                st.markdown(questions)
                
                st.divider()
                st.info("Try answering the questions yourself first, then reveal the suggested answers below.")
                
                # Generate answers separately — hidden behind expanders
                with st.spinner("Preparing answer guides..."):
                    a_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"""You are a senior interviewer.

CANDIDATE RESUME: {resume_text}
JOB: {job_description}

These were the interview questions generated:
{questions}

Now provide suggested answer approaches for each question.
For each answer:
- Reference their actual projects/internships from resume
- Give a 3-4 line answer approach
- For DSA questions: give approach + time complexity
- For behavioral: give STAR format outline
- For system design: give key components to mention

Format:
A1. [answer approach]
A2. [answer approach]
...and so on"""}]
                    )
                    answers = a_response.choices[0].message.content
                
                # Split answers and show each behind expander
                st.subheader("Suggested Answer Guides")
                answer_lines = answers.split('\n')
                
                current_q = ""
                current_a = []
                q_num = 0
                
                for line in answer_lines:
                    if line.strip().startswith('A') and '.' in line[:3]:
                        if current_q and current_a:
                            with st.expander(f"Reveal Answer for Q{q_num}"):
                                st.markdown('\n'.join(current_a))
                        q_num += 1
                        current_q = line
                        current_a = [line]
                    elif current_q:
                        current_a.append(line)
                
                # Last answer
                if current_q and current_a:
                    with st.expander(f"Reveal Answer for Q{q_num}"):
                        st.markdown('\n'.join(current_a))

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
    st.caption("Humble, formal cold outreach message to send to hiring managers")
    if st.button("Generate LinkedIn Message", type="primary", key="linkedin"):
        if validate():
            resume_text = extract_resume(uploaded_file)
            with st.spinner("Writing LinkedIn message..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"""Write a humble, formal LinkedIn cold outreach message.

CANDIDATE RESUME: {resume_text}
JOB: {job_description}

Rules:
- Start with: Hi [Name],
- Introduce yourself as a third-year student at your college
- Mention 2-3 relevant skills or experiences in one line
- Say you are exploring internship opportunities at [Company]
- Express genuine interest in connecting
- End with: Would love to connect!
- Maximum 4 sentences
- Under 80 words
- Humble, warm, and formal — not salesy
- No achievements bragging — just a genuine introduction

Example style:
Hi [Name], I'm a third-year student at IIT Bombay with experience in 
backend development, REST APIs, and AI/ML projects. I'm currently 
exploring SWE and AI internship opportunities at [Company] and would 
love to connect!"""}]
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