from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GenerationJob, Certificate
from app.schemas import JobCreate
from app.services.certificate_generator import generate_certificate

import os
from datetime import datetime


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


def generate_certificates_for_job(job_id: int):
    db = next(get_db())

    try:
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        certificates = db.query(Certificate).filter(
            Certificate.job_id == job_id
        ).all()

        for certificate in certificates:
            try:
                os.makedirs(
                    "generated_certificates",
                    exist_ok=True
                )

                safe_name = certificate.recipient_name.replace(
                    " ",
                    "_"
                )

                filename = (
                    f"{job_id}_{certificate.id}_{safe_name}.pdf"
                )

                output_path = os.path.join(
                    "generated_certificates",
                    filename
                )

                generate_certificate(
                    recipient_name=certificate.recipient_name,
                    course_name=job.course_name,
                    event_date=job.event_date,
                    output_path=output_path
                )

                certificate.status = "SUCCESS"
                certificate.file_path = output_path

                job.success_count += 1

            except Exception as e:
                certificate.status = "FAILED"
                certificate.error_message = str(e)

                job.failed_count += 1

            db.commit()

        if job.failed_count == 0:
            job.status = "COMPLETED"
        else:
            job.status = "COMPLETED_WITH_ERRORS"

        job.completed_at = datetime.utcnow()

        db.commit()

    finally:
        db.close()


@router.post("/")
def create_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = GenerationJob(
        course_name=job_data.course_name,
        event_date=job_data.event_date,
        status="PENDING",
        total_count=len(job_data.recipients),
        success_count=0,
        failed_count=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in job_data.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    background_tasks.add_task(
        generate_certificates_for_job,
        job.id
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total_count,
        "successful": job.success_count,
        "failed": job.failed_count,
        "progress": 0
    }


@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        return {
            "error": "Job not found"
        }

    if job.total_count > 0:
        progress = int(
            ((job.success_count + job.failed_count)
             / job.total_count) * 100
        )
    else:
        progress = 0

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total_count,
        "successful": job.success_count,
        "failed": job.failed_count,
        "progress": progress
    }


@router.get("/{job_id}/certificates")
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        return {
            "error": "Job not found"
        }

    certificates = db.query(Certificate).filter(
        Certificate.job_id == job_id
    ).all()

    return {
        "job_id": job_id,
        "total": len(certificates),
        "certificates": [
            {
                "id": certificate.id,
                "recipient_name": certificate.recipient_name,
                "email": certificate.email,
                "status": certificate.status,
                "file_path": certificate.file_path,
                "error_message": certificate.error_message
            }
            for certificate in certificates
        ]
    }


@router.get("/certificates/{certificate_id}/download")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        return {
            "error": "Certificate not found"
        }

    if certificate.status != "SUCCESS":
        return {
            "error": "Certificate is not available"
        }

    if not certificate.file_path:
        return {
            "error": "Certificate file not found"
        }

    if not os.path.exists(certificate.file_path):
        return {
            "error": "Certificate file does not exist"
        }

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=os.path.basename(
            certificate.file_path
        )
    )