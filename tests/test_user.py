import requests


def test_update_user_bio(base_url, registered_user):
    headers = {"Authorization": f"Token {registered_user['token']}"}

    payload = {"user": {"bio": "Hello"}}

    response = requests.put(f"{base_url}/user", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["user"]["bio"] == payload["user"]["bio"]


def test_update_user_bio_persisted(base_url, registered_user):
    headers = {"Authorization": f"Token {registered_user['token']}"}

    payload = {"user": {"bio": "Hello"}}

    update_response = requests.put(f"{base_url}/user", json=payload, headers=headers)
    get_response = requests.get(f"{base_url}/user", headers=headers)

    assert get_response.status_code == 200
    assert update_response.status_code == 200
    assert get_response.json()["user"]["bio"] == payload["user"]["bio"]


def test_update_user_without_token(base_url):
    payload = {"user": {"bio": "Hello"}}

    put_response = requests.put(f"{base_url}/user", json=payload)

    assert put_response.status_code == 401
    assert put_response.json()["errors"] == {"token": ["is missing"]}
