import json

from app.models.user_model import User
from app.security.oauth2_bearer import verify_bearer_token
from app.utils.env_utils import setting

global truck_id, access_token, trailer_number

dummy_truck_data = [
    {
        "site": "KPCL",
        "trailer_number": "TEST",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST"
    },
    {
        "site": "KAT",
        "trailer_number": "TEST1",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST2"
    },
    {
        "site": "SHE",
        "trailer_number": "TEST2",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST3"
    }
]


def test_add_truck_new_user_without_authority(client_app):
    global access_token
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
    global truck_id, access_token, trailer_number
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
    update_status_of_elite_user(access_token, local_database_session)

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
    truck_id = truck_response.json()['truck_id']
    trailer_number = truck_response.json()['trailer_number']
    assert truck_response.status_code == 201


def test_fetch_truck_by_id(client_app, local_database_session):
    global truck_id, access_token
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    test_add_new_truck_with_authority(client_app, local_database_session)
    truck_response = client_app.get(f"/api/elite/truck/fetch?truck_id={truck_id}", headers=auth_headers)
    assert truck_response.status_code == 200
    assert truck_response.json()['truck_id'] == truck_id


def test_invalid_site(client_app, local_database_session):
    global access_token
    user_data = {
        "email": f"test@{setting.valid_email_allowed}",
        "password": "Anirudh@2001$",
        "name": "anirudh"
    }
    response = client_app.post("/api/elite/create", content=json.dumps(user_data))
    assert response.status_code == 201
    assert response.json()["is_active"] == False
    login_response = client_app.post("/api/elite/login",
                                     data={'username': f'test@{setting.valid_email_allowed}',
                                           'password': 'Anirudh@2001$'})
    assert login_response.status_code == 201
    update_status_of_elite_user(login_response.json()["access_token"], local_database_session)
    access_token = f'Bearer {login_response.json()["access_token"]}'
    truck_data = {
        "site": "TEST",
        "trailer_number": "TEST",
        "trailer_info": "TEST",
        "chasis_number": "TEST",
        "engine_number": "TEST",
        "trailer_length": 23,
        "suspension": "TEST",
        "engine": "TEST"
    }
    truck_response = client_app.post("/api/elite/truck/add", json=truck_data, headers={
        'Authorization': access_token
    })
    print(truck_response.json())
    assert truck_response.status_code == 400


def test_update_truck_detail(client_app, local_database_session):
    global access_token, truck_id
    test_add_new_truck_with_authority(client_app, local_database_session)
    truck_data = {
        "site": "KPCL",
        "trailer_number": "TEST124121",
        "trailer_info": "TEST",
        "chasis_number": "TEST1212121",
        "engine_number": "TEST121212",
        "trailer_length": 36,
        "suspension": "TEST181",
        "engine": "TEST"
    }
    print(access_token)
    update_truck_response = client_app.put("/api/elite/truck/update?truck_id="
                                           f"{truck_id}", headers={'Authorization': f'Bearer {access_token}'},
                                           json=truck_data)
    print(update_truck_response.json())
    assert update_truck_response.status_code == 200


def test_enable_disable_of_truck(client_app, local_database_session):
    global access_token, trailer_number
    test_add_new_truck_with_authority(client_app, local_database_session)
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client_app.put(f"/api/elite/truck?trailer_number={trailer_number}", headers=auth_headers)
    assert response.status_code == 200




def update_status_of_elite_user(token, local_database_session):
    local_database_session.query(User).filter(User.id == verify_bearer_token(token)).update({
        'is_active': True,
        'authority_level': int(setting.authority_level)
    }, synchronize_session=False)
