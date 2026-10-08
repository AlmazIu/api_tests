import requests

def test_create_article(base_url, registered_user):
    headers = {"Authorization": f"Token {registered_user['token']}"}

    payload = {
        "article": {
            "title": "My first article",
            "description": "About testing",
            "body": "Learning API autotests",
            "tagList": ["python", "pytest"],
        }
    }

    response = requests.post(f"{base_url}/articles", headers=headers, json=payload)
    assert response.status_code == 201

    article = response.json()["article"]
    expected = payload["article"]

    assert article["title"] == expected["title"]
    assert article["description"] == "About testing"
    assert article["body"] == "Learning API autotests"
    assert sorted(article["tagList"]) == sorted(expected["tagList"])
    assert isinstance(article["slug"], str)
    assert article["favorited"] is False
    assert article["favoritesCount"] == 0
    assert article["author"]["username"] == registered_user["username"]

def test_get_article(base_url, created_article):

    response = requests.get(f"{base_url}/articles/{created_article['slug']}")

    assert response.status_code == 200
    article = response.json()["article"]
    assert article["slug"] == created_article["slug"]
    assert article["title"] == created_article["title"]
    assert article["description"] == created_article["description"]
    assert article["body"] == created_article["body"]

def test_delete_article(base_url, registered_user, created_article):
    headers = {"Authorization": f"Token {registered_user['token']}"}

    response = requests.delete(f"{base_url}/articles/{created_article['slug']}",headers=headers)
    assert response.status_code == 204
    get_response = requests.get(f"{base_url}/articles/{created_article['slug']}")
    assert get_response.status_code == 404
    assert get_response.json() == {'errors': {'article': ['not found']}}

def test_delete_article_another_user(base_url, created_article, another_user):

    headers = {"Authorization": f"Token {another_user['token']}"}
    response = requests.delete(f"{base_url}/articles/{created_article['slug']}",headers=headers)
    assert response.status_code == 403
    assert response.json() == {'errors': {'article': ['forbidden']}}
    get_response = requests.get(f"{base_url}/articles/{created_article['slug']}")
    assert get_response.status_code == 200
    assert get_response.json()["article"]["slug"] == created_article["slug"]