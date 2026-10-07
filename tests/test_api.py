import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Bulk Certificate Generator API is running"
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_job():
    data = {
        "course_name": "Python Programming",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Test User",
                "email": "test@example.com"
            }
        ]
    }

    response = client.post(
        "/api/jobs/",
        json=data
    )

    assert response.status_code == 200

    result = response.json()

    assert "job_id" in result
    assert result["total"] == 1