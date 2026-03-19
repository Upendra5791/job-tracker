from datetime import date, datetime
from enum import StrEnum
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


class ApplicationStatus(StrEnum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class Application(SQLModel, table=True):
    """
    Represents a job application record in the system.

    This model stores information about a job application submitted by a user,
    including company details, position information, application status, and
    optional metadata such as job description, salary range, and notes.

    Attributes:
        id: Unique identifier for the application (UUID, primary key).
        user_id: Reference to the user who submitted the application (foreign key).
        company: Name of the company for the job application.
        role: Job title or role name for the position applied to.
        status: Current status of the application (default: APPLIED).
        job_url: Optional URL link to the job posting.
        job_description: Optional full text or excerpt of the job description.
        salary_min: Optional minimum salary offered for the position.
        salary_max: Optional maximum salary offered for the position.
        notes: Optional user notes or comments about the application.
        applied_date: Date when the application was submitted (default: today).
        ai_fit_score: Optional cached AI-generated fit score (0-100) based on resume/job analysis.
        created_at: Timestamp when the record was created (UTC).
        updated_at: Timestamp when the record was last updated (UTC).
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    company: str
    role: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None
    applied_date: date = Field(default_factory=date.today)
    ai_fit_score: Optional[int] = None  # cached 0–100 after analysis
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)