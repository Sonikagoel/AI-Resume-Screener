
from ai_engine import analyze_resume
from resume_parser import extract_text_from_pdf, extract_text_from_docx

job_description = """
Python Backend Developer

Required skills:
Python, Django, REST APIs, SQL, Docker, AWS.
"""

file_path = input("Enter resume file path: ").strip().strip('"')

if file_path.lower().endswith(".pdf"):
    resume_text = extract_text_from_pdf(file_path)

elif file_path.lower().endswith(".docx"):
    resume_text = extract_text_from_docx(file_path)

else:
    print("Please provide a PDF or DOCX file.")
    raise SystemExit

if not resume_text.strip():
    print("No text found in the resume.")
    raise SystemExit

result = analyze_resume(resume_text, job_description)

print(result.model_dump_json(indent=2))
