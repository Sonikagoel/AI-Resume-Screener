import streamlit as st
import hashlib
import json
import csv
import io
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from ai_engine import analyze_resume
from resume_parser import extract_text_from_uploaded_file


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeAI | Smart Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #eef2ff;
    }

    [data-testid="stSidebar"] {
        background: #11182b;
        border-right: 1px solid #29334d;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.9);
    }

    h1, h2, h3 {
        color: #f4f6ff !important;
    }

    p, label, li {
        color: #c5cde0;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 18px;
        background: linear-gradient(120deg, #182647, #33245f);
        border: 1px solid #45416e;
        margin-bottom: 24px;
    }

    .hero-label {
        color: #c4b5fd;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 12px;
        font-weight: 700;
    }

    .hero-title {
        color: #ffffff;
        font-size: 38px;
        font-weight: 800;
        margin: 8px 0;
    }

    .hero-description {
        color: #d1d8ed;
        font-size: 15px;
        line-height: 1.7;
    }

    .section-label {
        color: #a5b4fc;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }

    .metric-card {
        background: #141c31;
        border: 1px solid #2b3652;
        border-radius: 15px;
        padding: 20px;
        min-height: 120px;
    }

    .metric-label {
        color: #9daac5;
        font-size: 13px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 29px;
        font-weight: 800;
        margin-top: 9px;
    }

    .candidate-card {
        background: #141c31;
        border: 1px solid #2b3652;
        border-radius: 14px;
        padding: 17px;
        margin: 10px 0;
    }

    .candidate-name {
        color: #ffffff;
        font-size: 17px;
        font-weight: 700;
    }

    .candidate-meta {
        color: #9daac5;
        font-size: 12px;
        margin-top: 5px;
    }

    .score {
        color: #c4b5fd;
        font-size: 24px;
        font-weight: 800;
        text-align: right;
    }

    .tag {
        display: inline-block;
        padding: 5px 9px;
        margin: 3px 4px 3px 0;
        border-radius: 7px;
        font-size: 12px;
        background: #252449;
        color: #d9d6ff;
        border: 1px solid #474078;
    }

    .info-box {
        background: #141c31;
        border: 1px solid #2b3652;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #7563ef, #9b6dff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 700;
        min-height: 44px;
    }

    div.stButton > button:hover {
        border: 1px solid #c4b5fd;
        color: white;
    }

    div[data-testid="stMetric"] {
        background: #141c31;
        border: 1px solid #2b3652;
        border-radius: 12px;
        padding: 15px;
    }

    div[data-testid="stExpander"] {
        background: #11182b;
        border: 1px solid #2b3652;
        border-radius: 12px;
    }

    .stTextArea textarea {
        background: #11182b;
        color: #ffffff;
        border: 1px solid #34415f;
        border-radius: 10px;
    }

    .footer {
        text-align: center;
        color: #71809e;
        font-size: 12px;
        padding: 25px 0 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "processed_resume_hashes" not in st.session_state:
    st.session_state.processed_resume_hashes = set()

if "results" not in st.session_state:
    st.session_state.results = []

if "failures" not in st.session_state:
    st.session_state.failures = []

if "last_job_description" not in st.session_state:
    st.session_state.last_job_description = ""


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def fingerprint(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()[:12]


def render_tags(values):
    if not values:
        return '<span class="tag">None identified</span>'

    return "".join(
        f'<span class="tag">{escape(str(value))}</span>'
        for value in values
    )


def create_pdf_report(results, job_description):
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("ResumeAI Screening Report", styles["Title"])
    )
    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Job Description:</b> "
            + escape(job_description[:1500]),
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 18))

    table_data = [["Rank", "Candidate", "Match Score"]]

    for rank, item in enumerate(results, start=1):
        analysis = item["analysis"]
        table_data.append([
            str(rank),
            analysis.candidate_name,
            f"{analysis.match_score:.2f}%",
        ])

    table = Table(
        table_data,
        colWidths=[0.7 * inch, 3.5 * inch, 1.5 * inch],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#243B53"),
            ),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(
        Paragraph("Candidate Rankings", styles["Heading2"])
    )
    story.append(table)
    story.append(Spacer(1, 20))

    for rank, item in enumerate(results, start=1):
        analysis = item["analysis"]

        story.append(
            Paragraph(
                f"Candidate {rank}: "
                f"{escape(analysis.candidate_name)}",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Match Score:</b> "
                f"{analysis.match_score:.2f}%",
                styles["Normal"],
            )
        )

        for heading, values in [
            ("Skills Detected", analysis.skills),
            ("Required Skills", analysis.required_skills),
            ("Matched Skills", analysis.matched_skills),
            ("Missing Skills", analysis.missing_skills),
            ("Strengths", analysis.strengths),
        ]:
            story.append(
                Paragraph(
                    f"<b>{escape(heading)}:</b>",
                    styles["Normal"],
                )
            )

            value_text = (
                ", ".join(str(value) for value in values)
                if values
                else "None identified"
            )

            story.append(
                Paragraph(escape(value_text), styles["Normal"])
            )
            story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                "<b>Summary:</b> "
                + escape(analysis.summary),
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 18))

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 📄 ResumeAI")
    st.caption("SMART TALENT SCREENING")

    st.divider()

    st.markdown("### Screening controls")
    st.write("Upload resumes and compare them against a job description.")

    if st.button(
        "🗑️ Clear results & reset duplicates",
        use_container_width=True,
    ):
        st.session_state.results = []
        st.session_state.failures = []
        st.session_state.processed_resume_hashes = set()
        st.session_state.last_job_description = ""
        st.rerun()

    st.divider()

    st.markdown("### Built with")
    st.write("🐍 Python")
    st.write("🧠 Groq LLM")
    st.write("📊 Streamlit")
    st.write("🛡️ Pydantic")

    st.caption("ResumeAI · Portfolio Project")


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">AI-powered recruitment</div>
        <div class="hero-title">Find the right talent.</div>
        <div class="hero-description">
            Screen resumes, compare job requirements, and discover
            promising candidates with structured AI-assisted analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-label">01 / Define the role</div>',
    unsafe_allow_html=True,
)
st.markdown("### Job description")

job_description = st.text_area(
    "Job description",
    height=220,
    placeholder=(
        "Paste the complete job description here, "
        "including required skills and responsibilities..."
    ),
    label_visibility="collapsed",
)

if job_description.strip():
    st.caption(
        f"JD fingerprint: {fingerprint(job_description)}"
    )

st.markdown(
    '<div class="section-label">02 / Add candidates</div>',
    unsafe_allow_html=True,
)
st.markdown("### Upload resumes")

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="Exact duplicate files are rejected within this session.",
)

if uploaded_files:
    st.caption(
        f"{len(uploaded_files)} file(s) selected for screening."
    )


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if st.button("🚀 Analyze resumes", type="primary"):

    if not job_description.strip():
        st.error("Please enter a job description.")

    elif not uploaded_files:
        st.error("Please upload at least one resume.")

    else:
        seen_hashes = set(
            st.session_state.processed_resume_hashes
        )

        successful_hashes = set()
        new_results = []
        new_failures = []
        duplicate_count = 0

        progress = st.progress(0)
        status = st.empty()

        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):
            filename = uploaded_file.name

            status.write(
                f"Screening {index + 1}/{total_files}: {filename}"
            )

            try:
                file_bytes = uploaded_file.getvalue()

                file_hash = hashlib.sha256(
                    file_bytes
                ).hexdigest()

                if file_hash in seen_hashes:
                    duplicate_count += 1
                    st.warning(
                        f"Duplicate rejected: {filename}"
                    )
                    progress.progress(
                        (index + 1) / total_files
                    )
                    continue

                resume_text = extract_text_from_uploaded_file(
                    uploaded_file
                )

                if not resume_text or not resume_text.strip():
                    raise ValueError(
                        "No readable text found in this resume."
                    )

                resume_fingerprint = fingerprint(resume_text)
                jd_fingerprint = fingerprint(job_description)

                with st.expander(
                    f"Input verification: {filename}"
                ):
                    st.write(
                        "Resume fingerprint:",
                        resume_fingerprint,
                    )
                    st.write(
                        "JD fingerprint:",
                        jd_fingerprint,
                    )
                    st.write(
                        "Extracted text length:",
                        len(resume_text),
                    )

                analysis = analyze_resume(
                    resume_text,
                    job_description,
                )

                new_results.append({
                    "filename": filename,
                    "file_hash": file_hash,
                    "resume_fingerprint": resume_fingerprint,
                    "jd_fingerprint": jd_fingerprint,
                    "analysis": analysis,
                })

                successful_hashes.add(file_hash)
                seen_hashes.add(file_hash)

            except Exception as error:
                new_failures.append({
                    "filename": filename,
                    "error": str(error),
                })
                st.error(
                    f"Could not analyze {filename}: {error}"
                )

            progress.progress(
                (index + 1) / total_files
            )

        st.session_state.processed_resume_hashes.update(
            successful_hashes
        )

        # Replace previous results with this run's results.
        st.session_state.results = sorted(
            new_results,
            key=lambda item: item["analysis"].match_score,
            reverse=True,
        )

        st.session_state.failures = new_failures
        st.session_state.last_job_description = job_description

        status.success("Screening completed.")

        if duplicate_count:
            st.info(
                f"Rejected {duplicate_count} duplicate file(s)."
            )

        if new_results:
            st.success(
                f"Successfully screened {len(new_results)} "
                "new resume(s)."
            )

        if not new_results and duplicate_count:
            st.warning(
                "No new candidates were analyzed. "
                "Use the sidebar reset button before repeating "
                "the same test."
            )


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

results = st.session_state.results

if results:
    st.divider()

    st.markdown(
        '<div class="section-label">03 / Screening overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Candidate overview")

    scores = [
        item["analysis"].match_score
        for item in results
    ]

    average_score = sum(scores) / len(scores)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Candidates screened</div>
                <div class="metric-value">{len(results)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Highest match</div>
                <div class="metric-value">{max(scores):.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Average match</div>
                <div class="metric-value">{average_score:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<div class="section-label">04 / Candidate leaderboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Ranked candidates")

    for rank, item in enumerate(results, start=1):
        analysis = item["analysis"]

        st.markdown(
            f"""
            <div class="candidate-card">
                <div class="candidate-name">
                    #{rank} &nbsp; {escape(analysis.candidate_name)}
                </div>
                <div class="candidate-meta">
                    {escape(item["filename"])}
                </div>
                <div class="score">
                    {analysis.match_score:.1f}%
                </div>
                <div class="candidate-meta">
                    {len(analysis.matched_skills)} matched ·
                    {len(analysis.missing_skills)} missing
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(
            min(max(float(analysis.match_score) / 100, 0), 1)
        )

    st.divider()

    st.markdown(
        '<div class="section-label">05 / Candidate insights</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Detailed analysis")

    for rank, item in enumerate(results, start=1):
        analysis = item["analysis"]

        with st.expander(
            f"#{rank} · {analysis.candidate_name} · "
            f"{analysis.match_score:.1f}%"
        ):
            st.write(f"**Resume:** {item['filename']}")

            st.caption(
                f"Resume fingerprint: {item['resume_fingerprint']} "
                f" | JD fingerprint: {item['jd_fingerprint']}"
            )

            st.progress(
                min(max(float(analysis.match_score) / 100, 0), 1)
            )

            left, right = st.columns(2)

            with left:
                st.markdown("#### Matched skills")
                st.markdown(
                    render_tags(analysis.matched_skills),
                    unsafe_allow_html=True,
                )

            with right:
                st.markdown("#### Missing skills")
                st.markdown(
                    render_tags(analysis.missing_skills),
                    unsafe_allow_html=True,
                )

            st.markdown("#### All detected skills")
            st.markdown(
                render_tags(analysis.skills),
                unsafe_allow_html=True,
            )

            st.markdown("#### Required skills")
            st.markdown(
                render_tags(analysis.required_skills),
                unsafe_allow_html=True,
            )

            st.markdown("#### Strengths")

            if analysis.strengths:
                for strength in analysis.strengths:
                    st.write(f"✓ {strength}")
            else:
                st.write("No strengths identified.")

            st.markdown("#### AI summary")
            st.write(analysis.summary)

    # --------------------------------------------------
    # EXPORTS
    # --------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-label">06 / Export</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Download screening reports")

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)

    writer.writerow([
        "Rank",
        "Candidate Name",
        "Resume File",
        "Match Score",
        "Skills",
        "Required Skills",
        "Matched Skills",
        "Missing Skills",
        "Strengths",
        "Summary",
    ])

    for rank, item in enumerate(results, start=1):
        analysis = item["analysis"]

        writer.writerow([
            rank,
            analysis.candidate_name,
            item["filename"],
            analysis.match_score,
            ", ".join(analysis.skills),
            ", ".join(analysis.required_skills),
            ", ".join(analysis.matched_skills),
            ", ".join(analysis.missing_skills),
            ", ".join(analysis.strengths),
            analysis.summary,
        ])

    json_data = [
        {
            "rank": rank,
            "filename": item["filename"],
            "resume_fingerprint": item["resume_fingerprint"],
            "jd_fingerprint": item["jd_fingerprint"],
            "analysis": item["analysis"].model_dump(),
        }
        for rank, item in enumerate(results, start=1)
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "⬇️ Download CSV",
            data=csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="resume_screening_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "⬇️ Download JSON",
            data=json.dumps(
                json_data,
                indent=4,
                ensure_ascii=False,
            ),
            file_name="resume_screening_report.json",
            mime="application/json",
            use_container_width=True,
        )

    with col3:
        try:
            report_pdf = create_pdf_report(
                results,
                st.session_state.last_job_description,
            )

            st.download_button(
                "⬇️ Download PDF",
                data=report_pdf,
                file_name="resume_screening_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as error:
            st.error(f"Could not generate PDF: {error}")


# --------------------------------------------------
# FAILED FILES
# --------------------------------------------------

if st.session_state.failures:
    st.divider()
    st.subheader("⚠️ Files that failed to process")

    for failure in st.session_state.failures:
        st.error(
            f"{failure['filename']}: {failure['error']}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ResumeAI · Intelligent Resume Screening · Built with Python
    </div>
    """,
    unsafe_allow_html=True,
)