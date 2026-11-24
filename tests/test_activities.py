from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


def test_signup_is_visible_in_non_cacheable_activities_response():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    try:
        activities_response = client.get("/activities")
        assert activities_response.headers["cache-control"] == "no-store"
        assert email in activities_response.json()[activity_name]["participants"]
    finally:
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email},
        )
        assert unregister_response.status_code == 200
