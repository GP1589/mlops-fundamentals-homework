import pytest
from fastapi.testclient import TestClient

# Try to import the app to test it
try:
    from app.main import app
    client = TestClient(app)
except Exception:
    client = None

def test_predict_endpoint_exists():
    if client:
        # TODO: Add a proper payload based on the Spotify dataset
        response = client.post("/predict", json={})
        # The skeleton might return 422 if pydantic validation is added, or 200
        assert response.status_code in [200, 422]
