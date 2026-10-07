# Bulk Certificate Generator API

A FastAPI-based backend application that generates certificates in bulk for multiple recipients.

## Project Overview

The Bulk Certificate Generator API allows users to create certificate generation jobs for multiple recipients.

The application processes recipients in the background, generates individual PDF certificates, stores generation status in a relational database, and provides APIs to check job progress, retrieve certificates, and download generated certificates.

## Features

- Create bulk certificate generation jobs
- Generate certificates for multiple recipients
- Background certificate processing
- PDF certificate generation
- Individual recipient failure handling
- Job status tracking
- Progress tracking
- Retrieve certificates for a job
- Download individual certificates
- Email validation
- SQLite database
- RESTful APIs
- Automated API testing using pytest

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Uvicorn
- Pytest
- HTTPX

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── jobs.py
│   │
│   └── services/
│       ├── __init__.py
│       └── certificate_generator.py
│
├── tests/
│   └── test_api.py
│
├── templates/
├── generated_certificates/
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md