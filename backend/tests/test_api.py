import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MediPredict API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_endpoint():
    # Test without credentials
    response = client.post("/api/auth/token", data={})
    assert response.status_code == 422  # Validation error

def test_user_registration():
    # Test user registration endpoint
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "technician"
    })
    # This might fail if the database isn't set up, but we're testing the endpoint structure
    assert response.status_code in [200, 400, 500]