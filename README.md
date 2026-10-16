# ResumeAI — AI-Powered Resume Screening

ResumeAI is an AI-powered resume screening application built with Python, Streamlit, and Generative AI. It analyzes resumes against job descriptions to identify relevant skills, highlight missing requirements, and calculate a skill-based match score.

The application aims to make initial resume screening more efficient by presenting candidate information in a structured and easy-to-understand format.

## Live Demo

**[Try ResumeAI Online](https://resumeai-yvrxjamyj539kb9tvmszr4.streamlit.app/)**

## Features

- **Resume Parsing:** Extract text from PDF and DOCX resumes.
- **AI-Powered Analysis:** Analyze resumes against job descriptions using the Groq API.
- **Skill Extraction:** Identify relevant skills mentioned in a candidate's resume.
- **Skill Matching:** Compare candidate skills with the requirements in a job description.
- **Missing Skills Identification:** Highlight required skills that are not matched.
- **Match Score:** Calculate a percentage based on matched required skills.
- **Candidate Summary:** Generate a concise summary of relevant qualifications.
- **Structured Validation:** Validate AI-generated results using Pydantic.
- **Error Handling:** Handle analysis errors and invalid resume files.
- **PDF Reports:** Generate screening reports in PDF format.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| Groq API | Generative AI analysis |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX document parsing |
| Pydantic | Data validation |
| python-dotenv | Local environment variable management |
| ReportLab | PDF report generation |

## How It Works

1. The user uploads a resume in PDF or DOCX format.
2. The application extracts readable text from the resume.
3. The user provides a job description.
4. The Groq API analyzes the resume against the job requirements.
5. The application processes and validates the structured AI response.
6. Python calculates the match score using matched required skills.
7. The application displays the candidate summary, matched skills, missing skills, strengths, and other analysis results.

## Match Score Calculation

The application calculates the score using:

**Match Score = (Matched Required Skills / Total Required Skills) × 100**

For example, if 8 out of 10 required skills are matched, the score is 80%.

The score is an indicative measure of skill alignment, not a guarantee of job suitability.

## Project Structure

```text
ResumeAI/
├── app.py
├── ai_engine.py
├── resume_parser.py
├── schemas.py
├── requirements.txt
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

Clone the project repository from GitHub, then navigate to the project directory.

```bash
cd ResumeAI
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Application

Configure the required environment variables before running the application. Keep API credentials out of source code and version control.

For local development, use a `.env` file and store the required Groq API key there.

For Streamlit Cloud deployment, configure the required secret through the application's Secrets settings.

**Never publish your actual API key in the README or commit it to GitHub.**

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to use the application.

## Testing

The application can be tested with:

- A strong-match resume and its corresponding job description.
- A weak-match resume to evaluate skill-matching behavior.
- An invalid PDF to test error handling.
- Different job descriptions to evaluate how requirements affect the analysis.

AI-generated results may vary. Review the identified skills and match score for accuracy before relying on the output.

## Limitations

- Analysis quality depends on the quality and readability of the resume and job description.
- Scanned PDFs may require OCR if their text cannot be extracted directly.
- AI-generated skill extraction and matching may contain errors.
- The match score is a screening aid, not an objective measure of a candidate's overall ability.
- Human review should remain part of hiring decisions.

## Future Improvements

- More comprehensive automated testing.
- Improved skill normalization and matching accuracy.
- Enhanced downloadable screening reports.
- Support for additional document formats.
- Analysis history and reporting features.

## Security and Responsible Use

- Keep API credentials in environment variables or secure platform settings.
- Avoid uploading sensitive candidate information without appropriate authorization.
- Do not use the match score as the sole basis for hiring or rejecting a candidate.
- Review AI-generated results for accuracy and fairness.

---

Built with Python, Streamlit, and Generative AI.
