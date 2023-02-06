import json

from app.utils.env_utils import setting
from test.truck_test.truck_test import update_status_of_elite_user

global token


def test_create_invalid_user(client_app):
    user_data = {
        "email": "test@foobar.com",
        "password": "1234",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 403


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


def test_correct_credentials(client_app):
    global token
    test_elite_user_strong_password(client_app)
    login_data = {
        'username': f'test@{setting.valid_email_allowed}',
        'password': 'Anirudh@2001$'
    }

    login_response = client_app.post("/api/elite/login", data=login_data)
    token = login_response.json()['access_token']
    assert login_response.status_code == 201


def test_role_reversal(client_app, local_database_session):
    global token
    test_elite_user_strong_password(client_app)
    update_status_of_elite_user(token, local_database_session)

    response = client_app.put(f"/api/elite/user/access?email=test@{setting.valid_email_allowed}",
                              headers={'Authorization': f'Bearer {token}'})
    print(response.json())
    assert response.status_code == 200
