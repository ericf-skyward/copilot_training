from copy import deepcopy

import pytest


def test_root_redirects_to_frontend(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_lists_activities_including_empty_participants(client, activity_data):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activity_data
    assert response.json()["Empty Activity"]["participants"] == []


def test_signup_appears_in_activity_listing(client):
    response = client.post(
        "/activities/Empty%20Activity/signup",
        params={"email": "new+student@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new+student@example.com for Empty Activity"
    }
    assert client.get("/activities").json()["Empty Activity"]["participants"] == [
        "new+student@example.com"
    ]


@pytest.mark.parametrize(
    ("activity", "email", "status", "detail"),
    [
        ("Test Activity", "registered@example.com", 400, "Student is already signed up"),
        ("Missing Activity", "new@example.com", 404, "Activity not found"),
    ],
)
def test_signup_errors_leave_data_unchanged(
    client, activity_data, activity, email, status, detail
):
    before = deepcopy(activity_data)

    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )

    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert client.get("/activities").json() == before


@pytest.mark.parametrize("with_duplicate", [False, True])
def test_unregister_removes_matching_entries_only(client, activity_data, with_duplicate):
    if with_duplicate:
        activity_data["Test Activity"]["participants"].append("registered@example.com")

    response = client.delete(
        "/activities/Test%20Activity/signup",
        params={"email": "registered@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered registered@example.com from Test Activity"
    }
    listing = client.get("/activities").json()
    assert listing["Test Activity"]["participants"] == ["other@example.com"]
    assert listing["Empty Activity"]["participants"] == []


@pytest.mark.parametrize(
    ("activity", "email", "detail"),
    [
        ("Missing Activity", "registered@example.com", "Activity not found"),
        ("Test Activity", "missing@example.com", "Student is not signed up"),
    ],
)
def test_unregister_errors_leave_data_unchanged(
    client, activity_data, activity, email, detail
):
    before = deepcopy(activity_data)

    response = client.delete(
        f"/activities/{activity}/signup", params={"email": email}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": detail}
    assert client.get("/activities").json() == before


@pytest.mark.parametrize("method", ["POST", "DELETE"])
def test_missing_email_returns_validation_error(client, activity_data, method):
    before = deepcopy(activity_data)

    response = client.request(method, "/activities/Test%20Activity/signup")

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
    assert client.get("/activities").json() == before
