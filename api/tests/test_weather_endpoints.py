import datetime
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.db.actions import create_user, find_user_by_id
from api.main import app
from api.tests.utils import delete_user

client = TestClient(app)
USER_ID = 25000


def test_create_weather_data_for_user():
    '''Test POST endpoint to verify the sucessful response is correct.'''
    data = {'user_id': USER_ID}

    response = client.post('/api/weather', json=data)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['user_id'] == data['user_id']
    
    main_keys = ['user_id', 'timestamp', 'status']
    for key in main_keys:
        assert key in response_json
        if key == 'user_id':
            assert response_json['user_id'] == data['user_id']
        elif key == 'status':
            assert response_json['status'] == 'in_progress'


def test_create_weather_data_for_existing_user(get_session):
    '''Test POST endpoint to verify the failure response is correct.'''
    session = get_session
    id = 70000
    timestamp = datetime.datetime.now()
    weather_data = []
    
    user = create_user(session, id, timestamp, weather_data)
    data = {'user_id': id}

    response = client.post('/api/weather', json=data)

    assert response.status_code == 422
    assert response.json()['detail'] == "User ID already exists"

    delete_user(session, user)


def test_get_progress_from_user(get_session):
    '''Test GET endpoint to verify the sucessful response is correct.'''
    session = get_session

    response = client.get(f'/api/weather/{USER_ID}')
    assert response.status_code == 200

    response_json = response.json()
    main_keys = ['user_id', 'progress']
    for key in main_keys:
        assert key in response_json

    assert response_json['user_id'] == USER_ID
    assert isinstance(response_json['progress'], str)
    assert len(response_json['progress']) > 1
    assert response_json['progress'][-1] == '%'

    user = find_user_by_id(session, USER_ID)
    delete_user(session, user)


def test_get_progress_from_non_existing_user():
    '''Test GET endpoint to verify the failure response is correct.'''
    id = 700000

    response = client.get(f'/api/weather/{id}')

    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
