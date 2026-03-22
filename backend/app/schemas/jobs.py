from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: Optional[str]
    job_description: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    notes: Optional[str]
    applied_date: date = date.today()


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None
    # All fields optional — partial updates via exclude_unset=True
