from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_submit_form():
    """Test the form submission endpoint"""
    test_data = {
        "name": "Test User",
        "interests": json.dumps(["Python", "Machine Learning"]),
        "experience_level": "intermediate"
    }
    response = client.post("/submit", data=test_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "user_id" in response_data

def test_generate_study_plan():
    """Test study plan generation endpoint"""
    test_data = {
        "course_name": "Python Programming",
        "course_description": "Learn Python from basics to advanced",
        "weekly_hours": 10,
        "start_date": "2025-01-20",
        "end_date": "2025-03-20",
        "fundamentals_percent": 30,
        "development_percent": 40,
        "project_percent": 30
    }
    response = client.post("/generate_study_plan", data=test_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "weekly_breakdown" in response_data

def test_invalid_form_data():
    """Test form submission with invalid data"""
    test_data = {
        "name": "",  # Empty name
        "interests": "[]",
        "experience_level": "invalid_level"
    }
    response = client.post("/submit", data=test_data)
    assert response.status_code == 422  # Validation error
