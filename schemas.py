
from pydantic import BaseModel, Field


class CandidateAnalysis(BaseModel):
    candidate_name: str

    # Skills extracted from the resume
    skills: list[str]

    # Skills extracted from the job description
    required_skills: list[str]

    # Skills that match the job requirements
    matched_skills: list[str]

    # Calculated by Python, not guessed by the LLM
    match_score: float = Field(ge=0, le=100)

    strengths: list[str]
    missing_skills: list[str]
    summary: str
