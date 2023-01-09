import json

from app.models.user_model import User
from app.security.oauth2_bearer import verify_bearer_token
from app.utils.env_utils import setting


def test_add_truck_new_user_without_authority(client_app):
    """Create a new elite user"""
    user_data = {
        "email": f"test@{setting.valid_email_allowed}",
        "password": "Anirudh@2001$",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 201
    assert response.json()["is_active"] == False

    """Login the new user"""

    login_response = client_app.post("/api/elite/login",
                                     data={'username': f'test@{setting.valid_email_allowed}',
                                           'password': 'Anirudh@2001$'})
    assert login_response.status_code == 201
    access_token = login_response.json()['access_token']

    """Add a truck"""
    truck_data = {
        "site": "KPCL",
        "trailer_number": "TEST",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST"
    }
    custom_header = {
        'Authorization': f"Bearer {access_token}"
    }
    truck_response = client_app.post("/api/elite/truck/add", content=json.dumps(truck_data), headers=custom_header)
    assert truck_response.status_code == 403


def test_add_new_truck_with_authority(client_app, local_database_session):
    """Create a new elite user"""
    user_data = {
        "email": f"test@{setting.valid_email_allowed}",
        "password": "Anirudh@2001$",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 201
    assert response.json()["is_active"] == False

    """Login the new user"""

    login_response = client_app.post("/api/elite/login",
                                     data={'username': f'test@{setting.valid_email_allowed}',
                                           'password': 'Anirudh@2001$'})
    assert login_response.status_code == 201
    access_token = login_response.json()['access_token']

    """Provide authority level access to the user"""
    local_database_session.query(User).filter(User.id == verify_bearer_token(access_token)).update({
        'is_active': True,
        'authority_level': int(setting.authority_level)
    }, synchronize_session=False)

    """Add a truck"""
    truck_data = {
        "site": "KPCL",
        "trailer_number": "TEST",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST"
    }
    custom_header = {
        'Authorization': f"Bearer {access_token}"
    }
    truck_response = client_app.post("/api/elite/truck/add", content=json.dumps(truck_data), headers=custom_header)
    assert truck_response.status_code == 201
