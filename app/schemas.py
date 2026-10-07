from pydantic import BaseModel, EmailStr
from typing import List


class Recipient(BaseModel):
    name: str
    email: EmailStr


class JobCreate(BaseModel):
    course_name: str
    event_date: str
    recipients: List[Recipient]


class JobResponse(BaseModel):
    job_id: int
    status: str
    total: int
    successful: int
    failed: int
    progress: int


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    email: str
    status: str
    file_path: str | None = None
    error_message: str | None = None