from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import jobs

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating certificates in bulk",
    version="1.0.0"
)

# Include Jobs Router
app.include_router(jobs.router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }