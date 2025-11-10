import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Get an activity name
    activities = client.get("/activities").json()
    activity_name = next(iter(activities.keys()))
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "signed up" in response.json()["message"].lower()
    # Try signing up again (should fail or indicate already signed up)
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response2.status_code in (400, 200)

def test_signup_invalid_activity():
    response = client.post("/activities/NonExistentActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
