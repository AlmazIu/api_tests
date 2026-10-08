import os
import uuid

import pytest
import requests

# Адрес API. Можно переопределить: $env:API_URL="https://api.realworld.show/api"
BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def new_user_data():
    """Уникальные данные для регистрации — чтобы тесты не мешали друг другу."""
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{uid}",
        "email": f"user_{uid}@test.com",
        "password": "password123",
    }


@pytest.fixture
def registered_user(base_url, new_user_data):
    """Регистрирует пользователя и возвращает его данные вместе с токеном."""
    response = requests.post(f"{base_url}/users", json={"user": new_user_data})
    assert response.status_code == 201, response.text
    return {**new_user_data, "token": response.json()["user"]["token"]}

@pytest.fixture
def created_article(base_url, registered_user):
    headers = {"Authorization": f"Token {registered_user['token']}"}
    payload = {
        "article": {
            "title": "Fixture article",
            "description": "Created by fixture",
            "body": "Will be deleted after test",
            "tagList": ["fixture"],
        }
    }

    response = requests.post(f"{base_url}/articles", json=payload, headers=headers)
    assert response.status_code == 201
    article = response.json()["article"]

    yield article

    requests.delete(f"{base_url}/articles/{article['slug']}", headers=headers)

@pytest.fixture
def another_user(base_url):
    """Второй пользователь — не автор статьи."""
    uid = uuid.uuid4().hex[:8]
    data = {
        "username": f"other_{uid}",
        "email": f"other_{uid}@test.com",
        "password": "password123",
    }
    response = requests.post(f"{base_url}/users", json={"user": data})
    assert response.status_code == 201, response.text
    return {**data, "token": response.json()["user"]["token"]}