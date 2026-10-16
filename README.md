# AI Resume Screener 🚀

An AI-powered resume screening application built with Python, Streamlit, and Groq AI. The application analyzes resumes against job descriptions, identifies matching and missing skills, and calculates a skill-based match percentage to help recruiters evaluate candidates more efficiently.

<p align="center">
  <a href="https://ai-resume-screener-7ihofvttjuboxbioctzl3v.streamlit.app/">
    <strong>🌐 Live Demo</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/Sonikagoel/AI-Resume-Screener">
    <strong>💻 GitHub Repository</strong>
  </a>
</p>

---

## 📌 Project Overview

AI Resume Screener is a recruitment assistance tool that simplifies the initial resume screening process.

Recruiters can upload resumes and provide a job description. The application extracts readable text from resumes, uses an AI model through the Groq API to identify relevant skills and qualifications, and presents structured candidate analysis.

The final match percentage is calculated using Python based on the required skills identified and the skills matched in the resume.

The goal is to reduce repetitive screening work and help recruiters review candidate qualifications more efficiently while keeping final hiring decisions under human control.

## ✨ Features

- 📄 **Resume Upload:** Upload candidate resumes for screening.
- 📑 **PDF and DOCX Support:** Extract readable text from supported document formats.
- 🤖 **AI-Powered Analysis:** Analyze resumes against job descriptions using Groq AI.
- 🛠️ **Skill Extraction:** Identify relevant skills and qualifications from resumes.
- 🎯 **Job Description Matching:** Compare candidate skills with job requirements.
- 📊 **Match Percentage:** Calculate a score based on matched required skills.
- 🔍 **Missing Skills Identification:** Highlight required skills not evidenced in a resume.
- 💡 **Candidate Strengths:** Summarize relevant qualifications and strengths.
- 📝 **Candidate Summary:** Generate a concise overview of the candidate's profile.
- 🧹 **Data Cleaning:** Remove duplicate and empty skill entries.
- ✅ **Structured Validation:** Validate AI-generated data using Pydantic.
- 🌐 **Interactive Web Interface:** Provide screening results through Streamlit.
- ☁️ **Cloud Deployment:** Deploy the application using Streamlit Community Cloud.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and score calculation |
| Streamlit | Interactive web interface |
| Groq API | AI-powered resume analysis |
| `openai/gpt-oss-20b` | Configured AI model used through Groq |
| PyMuPDF | PDF text extraction, if used by the parser |
| `python-docx` | DOCX text extraction |
| Pydantic | Data validation and structured output |
| `python-dotenv` | Loading local environment variables |
| Git | Version control |
| GitHub | Source code hosting |
| Streamlit Community Cloud | Application deployment |

## 🔄 How It Works

The application follows these steps:

1. **Upload resumes:** The recruiter uploads one or more candidate resumes.
2. **Extract text:** The resume parser extracts readable text from supported documents.
3. **Enter job description:** The recruiter provides the job description and required qualifications.
4. **AI analysis:** The Groq API analyzes the resume against the job description.
5. **Extract skills:** The AI returns candidate information, skills, required skills, matched skills, strengths, missing skills, and a summary.
6. **Clean and validate:** Python removes duplicate entries and validates the structured response.
7. **Calculate the match percentage:** Python calculates the percentage based on matched required skills.
8. **Display results:** Streamlit presents the candidate analysis and screening results.

### Match Score Formula

The application uses the following formula:

**Match Score = (Matched Required Skills / Total Required Skills) × 100**

For example, if a job description contains 8 required skills and a candidate matches 6, the score is:

**(6 / 8) × 100 = 75%**

The score measures required-skill coverage. It does not represent a scientifically validated measure of overall candidate quality.

## 🧠 AI Integration

The application uses the Groq API to process resume text and job descriptions.

The AI is instructed to return a structured JSON object containing:

- Candidate name
- Extracted skills
- Required skills
- Matched skills
- Strengths
- Missing skills
- Candidate summary

The application then parses and validates the response before calculating the match percentage in Python.

This separation makes the scoring formula explicit and reproducible for the same validated skill lists.

## 📁 Project Structure

```text
AI-Resume-Screener/
│
├── app.py              # Main Streamlit user interface
├── main.py             # Additional application entry point or logic
├── ai_engine.py        # Groq integration and resume analysis
├── resume_parser.py    # Resume text extraction
├── schemas.py          # Pydantic data models
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
├── README.md           # Project documentation
├── .env                # Local environment variables (not committed)
└── .streamlit/
    └── secrets.toml    # Optional local secrets file (not committed)
```

The `.env` and `.streamlit/secrets.toml` files are local configuration files and should not be committed to GitHub. The exact files present in your repository may differ from this illustrative structure.

## ⚙️ Installation and Setup

### Prerequisites

Before running the project, make sure you have:

- Python installed
- Git installed
- A Groq API key
- An internet connection for API requests

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/Sonikagoel/AI-Resume-Screener.git
```

Navigate to the project directory:

```bash
cd AI-Resume-Screener
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked by your system's execution policy, you can run the commands using the Python interpreter in the virtual environment without activating it.

### 3. Install Dependencies

Install the packages listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root directory.

Add the following line:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your actual API key.

Get your API key from the [Groq Console](https://console.groq.com/keys).

**Security:** Never commit your `.env` file or publish your API key on GitHub.

### 5. Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

Your AI Resume Screener application should now be available in your browser.

## ☁️ Deployment on Streamlit Community Cloud

The project can be deployed using Streamlit Community Cloud.

### Deployment Steps

1. Push the project source code to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with your account.
4. Select the option to create a new app.
5. Choose the repository `Sonikagoel/AI-Resume-Screener`.
6. Select the `main` branch.
7. Set the main file path to `app.py`.
8. Open the app's advanced settings and locate **Secrets**.
9. Configure the Groq API key using TOML syntax.
10. Deploy the application and wait for the build to finish.

### Streamlit Secrets Configuration

In the Streamlit Cloud Secrets editor, enter:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

Replace the placeholder with your actual key. Keep the quotation marks and do not include Markdown code fences in the Secrets editor.

Streamlit Cloud does not automatically receive your computer's local `.env` file. The application must read the key from `st.secrets` or the environment variables configured in the deployment environment.

After pushing code changes to the connected GitHub branch, Streamlit Cloud can automatically redeploy the app.

## 🔐 Security and Privacy

- Store API keys in environment variables or Streamlit Secrets.
- Never commit `.env` or credential-containing secrets files to GitHub.
- Add private configuration files to `.gitignore`.
- If an API key is accidentally exposed, revoke it and generate a replacement.
- Avoid uploading confidential resumes without appropriate authorization.
- Handle candidate information responsibly and follow applicable privacy requirements.
- Do not use AI-generated results as the sole basis for hiring decisions.

## ⚠️ Limitations

- Resume extraction depends on document quality and readable text.
- Scanned PDFs may require OCR support.
- AI-generated results can contain omissions or errors.
- The match score measures required-skill coverage, not overall employability.
- The current Python matching logic normalizes capitalization and whitespace but does not independently perform advanced semantic skill matching.
- API access requires a valid Groq API key and an available, supported model.
- Recruiters should review the original resume and verify important qualifications.

## 🔮 Future Enhancements

Potential future improvements include:

- 📑 PDF report generation for candidate analysis.
- 📊 Candidate comparison dashboards.
- 🏆 Candidate ranking based on configurable criteria.
- 🧠 Improved semantic skill matching and synonym detection.
- 🗄️ Database integration for screening history.
- 📈 Analytics and screening statistics.
- 📂 Additional resume formats and OCR support.
- 👥 Recruiter feedback and review workflows.

## 👩‍💻 Author

**Sonika Goel**

- GitHub: [@Sonikagoel](https://github.com/Sonikagoel)
- Project Repository: [AI Resume Screener](https://github.com/Sonikagoel/AI-Resume-Screener)
- Live Application: [AI Resume Screener on Streamlit](https://ai-resume-screener-7ihofvttjuboxbioctzl3v.streamlit.app/)

## 📄 License

No license is specified by default. If you intend to make this project open source, add a `LICENSE` file and select a license appropriate for your intended use.

---

**AI Resume Screener** — Simplifying resume screening through AI-assisted skill analysis.
