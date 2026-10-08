import pytest
import requests


# ---------- Позитивные тесты ----------

def test_register_user(base_url, new_user_data):
    response = requests.post(f"{base_url}/users", json={"user": new_user_data})

    assert response.status_code == 201
    user = response.json()["user"]
    assert user["username"] == new_user_data["username"]
    assert user["email"] == new_user_data["email"]
    assert user["bio"] is None
    assert user["image"] is None
    assert isinstance(user["token"], str) and user["token"]


def test_login(base_url, registered_user):
    payload = {"user": {"email": registered_user["email"], "password": registered_user["password"]}}
    response = requests.post(f"{base_url}/users/login", json=payload)

    assert response.status_code == 200
    assert response.json()["user"]["username"] == registered_user["username"]


def test_get_current_user(base_url, registered_user):
    headers = {"Authorization": f"Token {registered_user['token']}"}
    response = requests.get(f"{base_url}/user", headers=headers)

    assert response.status_code == 200
    assert response.json()["user"]["email"] == registered_user["email"]


# ---------- Негативные тесты ----------

def test_login_wrong_password(base_url, registered_user):
    payload = {"user": {"email": registered_user["email"], "password": "wrongpassword"}}
    response = requests.post(f"{base_url}/users/login", json=payload)

    assert response.status_code == 401
    assert response.json()["errors"]["credentials"] == ["invalid"]


def test_get_current_user_without_token(base_url):
    response = requests.get(f"{base_url}/user")

    assert response.status_code == 401
    assert response.json()["errors"]["token"] == ["is missing"]


@pytest.mark.parametrize("field", ["username", "email", "password"])
def test_register_with_empty_field(base_url, new_user_data, field):
    new_user_data[field] = ""
    response = requests.post(f"{base_url}/users", json={"user": new_user_data})

    assert response.status_code == 422
    assert response.json()["errors"][field] == ["can't be blank"]


def test_register_duplicate_email(base_url, registered_user, new_user_data):
    new_user_data["email"] = registered_user["email"]
    response = requests.post(f"{base_url}/users", json={"user": new_user_data})

    assert response.status_code == 409
    assert response.json()["errors"]["email"] == ["has already been taken"]
