import json
from flask_jwt_extended import create_access_token


def test_home(api):
    resp = api.get("/")
    assert resp.text == "Welcome to our houseplant API"
    assert resp.status == "200 OK"


def test_register(api):
    mock_headers = {'Content-Type': 'application/json'}
    mock_data = json.dumps({"username": "username1",
                            "email": "email1@email1.com",
                            "password": "password1"})

    resp = api.post("/register", data=mock_data, headers=mock_headers)
    assert resp.json == {"message": "User Created"}
    assert resp.status == "201 CREATED"


def test_login(api):
    mock_headers = {
        "Content-Type": "application/json"
    }
    mock_data = json.dumps({"username": "username1",
                            "password": "password1"})
    resp = api.post("/login", data=mock_data, headers=mock_headers)
    assert resp.status == "201 CREATED"


def test_invalid_credentials_login(api):
    mock_headers = {
        "Content-Type": "application/json"
    }
    mock_data = json.dumps({"username": "username1",
                            "password": "invalid"})
    resp = api.post("/login", data=mock_data, headers=mock_headers)
    assert resp.status == "401 UNAUTHORIZED"


def test_show_user(api):
    access_token = create_access_token('username1')
    mock_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    resp = api.get('/users/username1', headers=mock_headers)
    assert resp.status == "200 OK"


def test_create_user_plant(api):
    access_token = create_access_token('username1')
    mock_headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json"
    }

    mock_data = json.dumps({
        "nickname": "plant1",
        "water_freq": 1,
        "purchase_date": "Thu, 02 Mar 2023 00:00:00 GMT",
        "plant_data_id": 41,
    })

    resp = api.post("/users/username1/plants",
                    data=mock_data, headers=mock_headers)
    assert resp.json == {'message': 'Plant Added'}
    assert resp.status == "201 CREATED"


def test_get_user_plants(api):
    access_token = create_access_token('username1')
    mock_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    resp = api.get("/users/username1/plants", headers=mock_headers)
    assert b"plant1" in resp.data
    assert resp.status == "200 OK"


# def test_get_one_user_plant(api):


def test_get_all_plants(api):
    access_token = create_access_token('username1')
    mock_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    resp = api.get("/plants", headers=mock_headers)
    assert type(resp.json) == list
    assert type(resp.json[0]) == dict
    assert resp.status == "200 OK"


def test_get_one_plant(api):
    access_token = create_access_token('username1')
    mock_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    resp = api.get("/plants/41", headers=mock_headers)
    assert type(resp.json) == dict
    assert resp.status == "200 OK"


def test_404_handler(api):
    resp = api.get("/notfound")
    assert resp.status == "404 NOT FOUND"
    assert "Oops!" in resp.json["message"]
