import json

from app.utils.env_utils import setting


def test_create_invalid_user(client_app):
    user_data = {
        "email": "test@foobar.com",
        "password": "1234",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 403
    assert response.json()["detail"] == 'User creation failed'


def test_create_elite_user_weak_password(client_app):
    user_data = {
        "email": f"test@{setting.valid_email_allowed}",
        "password": "1234",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 400


def test_login_elite_user(client_app):
    test_elite_user_strong_password(client_app)
    form_data = {
        "username": f"test@{setting.valid_email_allowed}",
        "password": "1234"
    }
    response = client_app.post("/api/elite/login", data=form_data)
    assert response.status_code == 403


def test_case_sensitive_input_elite_user(client_app):
    user_data = {
        "email": f"test@{setting.valid_email_allowed.upper()}",
        "password": "Anirudh@2001$",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    print(response.json())
    assert response.status_code == 201


def test_elite_user_strong_password(client_app):
    user_data = {
        "email": f"test@{setting.valid_email_allowed}",
        "password": "Anirudh@2001$",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 201
    assert response.json()["is_active"] == False


def test_invalid_credentials(client_app):
    test_elite_user_strong_password(client_app)
    form_data = {
        'username': f'test@{setting.valid_email_allowed}',
        'password': "1234"
    }
    response = client_app.post("/api/elite/login", data=form_data)
    assert response.status_code == 403
