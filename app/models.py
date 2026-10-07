from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    certificates = relationship(
        "Certificate",
        back_populates="job",
        cascade="all, delete"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )

    recipient_name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    status = Column(String, default="PENDING")
    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship(
        "GenerationJob",
        back_populates="certificates"
    )